# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ....._compat import cached_property
from .transactions import (
    TransactionsResource,
    AsyncTransactionsResource,
    TransactionsResourceWithRawResponse,
    AsyncTransactionsResourceWithRawResponse,
    TransactionsResourceWithStreamingResponse,
    AsyncTransactionsResourceWithStreamingResponse,
)
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
from .account_access import (
    AccountAccessResource,
    AsyncAccountAccessResource,
    AccountAccessResourceWithRawResponse,
    AsyncAccountAccessResourceWithRawResponse,
    AccountAccessResourceWithStreamingResponse,
    AsyncAccountAccessResourceWithStreamingResponse,
)
from ....._base_client import make_request_options
from .transaction_requests import (
    TransactionRequestsResource,
    AsyncTransactionRequestsResource,
    TransactionRequestsResourceWithRawResponse,
    AsyncTransactionRequestsResourceWithRawResponse,
    TransactionRequestsResourceWithStreamingResponse,
    AsyncTransactionRequestsResourceWithStreamingResponse,
)
from .....types.banks.accounts import view_create_params, view_delete_params, view_update_params
from .transaction_request_types import (
    TransactionRequestTypesResource,
    AsyncTransactionRequestTypesResource,
    TransactionRequestTypesResourceWithRawResponse,
    AsyncTransactionRequestTypesResourceWithRawResponse,
    TransactionRequestTypesResourceWithStreamingResponse,
    AsyncTransactionRequestTypesResourceWithStreamingResponse,
)
from .transaction_request_types.transaction_request_types import (
    TransactionRequestTypesResource,
    AsyncTransactionRequestTypesResource,
)

__all__ = ["ViewsResource", "AsyncViewsResource"]


class ViewsResource(SyncAPIResource):
    @cached_property
    def transaction_request_types(self) -> TransactionRequestTypesResource:
        return TransactionRequestTypesResource(self._client)

    @cached_property
    def transaction_requests(self) -> TransactionRequestsResource:
        return TransactionRequestsResource(self._client)

    @cached_property
    def transactions(self) -> TransactionsResource:
        return TransactionsResource(self._client)

    @cached_property
    def account_access(self) -> AccountAccessResource:
        return AccountAccessResource(self._client)

    @cached_property
    def with_raw_response(self) -> ViewsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ViewsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ViewsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ViewsResourceWithStreamingResponse(self)

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
        <p>Create a custom view on bank account</p><p>Authentication is Mandatory and the user needs to have access to the owner view.<br />The 'alias' field in the JSON can take one of three values:</p><ul><li><em>public</em>: to use the public alias if there is one specified for the other account.</li><li><em>private</em>: to use the private alias if there is one specified for the other account.</li><li><p><em>''(empty string)</em>: to use no alias; the view shows the real name of the other account.</p></li></ul><p>The 'hide_metadata_if_alias_used' field in the JSON can take boolean values. If it is set to <code>true</code> and there is an alias on the other account then the other accounts' metadata (like more_info, url, image_url, open_corporates_url, etc.) will be hidden. Otherwise the metadata will be shown.</p><p>The 'allowed_actions' field is a list containing the name of the actions allowed on this view, all the actions contained will be set to <code>true</code> on the view creation, the rest will be set to <code>false</code>.</p><p>You MUST use a leading _ (underscore) in the view name because other view names are reserved for OBP <a href="/index#group-View-System">system views</a>.</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/views",
            body=maybe_transform(body, view_create_params.ViewCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

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
        <p>Information returned about the account through VIEW_ID :</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/views/{view_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
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
        <p>Update an existing custom view on a bank account</p><p>Authentication is Mandatory and the user needs to have access to the owner view.</p><p>The json sent is the same as during view creation (above), with one difference: the 'name' field<br />of a view is not editable (it is only set when a view is created)</p>

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
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/views/{view_id}",
            body=maybe_transform(body, view_update_params.ViewUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
        self,
        account_id: str,
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
        <h1><a href="#views" id="views">Views</a></h1><p>Views in Open Bank Project provide a mechanism for fine grained access control and delegation to Accounts and Transactions. Account holders use the 'owner' view by default. Delegated access is made through other views for example 'accountants', 'share-holders' or 'tagging-application'. Views can be created via the API and each view has a list of entitlements.</p><p>Views on accounts and transactions filter the underlying data to redact certain fields for certain users. For instance the balance on an account may be hidden from the public. The way to know what is possible on a view is determined in the following JSON.</p><p><strong>Data:</strong> When a view moderates a set of data, some fields my contain the value <code>null</code> rather than the original value. This indicates either that the user is not allowed to see the original data or the field is empty.</p><p>There is currently one exception to this rule; the 'holder' field in the JSON contains always a value which is either an alias or the real name - indicated by the 'is_alias' field.</p><p><strong>Action:</strong> When a user performs an action like trying to post a comment (with POST API call), if he is not allowed, the body response will contain an error message.</p><p><strong>Metadata:</strong><br />Transaction metadata (like images, tags, comments, etc.) will appears <em>ONLY</em> on the view where they have been created e.g. comments posted to the public view only appear on the public view.</p><p>The other account metadata fields (like image_URL, more_info, etc.) are unique through all the views. Example, if a user edits the 'more_info' field in the 'team' view, then the view 'authorities' will show the new value (if it is allowed to do it).</p><h1><a href="#all" id="all">All</a></h1><p><em>Optional</em></p><p>Returns the list of the views created for account ACCOUNT_ID at BANK_ID.</p><p>Authentication is Mandatory and the user needs to have access to the owner view.</p>

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
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/views",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
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
        <p>Deletes the custom view specified by VIEW_ID on the bank account specified by ACCOUNT_ID at bank BANK_ID</p><p>Authentication is Mandatory</p>

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
        return self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/views/{view_id}",
            body=maybe_transform(body, view_delete_params.ViewDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncViewsResource(AsyncAPIResource):
    @cached_property
    def transaction_request_types(self) -> AsyncTransactionRequestTypesResource:
        return AsyncTransactionRequestTypesResource(self._client)

    @cached_property
    def transaction_requests(self) -> AsyncTransactionRequestsResource:
        return AsyncTransactionRequestsResource(self._client)

    @cached_property
    def transactions(self) -> AsyncTransactionsResource:
        return AsyncTransactionsResource(self._client)

    @cached_property
    def account_access(self) -> AsyncAccountAccessResource:
        return AsyncAccountAccessResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncViewsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncViewsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncViewsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncViewsResourceWithStreamingResponse(self)

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
        <p>Create a custom view on bank account</p><p>Authentication is Mandatory and the user needs to have access to the owner view.<br />The 'alias' field in the JSON can take one of three values:</p><ul><li><em>public</em>: to use the public alias if there is one specified for the other account.</li><li><em>private</em>: to use the private alias if there is one specified for the other account.</li><li><p><em>''(empty string)</em>: to use no alias; the view shows the real name of the other account.</p></li></ul><p>The 'hide_metadata_if_alias_used' field in the JSON can take boolean values. If it is set to <code>true</code> and there is an alias on the other account then the other accounts' metadata (like more_info, url, image_url, open_corporates_url, etc.) will be hidden. Otherwise the metadata will be shown.</p><p>The 'allowed_actions' field is a list containing the name of the actions allowed on this view, all the actions contained will be set to <code>true</code> on the view creation, the rest will be set to <code>false</code>.</p><p>You MUST use a leading _ (underscore) in the view name because other view names are reserved for OBP <a href="/index#group-View-System">system views</a>.</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/views",
            body=await async_maybe_transform(body, view_create_params.ViewCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

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
        <p>Information returned about the account through VIEW_ID :</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/views/{view_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
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
        <p>Update an existing custom view on a bank account</p><p>Authentication is Mandatory and the user needs to have access to the owner view.</p><p>The json sent is the same as during view creation (above), with one difference: the 'name' field<br />of a view is not editable (it is only set when a view is created)</p>

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
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/views/{view_id}",
            body=await async_maybe_transform(body, view_update_params.ViewUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
        self,
        account_id: str,
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
        <h1><a href="#views" id="views">Views</a></h1><p>Views in Open Bank Project provide a mechanism for fine grained access control and delegation to Accounts and Transactions. Account holders use the 'owner' view by default. Delegated access is made through other views for example 'accountants', 'share-holders' or 'tagging-application'. Views can be created via the API and each view has a list of entitlements.</p><p>Views on accounts and transactions filter the underlying data to redact certain fields for certain users. For instance the balance on an account may be hidden from the public. The way to know what is possible on a view is determined in the following JSON.</p><p><strong>Data:</strong> When a view moderates a set of data, some fields my contain the value <code>null</code> rather than the original value. This indicates either that the user is not allowed to see the original data or the field is empty.</p><p>There is currently one exception to this rule; the 'holder' field in the JSON contains always a value which is either an alias or the real name - indicated by the 'is_alias' field.</p><p><strong>Action:</strong> When a user performs an action like trying to post a comment (with POST API call), if he is not allowed, the body response will contain an error message.</p><p><strong>Metadata:</strong><br />Transaction metadata (like images, tags, comments, etc.) will appears <em>ONLY</em> on the view where they have been created e.g. comments posted to the public view only appear on the public view.</p><p>The other account metadata fields (like image_URL, more_info, etc.) are unique through all the views. Example, if a user edits the 'more_info' field in the 'team' view, then the view 'authorities' will show the new value (if it is allowed to do it).</p><h1><a href="#all" id="all">All</a></h1><p><em>Optional</em></p><p>Returns the list of the views created for account ACCOUNT_ID at BANK_ID.</p><p>Authentication is Mandatory and the user needs to have access to the owner view.</p>

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
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/views",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
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
        <p>Deletes the custom view specified by VIEW_ID on the bank account specified by ACCOUNT_ID at bank BANK_ID</p><p>Authentication is Mandatory</p>

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
        return await self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/views/{view_id}",
            body=await async_maybe_transform(body, view_delete_params.ViewDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ViewsResourceWithRawResponse:
    def __init__(self, views: ViewsResource) -> None:
        self._views = views

        self.create = to_custom_raw_response_wrapper(
            views.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            views.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            views.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            views.list,
            BinaryAPIResponse,
        )
        self.delete = to_custom_raw_response_wrapper(
            views.delete,
            BinaryAPIResponse,
        )

    @cached_property
    def transaction_request_types(self) -> TransactionRequestTypesResourceWithRawResponse:
        return TransactionRequestTypesResourceWithRawResponse(self._views.transaction_request_types)

    @cached_property
    def transaction_requests(self) -> TransactionRequestsResourceWithRawResponse:
        return TransactionRequestsResourceWithRawResponse(self._views.transaction_requests)

    @cached_property
    def transactions(self) -> TransactionsResourceWithRawResponse:
        return TransactionsResourceWithRawResponse(self._views.transactions)

    @cached_property
    def account_access(self) -> AccountAccessResourceWithRawResponse:
        return AccountAccessResourceWithRawResponse(self._views.account_access)


class AsyncViewsResourceWithRawResponse:
    def __init__(self, views: AsyncViewsResource) -> None:
        self._views = views

        self.create = async_to_custom_raw_response_wrapper(
            views.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            views.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            views.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            views.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_custom_raw_response_wrapper(
            views.delete,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def transaction_request_types(self) -> AsyncTransactionRequestTypesResourceWithRawResponse:
        return AsyncTransactionRequestTypesResourceWithRawResponse(self._views.transaction_request_types)

    @cached_property
    def transaction_requests(self) -> AsyncTransactionRequestsResourceWithRawResponse:
        return AsyncTransactionRequestsResourceWithRawResponse(self._views.transaction_requests)

    @cached_property
    def transactions(self) -> AsyncTransactionsResourceWithRawResponse:
        return AsyncTransactionsResourceWithRawResponse(self._views.transactions)

    @cached_property
    def account_access(self) -> AsyncAccountAccessResourceWithRawResponse:
        return AsyncAccountAccessResourceWithRawResponse(self._views.account_access)


class ViewsResourceWithStreamingResponse:
    def __init__(self, views: ViewsResource) -> None:
        self._views = views

        self.create = to_custom_streamed_response_wrapper(
            views.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            views.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            views.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            views.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_custom_streamed_response_wrapper(
            views.delete,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def transaction_request_types(self) -> TransactionRequestTypesResourceWithStreamingResponse:
        return TransactionRequestTypesResourceWithStreamingResponse(self._views.transaction_request_types)

    @cached_property
    def transaction_requests(self) -> TransactionRequestsResourceWithStreamingResponse:
        return TransactionRequestsResourceWithStreamingResponse(self._views.transaction_requests)

    @cached_property
    def transactions(self) -> TransactionsResourceWithStreamingResponse:
        return TransactionsResourceWithStreamingResponse(self._views.transactions)

    @cached_property
    def account_access(self) -> AccountAccessResourceWithStreamingResponse:
        return AccountAccessResourceWithStreamingResponse(self._views.account_access)


class AsyncViewsResourceWithStreamingResponse:
    def __init__(self, views: AsyncViewsResource) -> None:
        self._views = views

        self.create = async_to_custom_streamed_response_wrapper(
            views.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            views.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            views.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            views.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_custom_streamed_response_wrapper(
            views.delete,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def transaction_request_types(self) -> AsyncTransactionRequestTypesResourceWithStreamingResponse:
        return AsyncTransactionRequestTypesResourceWithStreamingResponse(self._views.transaction_request_types)

    @cached_property
    def transaction_requests(self) -> AsyncTransactionRequestsResourceWithStreamingResponse:
        return AsyncTransactionRequestsResourceWithStreamingResponse(self._views.transaction_requests)

    @cached_property
    def transactions(self) -> AsyncTransactionsResourceWithStreamingResponse:
        return AsyncTransactionsResourceWithStreamingResponse(self._views.transactions)

    @cached_property
    def account_access(self) -> AsyncAccountAccessResourceWithStreamingResponse:
        return AsyncAccountAccessResourceWithStreamingResponse(self._views.account_access)
