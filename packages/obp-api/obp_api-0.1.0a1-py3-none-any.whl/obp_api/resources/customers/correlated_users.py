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

__all__ = ["CorrelatedUsersResource", "AsyncCorrelatedUsersResource"]


class CorrelatedUsersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CorrelatedUsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CorrelatedUsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CorrelatedUsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CorrelatedUsersResourceWithStreamingResponse(self)

    def list(
        self,
        customer_id: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get Correlated User Info by CUSTOMER_ID</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}/correlated-users",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncCorrelatedUsersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCorrelatedUsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCorrelatedUsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCorrelatedUsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCorrelatedUsersResourceWithStreamingResponse(self)

    async def list(
        self,
        customer_id: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get Correlated User Info by CUSTOMER_ID</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}/correlated-users",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class CorrelatedUsersResourceWithRawResponse:
    def __init__(self, correlated_users: CorrelatedUsersResource) -> None:
        self._correlated_users = correlated_users

        self.list = to_custom_raw_response_wrapper(
            correlated_users.list,
            BinaryAPIResponse,
        )


class AsyncCorrelatedUsersResourceWithRawResponse:
    def __init__(self, correlated_users: AsyncCorrelatedUsersResource) -> None:
        self._correlated_users = correlated_users

        self.list = async_to_custom_raw_response_wrapper(
            correlated_users.list,
            AsyncBinaryAPIResponse,
        )


class CorrelatedUsersResourceWithStreamingResponse:
    def __init__(self, correlated_users: CorrelatedUsersResource) -> None:
        self._correlated_users = correlated_users

        self.list = to_custom_streamed_response_wrapper(
            correlated_users.list,
            StreamedBinaryAPIResponse,
        )


class AsyncCorrelatedUsersResourceWithStreamingResponse:
    def __init__(self, correlated_users: AsyncCorrelatedUsersResource) -> None:
        self._correlated_users = correlated_users

        self.list = async_to_custom_streamed_response_wrapper(
            correlated_users.list,
            AsyncStreamedBinaryAPIResponse,
        )
