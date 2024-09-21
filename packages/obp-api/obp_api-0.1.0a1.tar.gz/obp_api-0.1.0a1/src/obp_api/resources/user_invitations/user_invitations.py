# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .secret_link import (
    SecretLinkResource,
    AsyncSecretLinkResource,
    SecretLinkResourceWithRawResponse,
    AsyncSecretLinkResourceWithRawResponse,
    SecretLinkResourceWithStreamingResponse,
    AsyncSecretLinkResourceWithStreamingResponse,
)

__all__ = ["UserInvitationsResource", "AsyncUserInvitationsResource"]


class UserInvitationsResource(SyncAPIResource):
    @cached_property
    def secret_link(self) -> SecretLinkResource:
        return SecretLinkResource(self._client)

    @cached_property
    def with_raw_response(self) -> UserInvitationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return UserInvitationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UserInvitationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return UserInvitationsResourceWithStreamingResponse(self)


class AsyncUserInvitationsResource(AsyncAPIResource):
    @cached_property
    def secret_link(self) -> AsyncSecretLinkResource:
        return AsyncSecretLinkResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncUserInvitationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUserInvitationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUserInvitationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncUserInvitationsResourceWithStreamingResponse(self)


class UserInvitationsResourceWithRawResponse:
    def __init__(self, user_invitations: UserInvitationsResource) -> None:
        self._user_invitations = user_invitations

    @cached_property
    def secret_link(self) -> SecretLinkResourceWithRawResponse:
        return SecretLinkResourceWithRawResponse(self._user_invitations.secret_link)


class AsyncUserInvitationsResourceWithRawResponse:
    def __init__(self, user_invitations: AsyncUserInvitationsResource) -> None:
        self._user_invitations = user_invitations

    @cached_property
    def secret_link(self) -> AsyncSecretLinkResourceWithRawResponse:
        return AsyncSecretLinkResourceWithRawResponse(self._user_invitations.secret_link)


class UserInvitationsResourceWithStreamingResponse:
    def __init__(self, user_invitations: UserInvitationsResource) -> None:
        self._user_invitations = user_invitations

    @cached_property
    def secret_link(self) -> SecretLinkResourceWithStreamingResponse:
        return SecretLinkResourceWithStreamingResponse(self._user_invitations.secret_link)


class AsyncUserInvitationsResourceWithStreamingResponse:
    def __init__(self, user_invitations: AsyncUserInvitationsResource) -> None:
        self._user_invitations = user_invitations

    @cached_property
    def secret_link(self) -> AsyncSecretLinkResourceWithStreamingResponse:
        return AsyncSecretLinkResourceWithStreamingResponse(self._user_invitations.secret_link)
