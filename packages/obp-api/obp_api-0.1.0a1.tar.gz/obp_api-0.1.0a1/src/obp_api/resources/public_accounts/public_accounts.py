# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .account import (
    AccountResource,
    AsyncAccountResource,
    AccountResourceWithRawResponse,
    AsyncAccountResourceWithRawResponse,
    AccountResourceWithStreamingResponse,
    AsyncAccountResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["PublicAccountsResource", "AsyncPublicAccountsResource"]


class PublicAccountsResource(SyncAPIResource):
    @cached_property
    def account(self) -> AccountResource:
        return AccountResource(self._client)

    @cached_property
    def with_raw_response(self) -> PublicAccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return PublicAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PublicAccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return PublicAccountsResourceWithStreamingResponse(self)


class AsyncPublicAccountsResource(AsyncAPIResource):
    @cached_property
    def account(self) -> AsyncAccountResource:
        return AsyncAccountResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPublicAccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPublicAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPublicAccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncPublicAccountsResourceWithStreamingResponse(self)


class PublicAccountsResourceWithRawResponse:
    def __init__(self, public_accounts: PublicAccountsResource) -> None:
        self._public_accounts = public_accounts

    @cached_property
    def account(self) -> AccountResourceWithRawResponse:
        return AccountResourceWithRawResponse(self._public_accounts.account)


class AsyncPublicAccountsResourceWithRawResponse:
    def __init__(self, public_accounts: AsyncPublicAccountsResource) -> None:
        self._public_accounts = public_accounts

    @cached_property
    def account(self) -> AsyncAccountResourceWithRawResponse:
        return AsyncAccountResourceWithRawResponse(self._public_accounts.account)


class PublicAccountsResourceWithStreamingResponse:
    def __init__(self, public_accounts: PublicAccountsResource) -> None:
        self._public_accounts = public_accounts

    @cached_property
    def account(self) -> AccountResourceWithStreamingResponse:
        return AccountResourceWithStreamingResponse(self._public_accounts.account)


class AsyncPublicAccountsResourceWithStreamingResponse:
    def __init__(self, public_accounts: AsyncPublicAccountsResource) -> None:
        self._public_accounts = public_accounts

    @cached_property
    def account(self) -> AsyncAccountResourceWithStreamingResponse:
        return AsyncAccountResourceWithStreamingResponse(self._public_accounts.account)
