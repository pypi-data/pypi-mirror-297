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

__all__ = ["FundsAvailableResource", "AsyncFundsAvailableResource"]


class FundsAvailableResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FundsAvailableResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return FundsAvailableResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FundsAvailableResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return FundsAvailableResourceWithStreamingResponse(self)

    def retrieve(
        self,
        view_id: str,
        *,
        bank_id: str,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Check Available Funds<br />Mandatory URL parameters:</p><ul><li>amount=NUMBER</li><li>currency=STRING</li></ul><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not view_id:
            raise ValueError(f"Expected a non-empty value for `view_id` but received {view_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/funds-available",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncFundsAvailableResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFundsAvailableResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFundsAvailableResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFundsAvailableResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncFundsAvailableResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        view_id: str,
        *,
        bank_id: str,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Check Available Funds<br />Mandatory URL parameters:</p><ul><li>amount=NUMBER</li><li>currency=STRING</li></ul><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not view_id:
            raise ValueError(f"Expected a non-empty value for `view_id` but received {view_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/funds-available",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class FundsAvailableResourceWithRawResponse:
    def __init__(self, funds_available: FundsAvailableResource) -> None:
        self._funds_available = funds_available

        self.retrieve = to_custom_raw_response_wrapper(
            funds_available.retrieve,
            BinaryAPIResponse,
        )


class AsyncFundsAvailableResourceWithRawResponse:
    def __init__(self, funds_available: AsyncFundsAvailableResource) -> None:
        self._funds_available = funds_available

        self.retrieve = async_to_custom_raw_response_wrapper(
            funds_available.retrieve,
            AsyncBinaryAPIResponse,
        )


class FundsAvailableResourceWithStreamingResponse:
    def __init__(self, funds_available: FundsAvailableResource) -> None:
        self._funds_available = funds_available

        self.retrieve = to_custom_streamed_response_wrapper(
            funds_available.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncFundsAvailableResourceWithStreamingResponse:
    def __init__(self, funds_available: AsyncFundsAvailableResource) -> None:
        self._funds_available = funds_available

        self.retrieve = async_to_custom_streamed_response_wrapper(
            funds_available.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
