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
from .....types.banks.accounts.other_accounts import (
    public_alias_create_params,
    public_alias_delete_params,
    public_alias_update_params,
)

__all__ = ["PublicAliasResource", "AsyncPublicAliasResource"]


class PublicAliasResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PublicAliasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return PublicAliasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PublicAliasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return PublicAliasResourceWithStreamingResponse(self)

    def create(
        self,
        other_account_id: str,
        *,
        bank_id: str,
        account_id: str,
        view_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Creates the public alias for the other account OTHER_ACCOUNT_ID.</p><p>Authentication is Optional<br />Authentication is required if the view is not public.</p><p>Note: Public aliases are automatically generated for new 'other accounts / counterparties', so this call should only be used if<br />the public alias was deleted.</p><p>The VIEW_ID parameter should be a view the caller is permitted to access to and that has permission to create public aliases.</p>

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
        if not other_account_id:
            raise ValueError(f"Expected a non-empty value for `other_account_id` but received {other_account_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/other_accounts/{other_account_id}/public_alias",
            body=maybe_transform(body, public_alias_create_params.PublicAliasCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def retrieve(
        self,
        other_account_id: str,
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
        <p>Returns the public alias of the other account OTHER_ACCOUNT_ID.<br />Authentication is Optional<br />Authentication is Mandatory if the view is not public.</p>

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
        if not other_account_id:
            raise ValueError(f"Expected a non-empty value for `other_account_id` but received {other_account_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/other_accounts/{other_account_id}/public_alias",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        other_account_id: str,
        *,
        bank_id: str,
        account_id: str,
        view_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Updates the public alias of the other account / counterparty OTHER_ACCOUNT_ID.</p><p>Authentication is Optional<br />Authentication is required if the view is not public.</p>

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
        if not other_account_id:
            raise ValueError(f"Expected a non-empty value for `other_account_id` but received {other_account_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/other_accounts/{other_account_id}/public_alias",
            body=maybe_transform(body, public_alias_update_params.PublicAliasUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        other_account_id: str,
        *,
        bank_id: str,
        account_id: str,
        view_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Deletes the public alias of the other account OTHER_ACCOUNT_ID.</p><p>Authentication is Optional<br />Authentication is required if the view is not public.</p>

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
        if not other_account_id:
            raise ValueError(f"Expected a non-empty value for `other_account_id` but received {other_account_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/other_accounts/{other_account_id}/public_alias",
            body=maybe_transform(body, public_alias_delete_params.PublicAliasDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncPublicAliasResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPublicAliasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPublicAliasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPublicAliasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncPublicAliasResourceWithStreamingResponse(self)

    async def create(
        self,
        other_account_id: str,
        *,
        bank_id: str,
        account_id: str,
        view_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Creates the public alias for the other account OTHER_ACCOUNT_ID.</p><p>Authentication is Optional<br />Authentication is required if the view is not public.</p><p>Note: Public aliases are automatically generated for new 'other accounts / counterparties', so this call should only be used if<br />the public alias was deleted.</p><p>The VIEW_ID parameter should be a view the caller is permitted to access to and that has permission to create public aliases.</p>

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
        if not other_account_id:
            raise ValueError(f"Expected a non-empty value for `other_account_id` but received {other_account_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/other_accounts/{other_account_id}/public_alias",
            body=await async_maybe_transform(body, public_alias_create_params.PublicAliasCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def retrieve(
        self,
        other_account_id: str,
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
        <p>Returns the public alias of the other account OTHER_ACCOUNT_ID.<br />Authentication is Optional<br />Authentication is Mandatory if the view is not public.</p>

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
        if not other_account_id:
            raise ValueError(f"Expected a non-empty value for `other_account_id` but received {other_account_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/other_accounts/{other_account_id}/public_alias",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        other_account_id: str,
        *,
        bank_id: str,
        account_id: str,
        view_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Updates the public alias of the other account / counterparty OTHER_ACCOUNT_ID.</p><p>Authentication is Optional<br />Authentication is required if the view is not public.</p>

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
        if not other_account_id:
            raise ValueError(f"Expected a non-empty value for `other_account_id` but received {other_account_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/other_accounts/{other_account_id}/public_alias",
            body=await async_maybe_transform(body, public_alias_update_params.PublicAliasUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        other_account_id: str,
        *,
        bank_id: str,
        account_id: str,
        view_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Deletes the public alias of the other account OTHER_ACCOUNT_ID.</p><p>Authentication is Optional<br />Authentication is required if the view is not public.</p>

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
        if not other_account_id:
            raise ValueError(f"Expected a non-empty value for `other_account_id` but received {other_account_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/other_accounts/{other_account_id}/public_alias",
            body=await async_maybe_transform(body, public_alias_delete_params.PublicAliasDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class PublicAliasResourceWithRawResponse:
    def __init__(self, public_alias: PublicAliasResource) -> None:
        self._public_alias = public_alias

        self.create = to_custom_raw_response_wrapper(
            public_alias.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            public_alias.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            public_alias.update,
            BinaryAPIResponse,
        )
        self.delete = to_custom_raw_response_wrapper(
            public_alias.delete,
            BinaryAPIResponse,
        )


class AsyncPublicAliasResourceWithRawResponse:
    def __init__(self, public_alias: AsyncPublicAliasResource) -> None:
        self._public_alias = public_alias

        self.create = async_to_custom_raw_response_wrapper(
            public_alias.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            public_alias.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            public_alias.update,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_custom_raw_response_wrapper(
            public_alias.delete,
            AsyncBinaryAPIResponse,
        )


class PublicAliasResourceWithStreamingResponse:
    def __init__(self, public_alias: PublicAliasResource) -> None:
        self._public_alias = public_alias

        self.create = to_custom_streamed_response_wrapper(
            public_alias.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            public_alias.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            public_alias.update,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_custom_streamed_response_wrapper(
            public_alias.delete,
            StreamedBinaryAPIResponse,
        )


class AsyncPublicAliasResourceWithStreamingResponse:
    def __init__(self, public_alias: AsyncPublicAliasResource) -> None:
        self._public_alias = public_alias

        self.create = async_to_custom_streamed_response_wrapper(
            public_alias.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            public_alias.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            public_alias.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_custom_streamed_response_wrapper(
            public_alias.delete,
            AsyncStreamedBinaryAPIResponse,
        )
