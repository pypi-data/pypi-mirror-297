# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ....._compat import cached_property
from .public_alias import (
    PublicAliasResource,
    AsyncPublicAliasResource,
    PublicAliasResourceWithRawResponse,
    AsyncPublicAliasResourceWithRawResponse,
    PublicAliasResourceWithStreamingResponse,
    AsyncPublicAliasResourceWithStreamingResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource
from .private_alias import (
    PrivateAliasResource,
    AsyncPrivateAliasResource,
    PrivateAliasResourceWithRawResponse,
    AsyncPrivateAliasResourceWithRawResponse,
    PrivateAliasResourceWithStreamingResponse,
    AsyncPrivateAliasResourceWithStreamingResponse,
)

__all__ = ["OtherAccountsResource", "AsyncOtherAccountsResource"]


class OtherAccountsResource(SyncAPIResource):
    @cached_property
    def private_alias(self) -> PrivateAliasResource:
        return PrivateAliasResource(self._client)

    @cached_property
    def public_alias(self) -> PublicAliasResource:
        return PublicAliasResource(self._client)

    @cached_property
    def with_raw_response(self) -> OtherAccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return OtherAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OtherAccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return OtherAccountsResourceWithStreamingResponse(self)


class AsyncOtherAccountsResource(AsyncAPIResource):
    @cached_property
    def private_alias(self) -> AsyncPrivateAliasResource:
        return AsyncPrivateAliasResource(self._client)

    @cached_property
    def public_alias(self) -> AsyncPublicAliasResource:
        return AsyncPublicAliasResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncOtherAccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOtherAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOtherAccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncOtherAccountsResourceWithStreamingResponse(self)


class OtherAccountsResourceWithRawResponse:
    def __init__(self, other_accounts: OtherAccountsResource) -> None:
        self._other_accounts = other_accounts

    @cached_property
    def private_alias(self) -> PrivateAliasResourceWithRawResponse:
        return PrivateAliasResourceWithRawResponse(self._other_accounts.private_alias)

    @cached_property
    def public_alias(self) -> PublicAliasResourceWithRawResponse:
        return PublicAliasResourceWithRawResponse(self._other_accounts.public_alias)


class AsyncOtherAccountsResourceWithRawResponse:
    def __init__(self, other_accounts: AsyncOtherAccountsResource) -> None:
        self._other_accounts = other_accounts

    @cached_property
    def private_alias(self) -> AsyncPrivateAliasResourceWithRawResponse:
        return AsyncPrivateAliasResourceWithRawResponse(self._other_accounts.private_alias)

    @cached_property
    def public_alias(self) -> AsyncPublicAliasResourceWithRawResponse:
        return AsyncPublicAliasResourceWithRawResponse(self._other_accounts.public_alias)


class OtherAccountsResourceWithStreamingResponse:
    def __init__(self, other_accounts: OtherAccountsResource) -> None:
        self._other_accounts = other_accounts

    @cached_property
    def private_alias(self) -> PrivateAliasResourceWithStreamingResponse:
        return PrivateAliasResourceWithStreamingResponse(self._other_accounts.private_alias)

    @cached_property
    def public_alias(self) -> PublicAliasResourceWithStreamingResponse:
        return PublicAliasResourceWithStreamingResponse(self._other_accounts.public_alias)


class AsyncOtherAccountsResourceWithStreamingResponse:
    def __init__(self, other_accounts: AsyncOtherAccountsResource) -> None:
        self._other_accounts = other_accounts

    @cached_property
    def private_alias(self) -> AsyncPrivateAliasResourceWithStreamingResponse:
        return AsyncPrivateAliasResourceWithStreamingResponse(self._other_accounts.private_alias)

    @cached_property
    def public_alias(self) -> AsyncPublicAliasResourceWithStreamingResponse:
        return AsyncPublicAliasResourceWithStreamingResponse(self._other_accounts.public_alias)
