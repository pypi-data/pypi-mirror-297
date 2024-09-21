# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
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
from ....types.banks.accounts import direct_debit_create_params

__all__ = ["DirectDebitResource", "AsyncDirectDebitResource"]


class DirectDebitResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DirectDebitResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return DirectDebitResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DirectDebitResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return DirectDebitResourceWithStreamingResponse(self)

    def create(
        self,
        account_id: str,
        *,
        bank_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Create direct debit for an account.</p><p>Authentication is Mandatory</p>

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
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/direct-debit",
            body=maybe_transform(body, direct_debit_create_params.DirectDebitCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncDirectDebitResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDirectDebitResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDirectDebitResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDirectDebitResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncDirectDebitResourceWithStreamingResponse(self)

    async def create(
        self,
        account_id: str,
        *,
        bank_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Create direct debit for an account.</p><p>Authentication is Mandatory</p>

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
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/direct-debit",
            body=await async_maybe_transform(body, direct_debit_create_params.DirectDebitCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class DirectDebitResourceWithRawResponse:
    def __init__(self, direct_debit: DirectDebitResource) -> None:
        self._direct_debit = direct_debit

        self.create = to_custom_raw_response_wrapper(
            direct_debit.create,
            BinaryAPIResponse,
        )


class AsyncDirectDebitResourceWithRawResponse:
    def __init__(self, direct_debit: AsyncDirectDebitResource) -> None:
        self._direct_debit = direct_debit

        self.create = async_to_custom_raw_response_wrapper(
            direct_debit.create,
            AsyncBinaryAPIResponse,
        )


class DirectDebitResourceWithStreamingResponse:
    def __init__(self, direct_debit: DirectDebitResource) -> None:
        self._direct_debit = direct_debit

        self.create = to_custom_streamed_response_wrapper(
            direct_debit.create,
            StreamedBinaryAPIResponse,
        )


class AsyncDirectDebitResourceWithStreamingResponse:
    def __init__(self, direct_debit: AsyncDirectDebitResource) -> None:
        self._direct_debit = direct_debit

        self.create = async_to_custom_streamed_response_wrapper(
            direct_debit.create,
            AsyncStreamedBinaryAPIResponse,
        )
