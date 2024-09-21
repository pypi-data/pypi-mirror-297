# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
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
from ...types.management import account_account_routing_query_params, account_account_routing_regex_query_params

__all__ = ["AccountsResource", "AsyncAccountsResource"]


class AccountsResource(SyncAPIResource):
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

    def account_routing_query(
        self,
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
        <p>This endpoint returns the account (if it exists) linked with the provided scheme and address.</p><p>The <code>bank_id</code> field is optional, but if it's not provided, we don't guarantee that the returned account is unique across all the banks.</p><p>Example of account routing scheme: <code>IBAN</code>, &quot;OBP&quot;, &quot;AccountNumber&quot;, ...<br />Example of account routing address: <code>DE17500105178275645584</code>, &quot;321774cc-fccd-11ea-adc1-0242ac120002&quot;, &quot;55897106215&quot;, ...</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/management/accounts/account-routing-query",
            body=maybe_transform(body, account_account_routing_query_params.AccountAccountRoutingQueryParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def account_routing_regex_query(
        self,
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
        <p>This endpoint returns an array of accounts matching the provided routing scheme and the routing address regex.</p><p>The <code>bank_id</code> field is optional.</p><p>Example of account routing scheme: <code>IBAN</code>, <code>OBP</code>, <code>AccountNumber</code>, ...<br />Example of account routing address regex: <code>DE175.*</code>, <code>55897106215-[A-Z]{3}</code>, ...</p><p>This endpoint can be used to retrieve multiples accounts matching a same account routing address pattern.<br />For example, if you want to link multiple accounts having different currencies, you can create an account<br />with <code>123456789-EUR</code> as Account Number and an other account with <code>123456789-USD</code> as Account Number.<br />So we can identify the Account Number as <code>123456789</code>, so to get all the accounts with the same account number<br />and the different currencies, we can use this body in the request :</p><pre><code>{   &quot;bank_id&quot;: &quot;BANK_ID&quot;,   &quot;account_routing&quot;: {       &quot;scheme&quot;: &quot;AccountNumber&quot;,       &quot;address&quot;: &quot;123456789-[A-Z]{3}&quot;   }}</code></pre><p>This request will returns the accounts matching the routing address regex (<code>123456789-EUR</code> and <code>123456789-USD</code>).</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/management/accounts/account-routing-regex-query",
            body=maybe_transform(
                body, account_account_routing_regex_query_params.AccountAccountRoutingRegexQueryParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAccountsResource(AsyncAPIResource):
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

    async def account_routing_query(
        self,
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
        <p>This endpoint returns the account (if it exists) linked with the provided scheme and address.</p><p>The <code>bank_id</code> field is optional, but if it's not provided, we don't guarantee that the returned account is unique across all the banks.</p><p>Example of account routing scheme: <code>IBAN</code>, &quot;OBP&quot;, &quot;AccountNumber&quot;, ...<br />Example of account routing address: <code>DE17500105178275645584</code>, &quot;321774cc-fccd-11ea-adc1-0242ac120002&quot;, &quot;55897106215&quot;, ...</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/management/accounts/account-routing-query",
            body=await async_maybe_transform(
                body, account_account_routing_query_params.AccountAccountRoutingQueryParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def account_routing_regex_query(
        self,
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
        <p>This endpoint returns an array of accounts matching the provided routing scheme and the routing address regex.</p><p>The <code>bank_id</code> field is optional.</p><p>Example of account routing scheme: <code>IBAN</code>, <code>OBP</code>, <code>AccountNumber</code>, ...<br />Example of account routing address regex: <code>DE175.*</code>, <code>55897106215-[A-Z]{3}</code>, ...</p><p>This endpoint can be used to retrieve multiples accounts matching a same account routing address pattern.<br />For example, if you want to link multiple accounts having different currencies, you can create an account<br />with <code>123456789-EUR</code> as Account Number and an other account with <code>123456789-USD</code> as Account Number.<br />So we can identify the Account Number as <code>123456789</code>, so to get all the accounts with the same account number<br />and the different currencies, we can use this body in the request :</p><pre><code>{   &quot;bank_id&quot;: &quot;BANK_ID&quot;,   &quot;account_routing&quot;: {       &quot;scheme&quot;: &quot;AccountNumber&quot;,       &quot;address&quot;: &quot;123456789-[A-Z]{3}&quot;   }}</code></pre><p>This request will returns the accounts matching the routing address regex (<code>123456789-EUR</code> and <code>123456789-USD</code>).</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/management/accounts/account-routing-regex-query",
            body=await async_maybe_transform(
                body, account_account_routing_regex_query_params.AccountAccountRoutingRegexQueryParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class AccountsResourceWithRawResponse:
    def __init__(self, accounts: AccountsResource) -> None:
        self._accounts = accounts

        self.account_routing_query = to_custom_raw_response_wrapper(
            accounts.account_routing_query,
            BinaryAPIResponse,
        )
        self.account_routing_regex_query = to_custom_raw_response_wrapper(
            accounts.account_routing_regex_query,
            BinaryAPIResponse,
        )


class AsyncAccountsResourceWithRawResponse:
    def __init__(self, accounts: AsyncAccountsResource) -> None:
        self._accounts = accounts

        self.account_routing_query = async_to_custom_raw_response_wrapper(
            accounts.account_routing_query,
            AsyncBinaryAPIResponse,
        )
        self.account_routing_regex_query = async_to_custom_raw_response_wrapper(
            accounts.account_routing_regex_query,
            AsyncBinaryAPIResponse,
        )


class AccountsResourceWithStreamingResponse:
    def __init__(self, accounts: AccountsResource) -> None:
        self._accounts = accounts

        self.account_routing_query = to_custom_streamed_response_wrapper(
            accounts.account_routing_query,
            StreamedBinaryAPIResponse,
        )
        self.account_routing_regex_query = to_custom_streamed_response_wrapper(
            accounts.account_routing_regex_query,
            StreamedBinaryAPIResponse,
        )


class AsyncAccountsResourceWithStreamingResponse:
    def __init__(self, accounts: AsyncAccountsResource) -> None:
        self._accounts = accounts

        self.account_routing_query = async_to_custom_streamed_response_wrapper(
            accounts.account_routing_query,
            AsyncStreamedBinaryAPIResponse,
        )
        self.account_routing_regex_query = async_to_custom_streamed_response_wrapper(
            accounts.account_routing_regex_query,
            AsyncStreamedBinaryAPIResponse,
        )
