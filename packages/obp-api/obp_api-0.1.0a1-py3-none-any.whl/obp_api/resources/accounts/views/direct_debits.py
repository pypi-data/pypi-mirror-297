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
from ....types.accounts.views import direct_debit_create_params

__all__ = ["DirectDebitsResource", "AsyncDirectDebitsResource"]


class DirectDebitsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DirectDebitsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return DirectDebitsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DirectDebitsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return DirectDebitsResourceWithStreamingResponse(self)

    def create(
        self,
        view_id: str,
        *,
        bank_id: str,
        account_id: str,
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
        if not view_id:
            raise ValueError(f"Expected a non-empty value for `view_id` but received {view_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/direct-debit",
            body=maybe_transform(body, direct_debit_create_params.DirectDebitCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncDirectDebitsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDirectDebitsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDirectDebitsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDirectDebitsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncDirectDebitsResourceWithStreamingResponse(self)

    async def create(
        self,
        view_id: str,
        *,
        bank_id: str,
        account_id: str,
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
        if not view_id:
            raise ValueError(f"Expected a non-empty value for `view_id` but received {view_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/direct-debit",
            body=await async_maybe_transform(body, direct_debit_create_params.DirectDebitCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class DirectDebitsResourceWithRawResponse:
    def __init__(self, direct_debits: DirectDebitsResource) -> None:
        self._direct_debits = direct_debits

        self.create = to_custom_raw_response_wrapper(
            direct_debits.create,
            BinaryAPIResponse,
        )


class AsyncDirectDebitsResourceWithRawResponse:
    def __init__(self, direct_debits: AsyncDirectDebitsResource) -> None:
        self._direct_debits = direct_debits

        self.create = async_to_custom_raw_response_wrapper(
            direct_debits.create,
            AsyncBinaryAPIResponse,
        )


class DirectDebitsResourceWithStreamingResponse:
    def __init__(self, direct_debits: DirectDebitsResource) -> None:
        self._direct_debits = direct_debits

        self.create = to_custom_streamed_response_wrapper(
            direct_debits.create,
            StreamedBinaryAPIResponse,
        )


class AsyncDirectDebitsResourceWithStreamingResponse:
    def __init__(self, direct_debits: AsyncDirectDebitsResource) -> None:
        self._direct_debits = direct_debits

        self.create = async_to_custom_streamed_response_wrapper(
            direct_debits.create,
            AsyncStreamedBinaryAPIResponse,
        )
