# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

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

__all__ = ["SuggestedSessionTimeoutResource", "AsyncSuggestedSessionTimeoutResource"]


class SuggestedSessionTimeoutResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SuggestedSessionTimeoutResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return SuggestedSessionTimeoutResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SuggestedSessionTimeoutResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return SuggestedSessionTimeoutResourceWithStreamingResponse(self)

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
        <p>Returns information about:</p><ul><li>Suggested session timeout in case of a user inactivity</li></ul><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/ui/suggested-session-timeout",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncSuggestedSessionTimeoutResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSuggestedSessionTimeoutResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSuggestedSessionTimeoutResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSuggestedSessionTimeoutResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncSuggestedSessionTimeoutResourceWithStreamingResponse(self)

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
        <p>Returns information about:</p><ul><li>Suggested session timeout in case of a user inactivity</li></ul><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/ui/suggested-session-timeout",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class SuggestedSessionTimeoutResourceWithRawResponse:
    def __init__(self, suggested_session_timeout: SuggestedSessionTimeoutResource) -> None:
        self._suggested_session_timeout = suggested_session_timeout

        self.retrieve = to_custom_raw_response_wrapper(
            suggested_session_timeout.retrieve,
            BinaryAPIResponse,
        )


class AsyncSuggestedSessionTimeoutResourceWithRawResponse:
    def __init__(self, suggested_session_timeout: AsyncSuggestedSessionTimeoutResource) -> None:
        self._suggested_session_timeout = suggested_session_timeout

        self.retrieve = async_to_custom_raw_response_wrapper(
            suggested_session_timeout.retrieve,
            AsyncBinaryAPIResponse,
        )


class SuggestedSessionTimeoutResourceWithStreamingResponse:
    def __init__(self, suggested_session_timeout: SuggestedSessionTimeoutResource) -> None:
        self._suggested_session_timeout = suggested_session_timeout

        self.retrieve = to_custom_streamed_response_wrapper(
            suggested_session_timeout.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncSuggestedSessionTimeoutResourceWithStreamingResponse:
    def __init__(self, suggested_session_timeout: AsyncSuggestedSessionTimeoutResource) -> None:
        self._suggested_session_timeout = suggested_session_timeout

        self.retrieve = async_to_custom_streamed_response_wrapper(
            suggested_session_timeout.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
