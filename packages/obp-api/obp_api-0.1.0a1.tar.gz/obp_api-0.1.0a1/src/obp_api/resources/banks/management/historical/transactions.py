# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.banks.management.historical import transaction_create_params

__all__ = ["TransactionsResource", "AsyncTransactionsResource"]


class TransactionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TransactionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return TransactionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TransactionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return TransactionsResourceWithStreamingResponse(self)

    def create(
        self,
        bank_id: str,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Create historical transactions at one Bank</p><p>Use this endpoint to create transactions between any two accounts at the same bank.<br />From account and to account must be at the same bank.<br />Example:<br />{<br />&quot;from_account_id&quot;: &quot;1ca8a7e4-6d02-48e3-a029-0b2bf89de9f0&quot;,<br />&quot;to_account_id&quot;: &quot;2ca8a7e4-6d02-48e3-a029-0b2bf89de9f0&quot;,<br />&quot;value&quot;: {<br />&quot;currency&quot;: &quot;GBP&quot;,<br />&quot;amount&quot;: &quot;10&quot;<br />},<br />&quot;description&quot;: &quot;this is for work&quot;,<br />&quot;posted&quot;: &quot;2017-09-19T02:31:05Z&quot;,<br />&quot;completed&quot;: &quot;2017-09-19T02:31:05Z&quot;,<br />&quot;type&quot;: &quot;SANDBOX_TAN&quot;,<br />&quot;charge_policy&quot;: &quot;SHARED&quot;<br />}</p><p>This call is experimental.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/management/historical/transactions",
            body=maybe_transform(body, transaction_create_params.TransactionCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncTransactionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTransactionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTransactionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTransactionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncTransactionsResourceWithStreamingResponse(self)

    async def create(
        self,
        bank_id: str,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Create historical transactions at one Bank</p><p>Use this endpoint to create transactions between any two accounts at the same bank.<br />From account and to account must be at the same bank.<br />Example:<br />{<br />&quot;from_account_id&quot;: &quot;1ca8a7e4-6d02-48e3-a029-0b2bf89de9f0&quot;,<br />&quot;to_account_id&quot;: &quot;2ca8a7e4-6d02-48e3-a029-0b2bf89de9f0&quot;,<br />&quot;value&quot;: {<br />&quot;currency&quot;: &quot;GBP&quot;,<br />&quot;amount&quot;: &quot;10&quot;<br />},<br />&quot;description&quot;: &quot;this is for work&quot;,<br />&quot;posted&quot;: &quot;2017-09-19T02:31:05Z&quot;,<br />&quot;completed&quot;: &quot;2017-09-19T02:31:05Z&quot;,<br />&quot;type&quot;: &quot;SANDBOX_TAN&quot;,<br />&quot;charge_policy&quot;: &quot;SHARED&quot;<br />}</p><p>This call is experimental.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/management/historical/transactions",
            body=await async_maybe_transform(body, transaction_create_params.TransactionCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class TransactionsResourceWithRawResponse:
    def __init__(self, transactions: TransactionsResource) -> None:
        self._transactions = transactions

        self.create = to_custom_raw_response_wrapper(
            transactions.create,
            BinaryAPIResponse,
        )


class AsyncTransactionsResourceWithRawResponse:
    def __init__(self, transactions: AsyncTransactionsResource) -> None:
        self._transactions = transactions

        self.create = async_to_custom_raw_response_wrapper(
            transactions.create,
            AsyncBinaryAPIResponse,
        )


class TransactionsResourceWithStreamingResponse:
    def __init__(self, transactions: TransactionsResource) -> None:
        self._transactions = transactions

        self.create = to_custom_streamed_response_wrapper(
            transactions.create,
            StreamedBinaryAPIResponse,
        )


class AsyncTransactionsResourceWithStreamingResponse:
    def __init__(self, transactions: AsyncTransactionsResource) -> None:
        self._transactions = transactions

        self.create = async_to_custom_streamed_response_wrapper(
            transactions.create,
            AsyncStreamedBinaryAPIResponse,
        )
