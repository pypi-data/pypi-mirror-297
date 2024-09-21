# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .views import (
    ViewsResource,
    AsyncViewsResource,
    ViewsResourceWithRawResponse,
    AsyncViewsResourceWithRawResponse,
    ViewsResourceWithStreamingResponse,
    AsyncViewsResourceWithStreamingResponse,
)
from .account import (
    AccountResource,
    AsyncAccountResource,
    AccountResourceWithRawResponse,
    AsyncAccountResourceWithRawResponse,
    AccountResourceWithStreamingResponse,
    AsyncAccountResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from .views.views import ViewsResource, AsyncViewsResource
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
from .direct_debit import (
    DirectDebitResource,
    AsyncDirectDebitResource,
    DirectDebitResourceWithRawResponse,
    AsyncDirectDebitResourceWithRawResponse,
    DirectDebitResourceWithStreamingResponse,
    AsyncDirectDebitResourceWithStreamingResponse,
)
from .transactions import (
    TransactionsResource,
    AsyncTransactionsResource,
    TransactionsResourceWithRawResponse,
    AsyncTransactionsResourceWithRawResponse,
    TransactionsResourceWithStreamingResponse,
    AsyncTransactionsResourceWithStreamingResponse,
)
from ....types.banks import account_update_params
from .counterparties import (
    CounterpartiesResource,
    AsyncCounterpartiesResource,
    CounterpartiesResourceWithRawResponse,
    AsyncCounterpartiesResourceWithRawResponse,
    CounterpartiesResourceWithStreamingResponse,
    AsyncCounterpartiesResourceWithStreamingResponse,
)
from .other_accounts import (
    OtherAccountsResource,
    AsyncOtherAccountsResource,
    OtherAccountsResourceWithRawResponse,
    AsyncOtherAccountsResourceWithRawResponse,
    OtherAccountsResourceWithStreamingResponse,
    AsyncOtherAccountsResourceWithStreamingResponse,
)
from .standing_order import (
    StandingOrderResource,
    AsyncStandingOrderResource,
    StandingOrderResourceWithRawResponse,
    AsyncStandingOrderResourceWithRawResponse,
    StandingOrderResourceWithStreamingResponse,
    AsyncStandingOrderResourceWithStreamingResponse,
)
from ...._base_client import make_request_options
from .counterparty_names import (
    CounterpartyNamesResource,
    AsyncCounterpartyNamesResource,
    CounterpartyNamesResourceWithRawResponse,
    AsyncCounterpartyNamesResourceWithRawResponse,
    CounterpartyNamesResourceWithStreamingResponse,
    AsyncCounterpartyNamesResourceWithStreamingResponse,
)
from .transaction_requests import (
    TransactionRequestsResource,
    AsyncTransactionRequestsResource,
    TransactionRequestsResourceWithRawResponse,
    AsyncTransactionRequestsResourceWithRawResponse,
    TransactionRequestsResourceWithStreamingResponse,
    AsyncTransactionRequestsResourceWithStreamingResponse,
)
from .transaction_request_types import (
    TransactionRequestTypesResource,
    AsyncTransactionRequestTypesResource,
    TransactionRequestTypesResourceWithRawResponse,
    AsyncTransactionRequestTypesResourceWithRawResponse,
    TransactionRequestTypesResourceWithStreamingResponse,
    AsyncTransactionRequestTypesResourceWithStreamingResponse,
)
from .transactions.transactions import TransactionsResource, AsyncTransactionsResource
from .other_accounts.other_accounts import OtherAccountsResource, AsyncOtherAccountsResource

__all__ = ["AccountsResource", "AsyncAccountsResource"]


class AccountsResource(SyncAPIResource):
    @cached_property
    def other_accounts(self) -> OtherAccountsResource:
        return OtherAccountsResource(self._client)

    @cached_property
    def standing_order(self) -> StandingOrderResource:
        return StandingOrderResource(self._client)

    @cached_property
    def transaction_request_types(self) -> TransactionRequestTypesResource:
        return TransactionRequestTypesResource(self._client)

    @cached_property
    def transaction_requests(self) -> TransactionRequestsResource:
        return TransactionRequestsResource(self._client)

    @cached_property
    def views(self) -> ViewsResource:
        return ViewsResource(self._client)

    @cached_property
    def transactions(self) -> TransactionsResource:
        return TransactionsResource(self._client)

    @cached_property
    def counterparties(self) -> CounterpartiesResource:
        return CounterpartiesResource(self._client)

    @cached_property
    def counterparty_names(self) -> CounterpartyNamesResource:
        return CounterpartyNamesResource(self._client)

    @cached_property
    def direct_debit(self) -> DirectDebitResource:
        return DirectDebitResource(self._client)

    @cached_property
    def account(self) -> AccountResource:
        return AccountResource(self._client)

    @cached_property
    def with_raw_response(self) -> AccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AccountsResourceWithStreamingResponse(self)

    def update(
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
        <p>Update the account.</p><p>Authentication is Mandatory</p>

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
        return self._put(
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}",
            body=maybe_transform(body, account_update_params.AccountUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Returns the list of accounts at BANK_ID that the user has access to.<br />For each account the API returns the account ID and the views available to the user..<br />Each account must have at least one private View.</p><p>optional request parameters for filter with attributes<br />URL params example: /banks/some-bank-id/accounts?manager=John&amp;count=8</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAccountsResource(AsyncAPIResource):
    @cached_property
    def other_accounts(self) -> AsyncOtherAccountsResource:
        return AsyncOtherAccountsResource(self._client)

    @cached_property
    def standing_order(self) -> AsyncStandingOrderResource:
        return AsyncStandingOrderResource(self._client)

    @cached_property
    def transaction_request_types(self) -> AsyncTransactionRequestTypesResource:
        return AsyncTransactionRequestTypesResource(self._client)

    @cached_property
    def transaction_requests(self) -> AsyncTransactionRequestsResource:
        return AsyncTransactionRequestsResource(self._client)

    @cached_property
    def views(self) -> AsyncViewsResource:
        return AsyncViewsResource(self._client)

    @cached_property
    def transactions(self) -> AsyncTransactionsResource:
        return AsyncTransactionsResource(self._client)

    @cached_property
    def counterparties(self) -> AsyncCounterpartiesResource:
        return AsyncCounterpartiesResource(self._client)

    @cached_property
    def counterparty_names(self) -> AsyncCounterpartyNamesResource:
        return AsyncCounterpartyNamesResource(self._client)

    @cached_property
    def direct_debit(self) -> AsyncDirectDebitResource:
        return AsyncDirectDebitResource(self._client)

    @cached_property
    def account(self) -> AsyncAccountResource:
        return AsyncAccountResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAccountsResourceWithStreamingResponse(self)

    async def update(
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
        <p>Update the account.</p><p>Authentication is Mandatory</p>

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
        return await self._put(
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}",
            body=await async_maybe_transform(body, account_update_params.AccountUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Returns the list of accounts at BANK_ID that the user has access to.<br />For each account the API returns the account ID and the views available to the user..<br />Each account must have at least one private View.</p><p>optional request parameters for filter with attributes<br />URL params example: /banks/some-bank-id/accounts?manager=John&amp;count=8</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class AccountsResourceWithRawResponse:
    def __init__(self, accounts: AccountsResource) -> None:
        self._accounts = accounts

        self.update = to_custom_raw_response_wrapper(
            accounts.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            accounts.list,
            BinaryAPIResponse,
        )

    @cached_property
    def other_accounts(self) -> OtherAccountsResourceWithRawResponse:
        return OtherAccountsResourceWithRawResponse(self._accounts.other_accounts)

    @cached_property
    def standing_order(self) -> StandingOrderResourceWithRawResponse:
        return StandingOrderResourceWithRawResponse(self._accounts.standing_order)

    @cached_property
    def transaction_request_types(self) -> TransactionRequestTypesResourceWithRawResponse:
        return TransactionRequestTypesResourceWithRawResponse(self._accounts.transaction_request_types)

    @cached_property
    def transaction_requests(self) -> TransactionRequestsResourceWithRawResponse:
        return TransactionRequestsResourceWithRawResponse(self._accounts.transaction_requests)

    @cached_property
    def views(self) -> ViewsResourceWithRawResponse:
        return ViewsResourceWithRawResponse(self._accounts.views)

    @cached_property
    def transactions(self) -> TransactionsResourceWithRawResponse:
        return TransactionsResourceWithRawResponse(self._accounts.transactions)

    @cached_property
    def counterparties(self) -> CounterpartiesResourceWithRawResponse:
        return CounterpartiesResourceWithRawResponse(self._accounts.counterparties)

    @cached_property
    def counterparty_names(self) -> CounterpartyNamesResourceWithRawResponse:
        return CounterpartyNamesResourceWithRawResponse(self._accounts.counterparty_names)

    @cached_property
    def direct_debit(self) -> DirectDebitResourceWithRawResponse:
        return DirectDebitResourceWithRawResponse(self._accounts.direct_debit)

    @cached_property
    def account(self) -> AccountResourceWithRawResponse:
        return AccountResourceWithRawResponse(self._accounts.account)


class AsyncAccountsResourceWithRawResponse:
    def __init__(self, accounts: AsyncAccountsResource) -> None:
        self._accounts = accounts

        self.update = async_to_custom_raw_response_wrapper(
            accounts.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            accounts.list,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def other_accounts(self) -> AsyncOtherAccountsResourceWithRawResponse:
        return AsyncOtherAccountsResourceWithRawResponse(self._accounts.other_accounts)

    @cached_property
    def standing_order(self) -> AsyncStandingOrderResourceWithRawResponse:
        return AsyncStandingOrderResourceWithRawResponse(self._accounts.standing_order)

    @cached_property
    def transaction_request_types(self) -> AsyncTransactionRequestTypesResourceWithRawResponse:
        return AsyncTransactionRequestTypesResourceWithRawResponse(self._accounts.transaction_request_types)

    @cached_property
    def transaction_requests(self) -> AsyncTransactionRequestsResourceWithRawResponse:
        return AsyncTransactionRequestsResourceWithRawResponse(self._accounts.transaction_requests)

    @cached_property
    def views(self) -> AsyncViewsResourceWithRawResponse:
        return AsyncViewsResourceWithRawResponse(self._accounts.views)

    @cached_property
    def transactions(self) -> AsyncTransactionsResourceWithRawResponse:
        return AsyncTransactionsResourceWithRawResponse(self._accounts.transactions)

    @cached_property
    def counterparties(self) -> AsyncCounterpartiesResourceWithRawResponse:
        return AsyncCounterpartiesResourceWithRawResponse(self._accounts.counterparties)

    @cached_property
    def counterparty_names(self) -> AsyncCounterpartyNamesResourceWithRawResponse:
        return AsyncCounterpartyNamesResourceWithRawResponse(self._accounts.counterparty_names)

    @cached_property
    def direct_debit(self) -> AsyncDirectDebitResourceWithRawResponse:
        return AsyncDirectDebitResourceWithRawResponse(self._accounts.direct_debit)

    @cached_property
    def account(self) -> AsyncAccountResourceWithRawResponse:
        return AsyncAccountResourceWithRawResponse(self._accounts.account)


class AccountsResourceWithStreamingResponse:
    def __init__(self, accounts: AccountsResource) -> None:
        self._accounts = accounts

        self.update = to_custom_streamed_response_wrapper(
            accounts.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            accounts.list,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def other_accounts(self) -> OtherAccountsResourceWithStreamingResponse:
        return OtherAccountsResourceWithStreamingResponse(self._accounts.other_accounts)

    @cached_property
    def standing_order(self) -> StandingOrderResourceWithStreamingResponse:
        return StandingOrderResourceWithStreamingResponse(self._accounts.standing_order)

    @cached_property
    def transaction_request_types(self) -> TransactionRequestTypesResourceWithStreamingResponse:
        return TransactionRequestTypesResourceWithStreamingResponse(self._accounts.transaction_request_types)

    @cached_property
    def transaction_requests(self) -> TransactionRequestsResourceWithStreamingResponse:
        return TransactionRequestsResourceWithStreamingResponse(self._accounts.transaction_requests)

    @cached_property
    def views(self) -> ViewsResourceWithStreamingResponse:
        return ViewsResourceWithStreamingResponse(self._accounts.views)

    @cached_property
    def transactions(self) -> TransactionsResourceWithStreamingResponse:
        return TransactionsResourceWithStreamingResponse(self._accounts.transactions)

    @cached_property
    def counterparties(self) -> CounterpartiesResourceWithStreamingResponse:
        return CounterpartiesResourceWithStreamingResponse(self._accounts.counterparties)

    @cached_property
    def counterparty_names(self) -> CounterpartyNamesResourceWithStreamingResponse:
        return CounterpartyNamesResourceWithStreamingResponse(self._accounts.counterparty_names)

    @cached_property
    def direct_debit(self) -> DirectDebitResourceWithStreamingResponse:
        return DirectDebitResourceWithStreamingResponse(self._accounts.direct_debit)

    @cached_property
    def account(self) -> AccountResourceWithStreamingResponse:
        return AccountResourceWithStreamingResponse(self._accounts.account)


class AsyncAccountsResourceWithStreamingResponse:
    def __init__(self, accounts: AsyncAccountsResource) -> None:
        self._accounts = accounts

        self.update = async_to_custom_streamed_response_wrapper(
            accounts.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            accounts.list,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def other_accounts(self) -> AsyncOtherAccountsResourceWithStreamingResponse:
        return AsyncOtherAccountsResourceWithStreamingResponse(self._accounts.other_accounts)

    @cached_property
    def standing_order(self) -> AsyncStandingOrderResourceWithStreamingResponse:
        return AsyncStandingOrderResourceWithStreamingResponse(self._accounts.standing_order)

    @cached_property
    def transaction_request_types(self) -> AsyncTransactionRequestTypesResourceWithStreamingResponse:
        return AsyncTransactionRequestTypesResourceWithStreamingResponse(self._accounts.transaction_request_types)

    @cached_property
    def transaction_requests(self) -> AsyncTransactionRequestsResourceWithStreamingResponse:
        return AsyncTransactionRequestsResourceWithStreamingResponse(self._accounts.transaction_requests)

    @cached_property
    def views(self) -> AsyncViewsResourceWithStreamingResponse:
        return AsyncViewsResourceWithStreamingResponse(self._accounts.views)

    @cached_property
    def transactions(self) -> AsyncTransactionsResourceWithStreamingResponse:
        return AsyncTransactionsResourceWithStreamingResponse(self._accounts.transactions)

    @cached_property
    def counterparties(self) -> AsyncCounterpartiesResourceWithStreamingResponse:
        return AsyncCounterpartiesResourceWithStreamingResponse(self._accounts.counterparties)

    @cached_property
    def counterparty_names(self) -> AsyncCounterpartyNamesResourceWithStreamingResponse:
        return AsyncCounterpartyNamesResourceWithStreamingResponse(self._accounts.counterparty_names)

    @cached_property
    def direct_debit(self) -> AsyncDirectDebitResourceWithStreamingResponse:
        return AsyncDirectDebitResourceWithStreamingResponse(self._accounts.direct_debit)

    @cached_property
    def account(self) -> AsyncAccountResourceWithStreamingResponse:
        return AsyncAccountResourceWithStreamingResponse(self._accounts.account)
