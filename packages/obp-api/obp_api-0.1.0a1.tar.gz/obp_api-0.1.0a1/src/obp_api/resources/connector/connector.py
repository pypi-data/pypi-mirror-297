# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .metrics import (
    MetricsResource,
    AsyncMetricsResource,
    MetricsResourceWithRawResponse,
    AsyncMetricsResourceWithRawResponse,
    MetricsResourceWithStreamingResponse,
    AsyncMetricsResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["ConnectorResource", "AsyncConnectorResource"]


class ConnectorResource(SyncAPIResource):
    @cached_property
    def metrics(self) -> MetricsResource:
        return MetricsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ConnectorResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ConnectorResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConnectorResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ConnectorResourceWithStreamingResponse(self)

    def loopback(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>This endpoint makes a call to the Connector to check the backend transport (e.g. Kafka) is reachable.</p><p>Currently this is only implemented for Kafka based connectors.</p><p>For Kafka based connectors, this endpoint writes a message to Kafka and reads it again.</p><p>In the future, this endpoint may also return information about database connections etc.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/connector/loopback",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncConnectorResource(AsyncAPIResource):
    @cached_property
    def metrics(self) -> AsyncMetricsResource:
        return AsyncMetricsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncConnectorResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConnectorResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConnectorResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncConnectorResourceWithStreamingResponse(self)

    async def loopback(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>This endpoint makes a call to the Connector to check the backend transport (e.g. Kafka) is reachable.</p><p>Currently this is only implemented for Kafka based connectors.</p><p>For Kafka based connectors, this endpoint writes a message to Kafka and reads it again.</p><p>In the future, this endpoint may also return information about database connections etc.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/connector/loopback",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ConnectorResourceWithRawResponse:
    def __init__(self, connector: ConnectorResource) -> None:
        self._connector = connector

        self.loopback = to_custom_raw_response_wrapper(
            connector.loopback,
            BinaryAPIResponse,
        )

    @cached_property
    def metrics(self) -> MetricsResourceWithRawResponse:
        return MetricsResourceWithRawResponse(self._connector.metrics)


class AsyncConnectorResourceWithRawResponse:
    def __init__(self, connector: AsyncConnectorResource) -> None:
        self._connector = connector

        self.loopback = async_to_custom_raw_response_wrapper(
            connector.loopback,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithRawResponse:
        return AsyncMetricsResourceWithRawResponse(self._connector.metrics)


class ConnectorResourceWithStreamingResponse:
    def __init__(self, connector: ConnectorResource) -> None:
        self._connector = connector

        self.loopback = to_custom_streamed_response_wrapper(
            connector.loopback,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def metrics(self) -> MetricsResourceWithStreamingResponse:
        return MetricsResourceWithStreamingResponse(self._connector.metrics)


class AsyncConnectorResourceWithStreamingResponse:
    def __init__(self, connector: AsyncConnectorResource) -> None:
        self._connector = connector

        self.loopback = async_to_custom_streamed_response_wrapper(
            connector.loopback,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithStreamingResponse:
        return AsyncMetricsResourceWithStreamingResponse(self._connector.metrics)
