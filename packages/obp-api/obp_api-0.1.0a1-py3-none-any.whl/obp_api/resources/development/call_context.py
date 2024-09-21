# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["CallContextResource", "AsyncCallContextResource"]


class CallContextResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CallContextResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CallContextResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CallContextResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CallContextResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Get the Call Context of the current call.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/development/call_context",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncCallContextResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCallContextResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCallContextResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCallContextResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCallContextResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Get the Call Context of the current call.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/development/call_context",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class CallContextResourceWithRawResponse:
    def __init__(self, call_context: CallContextResource) -> None:
        self._call_context = call_context

        self.retrieve = to_raw_response_wrapper(
            call_context.retrieve,
        )


class AsyncCallContextResourceWithRawResponse:
    def __init__(self, call_context: AsyncCallContextResource) -> None:
        self._call_context = call_context

        self.retrieve = async_to_raw_response_wrapper(
            call_context.retrieve,
        )


class CallContextResourceWithStreamingResponse:
    def __init__(self, call_context: CallContextResource) -> None:
        self._call_context = call_context

        self.retrieve = to_streamed_response_wrapper(
            call_context.retrieve,
        )


class AsyncCallContextResourceWithStreamingResponse:
    def __init__(self, call_context: AsyncCallContextResource) -> None:
        self._call_context = call_context

        self.retrieve = async_to_streamed_response_wrapper(
            call_context.retrieve,
        )
