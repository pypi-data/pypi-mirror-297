# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["RateLimitsResource", "AsyncRateLimitsResource"]


class RateLimitsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RateLimitsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return RateLimitsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RateLimitsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return RateLimitsResourceWithStreamingResponse(self)

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
        <p>Get information about the Rate Limiting setup on this OBP Instance such as:</p><p>Is rate limiting enabled and active?<br />What backend is used to keep track of the API calls (e.g. REDIS).</p><p>Note: Rate limiting can be set at the Consumer level and also for anonymous calls.</p><p>See the consumer rate limits / call limits endpoints.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/rate-limiting",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncRateLimitsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRateLimitsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRateLimitsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRateLimitsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncRateLimitsResourceWithStreamingResponse(self)

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
        <p>Get information about the Rate Limiting setup on this OBP Instance such as:</p><p>Is rate limiting enabled and active?<br />What backend is used to keep track of the API calls (e.g. REDIS).</p><p>Note: Rate limiting can be set at the Consumer level and also for anonymous calls.</p><p>See the consumer rate limits / call limits endpoints.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/rate-limiting",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class RateLimitsResourceWithRawResponse:
    def __init__(self, rate_limits: RateLimitsResource) -> None:
        self._rate_limits = rate_limits

        self.retrieve = to_custom_raw_response_wrapper(
            rate_limits.retrieve,
            BinaryAPIResponse,
        )


class AsyncRateLimitsResourceWithRawResponse:
    def __init__(self, rate_limits: AsyncRateLimitsResource) -> None:
        self._rate_limits = rate_limits

        self.retrieve = async_to_custom_raw_response_wrapper(
            rate_limits.retrieve,
            AsyncBinaryAPIResponse,
        )


class RateLimitsResourceWithStreamingResponse:
    def __init__(self, rate_limits: RateLimitsResource) -> None:
        self._rate_limits = rate_limits

        self.retrieve = to_custom_streamed_response_wrapper(
            rate_limits.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncRateLimitsResourceWithStreamingResponse:
    def __init__(self, rate_limits: AsyncRateLimitsResource) -> None:
        self._rate_limits = rate_limits

        self.retrieve = async_to_custom_streamed_response_wrapper(
            rate_limits.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
