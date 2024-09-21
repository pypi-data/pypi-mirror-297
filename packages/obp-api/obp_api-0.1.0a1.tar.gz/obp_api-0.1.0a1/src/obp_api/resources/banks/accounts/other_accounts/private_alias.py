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
from .....types.banks.accounts.other_accounts import private_alias_delete_params

__all__ = ["PrivateAliasResource", "AsyncPrivateAliasResource"]


class PrivateAliasResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PrivateAliasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return PrivateAliasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PrivateAliasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return PrivateAliasResourceWithStreamingResponse(self)

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
        <p>Deletes the private alias of the other account OTHER_ACCOUNT_ID.</p><p>Authentication is Optional<br />Authentication is required if the view is not public.</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/other_accounts/{other_account_id}/private_alias",
            body=maybe_transform(body, private_alias_delete_params.PrivateAliasDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncPrivateAliasResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPrivateAliasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPrivateAliasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPrivateAliasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncPrivateAliasResourceWithStreamingResponse(self)

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
        <p>Deletes the private alias of the other account OTHER_ACCOUNT_ID.</p><p>Authentication is Optional<br />Authentication is required if the view is not public.</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/other_accounts/{other_account_id}/private_alias",
            body=await async_maybe_transform(body, private_alias_delete_params.PrivateAliasDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class PrivateAliasResourceWithRawResponse:
    def __init__(self, private_alias: PrivateAliasResource) -> None:
        self._private_alias = private_alias

        self.delete = to_custom_raw_response_wrapper(
            private_alias.delete,
            BinaryAPIResponse,
        )


class AsyncPrivateAliasResourceWithRawResponse:
    def __init__(self, private_alias: AsyncPrivateAliasResource) -> None:
        self._private_alias = private_alias

        self.delete = async_to_custom_raw_response_wrapper(
            private_alias.delete,
            AsyncBinaryAPIResponse,
        )


class PrivateAliasResourceWithStreamingResponse:
    def __init__(self, private_alias: PrivateAliasResource) -> None:
        self._private_alias = private_alias

        self.delete = to_custom_streamed_response_wrapper(
            private_alias.delete,
            StreamedBinaryAPIResponse,
        )


class AsyncPrivateAliasResourceWithStreamingResponse:
    def __init__(self, private_alias: AsyncPrivateAliasResource) -> None:
        self._private_alias = private_alias

        self.delete = async_to_custom_streamed_response_wrapper(
            private_alias.delete,
            AsyncStreamedBinaryAPIResponse,
        )
