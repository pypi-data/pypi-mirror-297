# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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

__all__ = ["TransactionRequestsResource", "AsyncTransactionRequestsResource"]


class TransactionRequestsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TransactionRequestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return TransactionRequestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TransactionRequestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return TransactionRequestsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        transaction_request_id: str,
        *,
        bank_id: str,
        account_id: str,
        view_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Returns transaction request for transaction specified by TRANSACTION_REQUEST_ID and for account specified by ACCOUNT_ID at bank specified by BANK_ID.</p><p>The VIEW_ID specified must be 'owner' and the user must have access to this view.</p><p>Version 2.0.0 now returns charge information.</p><p>Transaction Requests serve to initiate transactions that may or may not proceed. They contain information including:</p><ul><li>Transaction Request Id</li><li>Type</li><li>Status (INITIATED, COMPLETED)</li><li>Challenge (in order to confirm the request)</li><li>From Bank / Account</li><li>Details including Currency, Value, Description and other initiation information specific to each type. (Could potentialy include a list of future transactions.)</li><li>Related Transactions</li></ul><p>PSD2 Context: PSD2 requires transparency of charges to the customer.<br />This endpoint provides the charge that would be applied if the Transaction Request proceeds - and a record of that charge there after.<br />The customer can proceed with the Transaction by answering the security challenge.</p><p>Authentication is Mandatory</p>

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
        if not transaction_request_id:
            raise ValueError(
                f"Expected a non-empty value for `transaction_request_id` but received {transaction_request_id!r}"
            )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/transaction-requests/{transaction_request_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
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
        <p>Returns transaction requests for account specified by ACCOUNT_ID at bank specified by BANK_ID.</p><p>The VIEW_ID specified must be 'owner' and the user must have access to this view.</p><p>Version 2.0.0 now returns charge information.</p><p>Transaction Requests serve to initiate transactions that may or may not proceed. They contain information including:</p><ul><li>Transaction Request Id</li><li>Type</li><li>Status (INITIATED, COMPLETED)</li><li>Challenge (in order to confirm the request)</li><li>From Bank / Account</li><li>Details including Currency, Value, Description and other initiation information specific to each type. (Could potentialy include a list of future transactions.)</li><li>Related Transactions</li></ul><p>PSD2 Context: PSD2 requires transparency of charges to the customer.<br />This endpoint provides the charge that would be applied if the Transaction Request proceeds - and a record of that charge there after.<br />The customer can proceed with the Transaction by answering the security challenge.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/transaction-requests",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncTransactionRequestsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTransactionRequestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTransactionRequestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTransactionRequestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncTransactionRequestsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        transaction_request_id: str,
        *,
        bank_id: str,
        account_id: str,
        view_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Returns transaction request for transaction specified by TRANSACTION_REQUEST_ID and for account specified by ACCOUNT_ID at bank specified by BANK_ID.</p><p>The VIEW_ID specified must be 'owner' and the user must have access to this view.</p><p>Version 2.0.0 now returns charge information.</p><p>Transaction Requests serve to initiate transactions that may or may not proceed. They contain information including:</p><ul><li>Transaction Request Id</li><li>Type</li><li>Status (INITIATED, COMPLETED)</li><li>Challenge (in order to confirm the request)</li><li>From Bank / Account</li><li>Details including Currency, Value, Description and other initiation information specific to each type. (Could potentialy include a list of future transactions.)</li><li>Related Transactions</li></ul><p>PSD2 Context: PSD2 requires transparency of charges to the customer.<br />This endpoint provides the charge that would be applied if the Transaction Request proceeds - and a record of that charge there after.<br />The customer can proceed with the Transaction by answering the security challenge.</p><p>Authentication is Mandatory</p>

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
        if not transaction_request_id:
            raise ValueError(
                f"Expected a non-empty value for `transaction_request_id` but received {transaction_request_id!r}"
            )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/transaction-requests/{transaction_request_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
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
        <p>Returns transaction requests for account specified by ACCOUNT_ID at bank specified by BANK_ID.</p><p>The VIEW_ID specified must be 'owner' and the user must have access to this view.</p><p>Version 2.0.0 now returns charge information.</p><p>Transaction Requests serve to initiate transactions that may or may not proceed. They contain information including:</p><ul><li>Transaction Request Id</li><li>Type</li><li>Status (INITIATED, COMPLETED)</li><li>Challenge (in order to confirm the request)</li><li>From Bank / Account</li><li>Details including Currency, Value, Description and other initiation information specific to each type. (Could potentialy include a list of future transactions.)</li><li>Related Transactions</li></ul><p>PSD2 Context: PSD2 requires transparency of charges to the customer.<br />This endpoint provides the charge that would be applied if the Transaction Request proceeds - and a record of that charge there after.<br />The customer can proceed with the Transaction by answering the security challenge.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/transaction-requests",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class TransactionRequestsResourceWithRawResponse:
    def __init__(self, transaction_requests: TransactionRequestsResource) -> None:
        self._transaction_requests = transaction_requests

        self.retrieve = to_custom_raw_response_wrapper(
            transaction_requests.retrieve,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            transaction_requests.list,
            BinaryAPIResponse,
        )


class AsyncTransactionRequestsResourceWithRawResponse:
    def __init__(self, transaction_requests: AsyncTransactionRequestsResource) -> None:
        self._transaction_requests = transaction_requests

        self.retrieve = async_to_custom_raw_response_wrapper(
            transaction_requests.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            transaction_requests.list,
            AsyncBinaryAPIResponse,
        )


class TransactionRequestsResourceWithStreamingResponse:
    def __init__(self, transaction_requests: TransactionRequestsResource) -> None:
        self._transaction_requests = transaction_requests

        self.retrieve = to_custom_streamed_response_wrapper(
            transaction_requests.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            transaction_requests.list,
            StreamedBinaryAPIResponse,
        )


class AsyncTransactionRequestsResourceWithStreamingResponse:
    def __init__(self, transaction_requests: AsyncTransactionRequestsResource) -> None:
        self._transaction_requests = transaction_requests

        self.retrieve = async_to_custom_streamed_response_wrapper(
            transaction_requests.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            transaction_requests.list,
            AsyncStreamedBinaryAPIResponse,
        )
