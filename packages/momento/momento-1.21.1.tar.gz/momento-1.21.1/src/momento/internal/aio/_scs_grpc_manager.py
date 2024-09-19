from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Optional

import grpc
from momento_wire_types import cacheclient_pb2_grpc as cache_client
from momento_wire_types import cachepubsub_pb2_grpc as pubsub_client
from momento_wire_types import controlclient_pb2_grpc as control_client

from momento.auth import CredentialProvider
from momento.config import Configuration, TopicConfiguration
from momento.config.transport.transport_strategy import StaticGrpcConfiguration
from momento.errors.exceptions import ConnectionException
from momento.internal._utilities import PYTHON_RUNTIME_VERSION, ClientType, momento_version
from momento.internal._utilities._channel_credentials import (
    channel_credentials_from_root_certs_or_default,
)
from momento.internal._utilities._grpc_channel_options import (
    grpc_control_channel_options_from_grpc_config,
    grpc_data_channel_options_from_grpc_config,
)
from momento.internal.services import Service
from momento.retry import RetryStrategy

from ... import logs
from ._add_header_client_interceptor import (
    AddHeaderClientInterceptor,
    AddHeaderStreamingClientInterceptor,
    Header,
)
from ._retry_interceptor import RetryInterceptor


class _ControlGrpcManager:
    """Internal gRPC control manager."""

    version = momento_version

    def __init__(self, configuration: Configuration, credential_provider: CredentialProvider):
        self._secure_channel = grpc.aio.secure_channel(
            target=credential_provider.control_endpoint,
            credentials=channel_credentials_from_root_certs_or_default(configuration),
            interceptors=_interceptors(
                credential_provider.auth_token, ClientType.CACHE, configuration.get_retry_strategy()
            ),
            options=grpc_control_channel_options_from_grpc_config(
                grpc_config=configuration.get_transport_strategy().get_grpc_configuration(),
            ),
        )

    async def close(self) -> None:
        await self._secure_channel.close()

    def async_stub(self) -> control_client.ScsControlStub:
        return control_client.ScsControlStub(self._secure_channel)  # type: ignore[no-untyped-call]


class _DataGrpcManager:
    """Internal gRPC data manager."""

    version = momento_version

    def __init__(self, configuration: Configuration, credential_provider: CredentialProvider):
        self._logger = logs.logger
        self._secure_channel = grpc.aio.secure_channel(
            target=credential_provider.cache_endpoint,
            credentials=channel_credentials_from_root_certs_or_default(configuration),
            interceptors=_interceptors(
                credential_provider.auth_token, ClientType.CACHE, configuration.get_retry_strategy()
            ),
            # Here is where you would pass override configuration to the underlying C gRPC layer.
            # However, I have tried several different tuning options here and did not see any
            # performance improvements, so sticking with the defaults for now.
            # For more info on the performance investigations:
            # https://github.com/momentohq/client-sdk-python/issues/120
            # For more info on available gRPC config options:
            # https://grpc.github.io/grpc/python/grpc.html
            # https://grpc.github.io/grpc/python/glossary.html#term-channel_arguments
            # https://github.com/grpc/grpc/blob/v1.46.x/include/grpc/impl/codegen/grpc_types.h#L140
            # options=[
            #     ('grpc.max_concurrent_streams', 1000),
            #     ('grpc.use_local_subchannel_pool', 1),
            #     (experimental.ChannelOptions.SingleThreadedUnaryStream, 1)
            # ],
            options=grpc_data_channel_options_from_grpc_config(
                configuration.get_transport_strategy().get_grpc_configuration()
            ),
        )

    async def eagerly_connect(self, timeout_seconds: float) -> None:
        self._logger.debug(
            f"Attempting to create an eager connection with Momento's server within {timeout_seconds} seconds"
        )
        try:
            await asyncio.wait_for(self.wait_for_ready(), timeout_seconds)
        except Exception as error:
            self._secure_channel.close()
            self._logger.debug(f"Failed to connect to the server within the given timeout. {error}")
            raise ConnectionException(
                message=f"Failed to connect to Momento's server within given eager connection timeout: {error}",
                service=Service.CACHE,
            ) from error

    async def wait_for_ready(self) -> None:
        latest_state = self._secure_channel.get_state(True)  # try_to_connect
        ready: grpc.ChannelConnectivity = grpc.ChannelConnectivity.READY
        connecting: grpc.ChannelConnectivity = grpc.ChannelConnectivity.CONNECTING
        idle: grpc.ChannelConnectivity = grpc.ChannelConnectivity.IDLE

        while latest_state != ready:
            if latest_state == idle:
                self._logger.debug("State is idle; waiting to transition to CONNECTING")
            elif latest_state == connecting:
                self._logger.debug("State transitioned to CONNECTING; waiting to get READY")
            else:
                self._logger.warn(f"Unexpected connection state while trying to eagerly connect: {latest_state}.")
                break

            # This is a gRPC callback helper that prevents us from repeatedly polling on the state
            # which is highly inefficient.
            await self._secure_channel.wait_for_state_change(latest_state)
            latest_state = self._secure_channel.get_state(False)  # no need to reconnect

        if latest_state == ready:
            self._logger.debug("Connected to Momento's server! Happy Caching!")

    async def close(self) -> None:
        self._logger.debug("Closing and tearing down gRPC channel")
        await self._secure_channel.close()

    def async_stub(self) -> cache_client.ScsStub:
        return cache_client.ScsStub(self._secure_channel)  # type: ignore[no-untyped-call]


class _PubsubGrpcManager:
    """Internal gRPC pubsub manager."""

    version = momento_version

    def __init__(self, configuration: TopicConfiguration, credential_provider: CredentialProvider):
        # NOTE: This is hard-coded for now but we may want to expose it via TopicConfiguration in the future, as we do with some of the other clients.
        grpc_config = StaticGrpcConfiguration(deadline=timedelta(milliseconds=1100))

        self._secure_channel = grpc.aio.secure_channel(
            target=credential_provider.cache_endpoint,
            credentials=grpc.ssl_channel_credentials(),
            interceptors=_interceptors(credential_provider.auth_token, ClientType.TOPIC, None),
            options=grpc_data_channel_options_from_grpc_config(grpc_config),
        )

    async def close(self) -> None:
        await self._secure_channel.close()

    def async_stub(self) -> pubsub_client.PubsubStub:
        return pubsub_client.PubsubStub(self._secure_channel)  # type: ignore[no-untyped-call]


class _PubsubGrpcStreamManager:
    """Internal gRPC pubsub stream manager."""

    version = momento_version

    def __init__(self, configuration: TopicConfiguration, credential_provider: CredentialProvider):
        # NOTE: This is hard-coded for now but we may want to expose it via TopicConfiguration in the future, as we do with some of the other clients.
        grpc_config = StaticGrpcConfiguration(deadline=timedelta(milliseconds=1100))

        self._secure_channel = grpc.aio.secure_channel(
            target=credential_provider.cache_endpoint,
            credentials=grpc.ssl_channel_credentials(),
            interceptors=_stream_interceptors(credential_provider.auth_token, ClientType.TOPIC),
            options=grpc_data_channel_options_from_grpc_config(grpc_config),
        )

    async def close(self) -> None:
        await self._secure_channel.close()

    def async_stub(self) -> pubsub_client.PubsubStub:
        return pubsub_client.PubsubStub(self._secure_channel)  # type: ignore[no-untyped-call]


def _interceptors(
    auth_token: str, client_type: ClientType, retry_strategy: Optional[RetryStrategy] = None
) -> list[grpc.aio.ClientInterceptor]:
    headers = [
        Header("authorization", auth_token),
        Header("agent", f"python:{client_type.value}:{_ControlGrpcManager.version}"),
        Header("runtime-version", f"python {PYTHON_RUNTIME_VERSION}"),
    ]
    return list(
        filter(
            None,
            [
                AddHeaderClientInterceptor(headers),
                RetryInterceptor(retry_strategy) if retry_strategy else None,
            ],
        )
    )


def _stream_interceptors(auth_token: str, client_type: ClientType) -> list[grpc.aio.UnaryStreamClientInterceptor]:
    headers = [
        Header("authorization", auth_token),
        Header("agent", f"python:{client_type.value}:{_PubsubGrpcStreamManager.version}"),
        Header("runtime-version", f"python {PYTHON_RUNTIME_VERSION}"),
    ]
    return [AddHeaderStreamingClientInterceptor(headers)]
