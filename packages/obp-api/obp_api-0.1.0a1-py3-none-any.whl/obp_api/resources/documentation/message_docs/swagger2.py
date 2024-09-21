# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...._base_client import make_request_options

__all__ = ["Swagger2Resource", "AsyncSwagger2Resource"]


class Swagger2Resource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> Swagger2ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return Swagger2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> Swagger2ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return Swagger2ResourceWithStreamingResponse(self)

    def _0(
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
        <p>This endpoint provides example message docs in swagger format.<br />It is only relavent for REST Connectors.</p><p>This endpoint can be used by the developer building a REST Adapter that connects to the Core Banking System (CBS).<br />That is, the Adapter developer can use the Swagger surfaced here to build the REST APIs that the OBP REST connector will call to consume CBS services.</p><p>i.e.:</p><p>OBP API (Core OBP API code) -&gt; OBP REST Connector (OBP REST Connector code) -&gt; OBP REST Adapter (Adapter developer code) -&gt; CBS (Main Frame)</p><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/message-docs/CONNECTOR/swagger2.0",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncSwagger2Resource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSwagger2ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSwagger2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSwagger2ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncSwagger2ResourceWithStreamingResponse(self)

    async def _0(
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
        <p>This endpoint provides example message docs in swagger format.<br />It is only relavent for REST Connectors.</p><p>This endpoint can be used by the developer building a REST Adapter that connects to the Core Banking System (CBS).<br />That is, the Adapter developer can use the Swagger surfaced here to build the REST APIs that the OBP REST connector will call to consume CBS services.</p><p>i.e.:</p><p>OBP API (Core OBP API code) -&gt; OBP REST Connector (OBP REST Connector code) -&gt; OBP REST Adapter (Adapter developer code) -&gt; CBS (Main Frame)</p><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/message-docs/CONNECTOR/swagger2.0",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class Swagger2ResourceWithRawResponse:
    def __init__(self, swagger2: Swagger2Resource) -> None:
        self._swagger2 = swagger2

        self._0 = to_custom_raw_response_wrapper(
            swagger2._0,
            BinaryAPIResponse,
        )


class AsyncSwagger2ResourceWithRawResponse:
    def __init__(self, swagger2: AsyncSwagger2Resource) -> None:
        self._swagger2 = swagger2

        self._0 = async_to_custom_raw_response_wrapper(
            swagger2._0,
            AsyncBinaryAPIResponse,
        )


class Swagger2ResourceWithStreamingResponse:
    def __init__(self, swagger2: Swagger2Resource) -> None:
        self._swagger2 = swagger2

        self._0 = to_custom_streamed_response_wrapper(
            swagger2._0,
            StreamedBinaryAPIResponse,
        )


class AsyncSwagger2ResourceWithStreamingResponse:
    def __init__(self, swagger2: AsyncSwagger2Resource) -> None:
        self._swagger2 = swagger2

        self._0 = async_to_custom_streamed_response_wrapper(
            swagger2._0,
            AsyncStreamedBinaryAPIResponse,
        )
