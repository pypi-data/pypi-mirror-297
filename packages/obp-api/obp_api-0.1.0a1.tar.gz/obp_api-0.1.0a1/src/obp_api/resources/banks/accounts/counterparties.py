# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.banks.accounts import counterparty_create_params

__all__ = ["CounterpartiesResource", "AsyncCounterpartiesResource"]


class CounterpartiesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CounterpartiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CounterpartiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CounterpartiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CounterpartiesResourceWithStreamingResponse(self)

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
        """<p>Create Counterparty for any Account.

        (Explicit)</p><p>In OBP, there are two types of Counterparty.</p><ul><li><p>Explicit Counterparties (those here) which we create explicitly and are used in COUNTERPARTY Transaction Requests</p></li><li><p>Implicit Counterparties (AKA Other Accounts) which are generated automatically from the other sides of Transactions.</p></li></ul><p>Explicit Counterparties are created for the account / view<br />They are how the user of the view (e.g. account owner) refers to the other side of the transaction</p><p>name : the human readable name (e.g. Piano teacher, Miss Nipa)</p><p>description : the human readable name (e.g. Piano teacher, Miss Nipa)</p><p>currency : counterparty account currency (e.g. EUR, GBP, USD, ...)</p><p>bank_routing_scheme : eg: bankId or bankCode or any other strings</p><p>bank_routing_address : eg: <code>gh.29.uk</code>, must be valid sandbox bankIds</p><p>account_routing_scheme : eg: AccountId or AccountNumber or any other strings</p><p>account_routing_address : eg: <code>1d65db7c-a7b2-4839-af41-95</code>, must be valid accountIds</p><p>other_account_secondary_routing_scheme : eg: IBAN or any other strings</p><p>other_account_secondary_routing_address : if it is an IBAN, it should be unique for each counterparty.</p><p>other_branch_routing_scheme : eg: branchId or any other strings or you can leave it empty, not useful in sandbox mode.</p><p>other_branch_routing_address : eg: <code>branch-id-123</code> or you can leave it empty, not useful in sandbox mode.</p><p>is_beneficiary : must be set to <code>true</code> in order to send payments to this counterparty</p><p>bespoke: It supports a list of key-value, you can add it to the counterparty.</p><p>bespoke.key : any info-key you want to add to this counterparty</p><p>bespoke.value : any info-value you want to add to this counterparty</p><p>The view specified by VIEW_ID must have the canAddCounterparty permission</p><p>A minimal example for TransactionRequestType == COUNTERPARTY<br />{<br />&quot;name&quot;: &quot;Tesobe1&quot;,<br />&quot;description&quot;: &quot;Good Company&quot;,<br />&quot;currency&quot;: &quot;EUR&quot;,<br />&quot;other_bank_routing_scheme&quot;: &quot;OBP&quot;,<br />&quot;other_bank_routing_address&quot;: &quot;gh.29.uk&quot;,<br />&quot;other_account_routing_scheme&quot;: &quot;OBP&quot;,<br />&quot;other_account_routing_address&quot;: &quot;8ca8a7e4-6d02-48e3-a029-0b2bf89de9f0&quot;,<br />&quot;is_beneficiary&quot;: true,<br />&quot;other_account_secondary_routing_scheme&quot;: &quot;&quot;,<br />&quot;other_account_secondary_routing_address&quot;: &quot;&quot;,<br />&quot;other_branch_routing_scheme&quot;: &quot;&quot;,<br />&quot;other_branch_routing_address&quot;: &quot;&quot;,<br />&quot;bespoke&quot;: []<br />}</p><p>A minimal example for TransactionRequestType == SEPA</p><p>{<br />&quot;name&quot;: &quot;Tesobe2&quot;,<br />&quot;description&quot;: &quot;Good Company&quot;,<br />&quot;currency&quot;: &quot;EUR&quot;,<br />&quot;other_bank_routing_scheme&quot;: &quot;OBP&quot;,<br />&quot;other_bank_routing_address&quot;: &quot;gh.29.uk&quot;,<br />&quot;other_account_routing_scheme&quot;: &quot;OBP&quot;,<br />&quot;other_account_routing_address&quot;: &quot;8ca8a7e4-6d02-48e3-a029-0b2bf89de9f0&quot;,<br />&quot;other_account_secondary_routing_scheme&quot;: &quot;IBAN&quot;,<br />&quot;other_account_secondary_routing_address&quot;: &quot;DE89 3704 0044 0532 0130 00&quot;,<br />&quot;is_beneficiary&quot;: true,<br />&quot;other_branch_routing_scheme&quot;: &quot;&quot;,<br />&quot;other_branch_routing_address&quot;: &quot;&quot;,<br />&quot;bespoke&quot;: []<br />}</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/{view_id}/counterparties",
            body=maybe_transform(body, counterparty_create_params.CounterpartyCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def retrieve(
        self,
        counterparty_id: str,
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
        <p>Authentication is Mandatory</p>

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
        if not counterparty_id:
            raise ValueError(f"Expected a non-empty value for `counterparty_id` but received {counterparty_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/{view_id}/counterparties/{counterparty_id}",
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
        <p>Get the Counterparties (Explicit) for any account .</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/{view_id}/counterparties",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        counterparty_id: str,
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
    ) -> None:
        """
        <p>Delete Counterparty (Explicit) for any account<br />and also delete the Metadata for its counterparty.</p><p>Authentication is Mandatory</p>

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
        if not counterparty_id:
            raise ValueError(f"Expected a non-empty value for `counterparty_id` but received {counterparty_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/{view_id}/counterparties/{counterparty_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncCounterpartiesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCounterpartiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCounterpartiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCounterpartiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCounterpartiesResourceWithStreamingResponse(self)

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
        """<p>Create Counterparty for any Account.

        (Explicit)</p><p>In OBP, there are two types of Counterparty.</p><ul><li><p>Explicit Counterparties (those here) which we create explicitly and are used in COUNTERPARTY Transaction Requests</p></li><li><p>Implicit Counterparties (AKA Other Accounts) which are generated automatically from the other sides of Transactions.</p></li></ul><p>Explicit Counterparties are created for the account / view<br />They are how the user of the view (e.g. account owner) refers to the other side of the transaction</p><p>name : the human readable name (e.g. Piano teacher, Miss Nipa)</p><p>description : the human readable name (e.g. Piano teacher, Miss Nipa)</p><p>currency : counterparty account currency (e.g. EUR, GBP, USD, ...)</p><p>bank_routing_scheme : eg: bankId or bankCode or any other strings</p><p>bank_routing_address : eg: <code>gh.29.uk</code>, must be valid sandbox bankIds</p><p>account_routing_scheme : eg: AccountId or AccountNumber or any other strings</p><p>account_routing_address : eg: <code>1d65db7c-a7b2-4839-af41-95</code>, must be valid accountIds</p><p>other_account_secondary_routing_scheme : eg: IBAN or any other strings</p><p>other_account_secondary_routing_address : if it is an IBAN, it should be unique for each counterparty.</p><p>other_branch_routing_scheme : eg: branchId or any other strings or you can leave it empty, not useful in sandbox mode.</p><p>other_branch_routing_address : eg: <code>branch-id-123</code> or you can leave it empty, not useful in sandbox mode.</p><p>is_beneficiary : must be set to <code>true</code> in order to send payments to this counterparty</p><p>bespoke: It supports a list of key-value, you can add it to the counterparty.</p><p>bespoke.key : any info-key you want to add to this counterparty</p><p>bespoke.value : any info-value you want to add to this counterparty</p><p>The view specified by VIEW_ID must have the canAddCounterparty permission</p><p>A minimal example for TransactionRequestType == COUNTERPARTY<br />{<br />&quot;name&quot;: &quot;Tesobe1&quot;,<br />&quot;description&quot;: &quot;Good Company&quot;,<br />&quot;currency&quot;: &quot;EUR&quot;,<br />&quot;other_bank_routing_scheme&quot;: &quot;OBP&quot;,<br />&quot;other_bank_routing_address&quot;: &quot;gh.29.uk&quot;,<br />&quot;other_account_routing_scheme&quot;: &quot;OBP&quot;,<br />&quot;other_account_routing_address&quot;: &quot;8ca8a7e4-6d02-48e3-a029-0b2bf89de9f0&quot;,<br />&quot;is_beneficiary&quot;: true,<br />&quot;other_account_secondary_routing_scheme&quot;: &quot;&quot;,<br />&quot;other_account_secondary_routing_address&quot;: &quot;&quot;,<br />&quot;other_branch_routing_scheme&quot;: &quot;&quot;,<br />&quot;other_branch_routing_address&quot;: &quot;&quot;,<br />&quot;bespoke&quot;: []<br />}</p><p>A minimal example for TransactionRequestType == SEPA</p><p>{<br />&quot;name&quot;: &quot;Tesobe2&quot;,<br />&quot;description&quot;: &quot;Good Company&quot;,<br />&quot;currency&quot;: &quot;EUR&quot;,<br />&quot;other_bank_routing_scheme&quot;: &quot;OBP&quot;,<br />&quot;other_bank_routing_address&quot;: &quot;gh.29.uk&quot;,<br />&quot;other_account_routing_scheme&quot;: &quot;OBP&quot;,<br />&quot;other_account_routing_address&quot;: &quot;8ca8a7e4-6d02-48e3-a029-0b2bf89de9f0&quot;,<br />&quot;other_account_secondary_routing_scheme&quot;: &quot;IBAN&quot;,<br />&quot;other_account_secondary_routing_address&quot;: &quot;DE89 3704 0044 0532 0130 00&quot;,<br />&quot;is_beneficiary&quot;: true,<br />&quot;other_branch_routing_scheme&quot;: &quot;&quot;,<br />&quot;other_branch_routing_address&quot;: &quot;&quot;,<br />&quot;bespoke&quot;: []<br />}</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/{view_id}/counterparties",
            body=await async_maybe_transform(body, counterparty_create_params.CounterpartyCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def retrieve(
        self,
        counterparty_id: str,
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
        <p>Authentication is Mandatory</p>

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
        if not counterparty_id:
            raise ValueError(f"Expected a non-empty value for `counterparty_id` but received {counterparty_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/{view_id}/counterparties/{counterparty_id}",
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
        <p>Get the Counterparties (Explicit) for any account .</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/{view_id}/counterparties",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        counterparty_id: str,
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
    ) -> None:
        """
        <p>Delete Counterparty (Explicit) for any account<br />and also delete the Metadata for its counterparty.</p><p>Authentication is Mandatory</p>

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
        if not counterparty_id:
            raise ValueError(f"Expected a non-empty value for `counterparty_id` but received {counterparty_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/{view_id}/counterparties/{counterparty_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class CounterpartiesResourceWithRawResponse:
    def __init__(self, counterparties: CounterpartiesResource) -> None:
        self._counterparties = counterparties

        self.create = to_custom_raw_response_wrapper(
            counterparties.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            counterparties.retrieve,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            counterparties.list,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            counterparties.delete,
        )


class AsyncCounterpartiesResourceWithRawResponse:
    def __init__(self, counterparties: AsyncCounterpartiesResource) -> None:
        self._counterparties = counterparties

        self.create = async_to_custom_raw_response_wrapper(
            counterparties.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            counterparties.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            counterparties.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            counterparties.delete,
        )


class CounterpartiesResourceWithStreamingResponse:
    def __init__(self, counterparties: CounterpartiesResource) -> None:
        self._counterparties = counterparties

        self.create = to_custom_streamed_response_wrapper(
            counterparties.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            counterparties.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            counterparties.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            counterparties.delete,
        )


class AsyncCounterpartiesResourceWithStreamingResponse:
    def __init__(self, counterparties: AsyncCounterpartiesResource) -> None:
        self._counterparties = counterparties

        self.create = async_to_custom_streamed_response_wrapper(
            counterparties.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            counterparties.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            counterparties.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            counterparties.delete,
        )
