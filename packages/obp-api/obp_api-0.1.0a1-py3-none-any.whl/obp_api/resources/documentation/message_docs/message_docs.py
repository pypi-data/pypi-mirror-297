# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .swagger2 import (
    Swagger2Resource,
    AsyncSwagger2Resource,
    Swagger2ResourceWithRawResponse,
    AsyncSwagger2ResourceWithRawResponse,
    Swagger2ResourceWithStreamingResponse,
    AsyncSwagger2ResourceWithStreamingResponse,
)
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

__all__ = ["MessageDocsResource", "AsyncMessageDocsResource"]


class MessageDocsResource(SyncAPIResource):
    @cached_property
    def swagger2(self) -> Swagger2Resource:
        return Swagger2Resource(self._client)

    @cached_property
    def with_raw_response(self) -> MessageDocsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return MessageDocsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MessageDocsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return MessageDocsResourceWithStreamingResponse(self)

    def retrieve(
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
        <p>These message docs provide example messages sent by OBP to the (Kafka) message queue for processing by the Core Banking / Payment system Adapter - together with an example expected response and possible error codes.<br />Integrators can use these messages to build Adapters that provide core banking services to OBP.</p><p>Note: API Explorer provides a Message Docs page where these messages are displayed.</p><p><code>CONNECTOR</code>: kafka_vSept2018, stored_procedure_vDec2019 ...</p><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/message-docs/CONNECTOR",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncMessageDocsResource(AsyncAPIResource):
    @cached_property
    def swagger2(self) -> AsyncSwagger2Resource:
        return AsyncSwagger2Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMessageDocsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMessageDocsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMessageDocsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncMessageDocsResourceWithStreamingResponse(self)

    async def retrieve(
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
        <p>These message docs provide example messages sent by OBP to the (Kafka) message queue for processing by the Core Banking / Payment system Adapter - together with an example expected response and possible error codes.<br />Integrators can use these messages to build Adapters that provide core banking services to OBP.</p><p>Note: API Explorer provides a Message Docs page where these messages are displayed.</p><p><code>CONNECTOR</code>: kafka_vSept2018, stored_procedure_vDec2019 ...</p><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/message-docs/CONNECTOR",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class MessageDocsResourceWithRawResponse:
    def __init__(self, message_docs: MessageDocsResource) -> None:
        self._message_docs = message_docs

        self.retrieve = to_custom_raw_response_wrapper(
            message_docs.retrieve,
            BinaryAPIResponse,
        )

    @cached_property
    def swagger2(self) -> Swagger2ResourceWithRawResponse:
        return Swagger2ResourceWithRawResponse(self._message_docs.swagger2)


class AsyncMessageDocsResourceWithRawResponse:
    def __init__(self, message_docs: AsyncMessageDocsResource) -> None:
        self._message_docs = message_docs

        self.retrieve = async_to_custom_raw_response_wrapper(
            message_docs.retrieve,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def swagger2(self) -> AsyncSwagger2ResourceWithRawResponse:
        return AsyncSwagger2ResourceWithRawResponse(self._message_docs.swagger2)


class MessageDocsResourceWithStreamingResponse:
    def __init__(self, message_docs: MessageDocsResource) -> None:
        self._message_docs = message_docs

        self.retrieve = to_custom_streamed_response_wrapper(
            message_docs.retrieve,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def swagger2(self) -> Swagger2ResourceWithStreamingResponse:
        return Swagger2ResourceWithStreamingResponse(self._message_docs.swagger2)


class AsyncMessageDocsResourceWithStreamingResponse:
    def __init__(self, message_docs: AsyncMessageDocsResource) -> None:
        self._message_docs = message_docs

        self.retrieve = async_to_custom_streamed_response_wrapper(
            message_docs.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def swagger2(self) -> AsyncSwagger2ResourceWithStreamingResponse:
        return AsyncSwagger2ResourceWithStreamingResponse(self._message_docs.swagger2)
