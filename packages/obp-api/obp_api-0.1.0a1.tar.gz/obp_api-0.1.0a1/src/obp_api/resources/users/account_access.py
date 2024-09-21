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

__all__ = ["AccountAccessResource", "AsyncAccountAccessResource"]


class AccountAccessResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AccountAccessResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AccountAccessResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AccountAccessResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AccountAccessResourceWithStreamingResponse(self)

    def list(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get Account Access by USER_ID</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/users/{user_id}/account-access",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAccountAccessResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAccountAccessResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAccountAccessResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAccountAccessResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAccountAccessResourceWithStreamingResponse(self)

    async def list(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get Account Access by USER_ID</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/users/{user_id}/account-access",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class AccountAccessResourceWithRawResponse:
    def __init__(self, account_access: AccountAccessResource) -> None:
        self._account_access = account_access

        self.list = to_custom_raw_response_wrapper(
            account_access.list,
            BinaryAPIResponse,
        )


class AsyncAccountAccessResourceWithRawResponse:
    def __init__(self, account_access: AsyncAccountAccessResource) -> None:
        self._account_access = account_access

        self.list = async_to_custom_raw_response_wrapper(
            account_access.list,
            AsyncBinaryAPIResponse,
        )


class AccountAccessResourceWithStreamingResponse:
    def __init__(self, account_access: AccountAccessResource) -> None:
        self._account_access = account_access

        self.list = to_custom_streamed_response_wrapper(
            account_access.list,
            StreamedBinaryAPIResponse,
        )


class AsyncAccountAccessResourceWithStreamingResponse:
    def __init__(self, account_access: AsyncAccountAccessResource) -> None:
        self._account_access = account_access

        self.list = async_to_custom_streamed_response_wrapper(
            account_access.list,
            AsyncStreamedBinaryAPIResponse,
        )
