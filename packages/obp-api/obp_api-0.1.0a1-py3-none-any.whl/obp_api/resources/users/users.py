# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .locks import (
    LocksResource,
    AsyncLocksResource,
    LocksResourceWithRawResponse,
    AsyncLocksResourceWithRawResponse,
    LocksResourceWithStreamingResponse,
    AsyncLocksResourceWithStreamingResponse,
)
from ...types import user_create_params, user_reset_password_url_params
from .current import (
    CurrentResource,
    AsyncCurrentResource,
    CurrentResourceWithRawResponse,
    AsyncCurrentResourceWithRawResponse,
    CurrentResourceWithStreamingResponse,
    AsyncCurrentResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .consents import (
    ConsentsResource,
    AsyncConsentsResource,
    ConsentsResourceWithRawResponse,
    AsyncConsentsResourceWithRawResponse,
    ConsentsResourceWithStreamingResponse,
    AsyncConsentsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
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
from .lock_status import (
    LockStatusResource,
    AsyncLockStatusResource,
    LockStatusResourceWithRawResponse,
    AsyncLockStatusResourceWithRawResponse,
    LockStatusResourceWithStreamingResponse,
    AsyncLockStatusResourceWithStreamingResponse,
)
from .entitlements import (
    EntitlementsResource,
    AsyncEntitlementsResource,
    EntitlementsResourceWithRawResponse,
    AsyncEntitlementsResourceWithRawResponse,
    EntitlementsResourceWithStreamingResponse,
    AsyncEntitlementsResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from .account_access import (
    AccountAccessResource,
    AsyncAccountAccessResource,
    AccountAccessResourceWithRawResponse,
    AsyncAccountAccessResourceWithRawResponse,
    AccountAccessResourceWithStreamingResponse,
    AsyncAccountAccessResourceWithStreamingResponse,
)
from .current.current import CurrentResource, AsyncCurrentResource
from .auth_context_updates import (
    AuthContextUpdatesResource,
    AsyncAuthContextUpdatesResource,
    AuthContextUpdatesResourceWithRawResponse,
    AsyncAuthContextUpdatesResourceWithRawResponse,
    AuthContextUpdatesResourceWithStreamingResponse,
    AsyncAuthContextUpdatesResourceWithStreamingResponse,
)

__all__ = ["UsersResource", "AsyncUsersResource"]


class UsersResource(SyncAPIResource):
    @cached_property
    def entitlements(self) -> EntitlementsResource:
        return EntitlementsResource(self._client)

    @cached_property
    def auth_context_updates(self) -> AuthContextUpdatesResource:
        return AuthContextUpdatesResource(self._client)

    @cached_property
    def current(self) -> CurrentResource:
        return CurrentResource(self._client)

    @cached_property
    def consents(self) -> ConsentsResource:
        return ConsentsResource(self._client)

    @cached_property
    def lock_status(self) -> LockStatusResource:
        return LockStatusResource(self._client)

    @cached_property
    def locks(self) -> LocksResource:
        return LocksResource(self._client)

    @cached_property
    def account_access(self) -> AccountAccessResource:
        return AccountAccessResource(self._client)

    @cached_property
    def with_raw_response(self) -> UsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return UsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return UsersResourceWithStreamingResponse(self)

    def create(
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
        <p>Creates OBP user.<br />No authorisation (currently) required.</p><p>Mimics current webform to Register.</p><p>Requires username(email) and password.</p><p>Returns 409 error if username not unique.</p><p>May require validation of email address.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/users",
            body=maybe_transform(body, user_create_params.UserCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get all users</p><p>Authentication is Mandatory</p><p>CanGetAnyUser entitlement is required,</p><p>Possible custom url parameters for pagination:</p><ul><li>limit=NUMBER ==&gt; default value: 50</li><li>offset=NUMBER ==&gt; default value: 0</li></ul><p>eg1:?limit=100&amp;offset=0</p><ul><li>sort_direction=ASC/DESC ==&gt; default value: DESC.</li></ul><p>eg2:?limit=100&amp;offset=0&amp;sort_direction=ASC</p><ul><li>locked_status (if null ignore)</li></ul>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/users",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete a User.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/users/{user_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def reset_password_url(
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
        <p>Create password reset url.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/management/user/reset-password-url",
            body=maybe_transform(body, user_reset_password_url_params.UserResetPasswordURLParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncUsersResource(AsyncAPIResource):
    @cached_property
    def entitlements(self) -> AsyncEntitlementsResource:
        return AsyncEntitlementsResource(self._client)

    @cached_property
    def auth_context_updates(self) -> AsyncAuthContextUpdatesResource:
        return AsyncAuthContextUpdatesResource(self._client)

    @cached_property
    def current(self) -> AsyncCurrentResource:
        return AsyncCurrentResource(self._client)

    @cached_property
    def consents(self) -> AsyncConsentsResource:
        return AsyncConsentsResource(self._client)

    @cached_property
    def lock_status(self) -> AsyncLockStatusResource:
        return AsyncLockStatusResource(self._client)

    @cached_property
    def locks(self) -> AsyncLocksResource:
        return AsyncLocksResource(self._client)

    @cached_property
    def account_access(self) -> AsyncAccountAccessResource:
        return AsyncAccountAccessResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncUsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncUsersResourceWithStreamingResponse(self)

    async def create(
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
        <p>Creates OBP user.<br />No authorisation (currently) required.</p><p>Mimics current webform to Register.</p><p>Requires username(email) and password.</p><p>Returns 409 error if username not unique.</p><p>May require validation of email address.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/users",
            body=await async_maybe_transform(body, user_create_params.UserCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get all users</p><p>Authentication is Mandatory</p><p>CanGetAnyUser entitlement is required,</p><p>Possible custom url parameters for pagination:</p><ul><li>limit=NUMBER ==&gt; default value: 50</li><li>offset=NUMBER ==&gt; default value: 0</li></ul><p>eg1:?limit=100&amp;offset=0</p><ul><li>sort_direction=ASC/DESC ==&gt; default value: DESC.</li></ul><p>eg2:?limit=100&amp;offset=0&amp;sort_direction=ASC</p><ul><li>locked_status (if null ignore)</li></ul>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/users",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete a User.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/users/{user_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def reset_password_url(
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
        <p>Create password reset url.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/management/user/reset-password-url",
            body=await async_maybe_transform(body, user_reset_password_url_params.UserResetPasswordURLParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class UsersResourceWithRawResponse:
    def __init__(self, users: UsersResource) -> None:
        self._users = users

        self.create = to_custom_raw_response_wrapper(
            users.create,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            users.list,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            users.delete,
        )
        self.reset_password_url = to_custom_raw_response_wrapper(
            users.reset_password_url,
            BinaryAPIResponse,
        )

    @cached_property
    def entitlements(self) -> EntitlementsResourceWithRawResponse:
        return EntitlementsResourceWithRawResponse(self._users.entitlements)

    @cached_property
    def auth_context_updates(self) -> AuthContextUpdatesResourceWithRawResponse:
        return AuthContextUpdatesResourceWithRawResponse(self._users.auth_context_updates)

    @cached_property
    def current(self) -> CurrentResourceWithRawResponse:
        return CurrentResourceWithRawResponse(self._users.current)

    @cached_property
    def consents(self) -> ConsentsResourceWithRawResponse:
        return ConsentsResourceWithRawResponse(self._users.consents)

    @cached_property
    def lock_status(self) -> LockStatusResourceWithRawResponse:
        return LockStatusResourceWithRawResponse(self._users.lock_status)

    @cached_property
    def locks(self) -> LocksResourceWithRawResponse:
        return LocksResourceWithRawResponse(self._users.locks)

    @cached_property
    def account_access(self) -> AccountAccessResourceWithRawResponse:
        return AccountAccessResourceWithRawResponse(self._users.account_access)


class AsyncUsersResourceWithRawResponse:
    def __init__(self, users: AsyncUsersResource) -> None:
        self._users = users

        self.create = async_to_custom_raw_response_wrapper(
            users.create,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            users.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            users.delete,
        )
        self.reset_password_url = async_to_custom_raw_response_wrapper(
            users.reset_password_url,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def entitlements(self) -> AsyncEntitlementsResourceWithRawResponse:
        return AsyncEntitlementsResourceWithRawResponse(self._users.entitlements)

    @cached_property
    def auth_context_updates(self) -> AsyncAuthContextUpdatesResourceWithRawResponse:
        return AsyncAuthContextUpdatesResourceWithRawResponse(self._users.auth_context_updates)

    @cached_property
    def current(self) -> AsyncCurrentResourceWithRawResponse:
        return AsyncCurrentResourceWithRawResponse(self._users.current)

    @cached_property
    def consents(self) -> AsyncConsentsResourceWithRawResponse:
        return AsyncConsentsResourceWithRawResponse(self._users.consents)

    @cached_property
    def lock_status(self) -> AsyncLockStatusResourceWithRawResponse:
        return AsyncLockStatusResourceWithRawResponse(self._users.lock_status)

    @cached_property
    def locks(self) -> AsyncLocksResourceWithRawResponse:
        return AsyncLocksResourceWithRawResponse(self._users.locks)

    @cached_property
    def account_access(self) -> AsyncAccountAccessResourceWithRawResponse:
        return AsyncAccountAccessResourceWithRawResponse(self._users.account_access)


class UsersResourceWithStreamingResponse:
    def __init__(self, users: UsersResource) -> None:
        self._users = users

        self.create = to_custom_streamed_response_wrapper(
            users.create,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            users.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            users.delete,
        )
        self.reset_password_url = to_custom_streamed_response_wrapper(
            users.reset_password_url,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def entitlements(self) -> EntitlementsResourceWithStreamingResponse:
        return EntitlementsResourceWithStreamingResponse(self._users.entitlements)

    @cached_property
    def auth_context_updates(self) -> AuthContextUpdatesResourceWithStreamingResponse:
        return AuthContextUpdatesResourceWithStreamingResponse(self._users.auth_context_updates)

    @cached_property
    def current(self) -> CurrentResourceWithStreamingResponse:
        return CurrentResourceWithStreamingResponse(self._users.current)

    @cached_property
    def consents(self) -> ConsentsResourceWithStreamingResponse:
        return ConsentsResourceWithStreamingResponse(self._users.consents)

    @cached_property
    def lock_status(self) -> LockStatusResourceWithStreamingResponse:
        return LockStatusResourceWithStreamingResponse(self._users.lock_status)

    @cached_property
    def locks(self) -> LocksResourceWithStreamingResponse:
        return LocksResourceWithStreamingResponse(self._users.locks)

    @cached_property
    def account_access(self) -> AccountAccessResourceWithStreamingResponse:
        return AccountAccessResourceWithStreamingResponse(self._users.account_access)


class AsyncUsersResourceWithStreamingResponse:
    def __init__(self, users: AsyncUsersResource) -> None:
        self._users = users

        self.create = async_to_custom_streamed_response_wrapper(
            users.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            users.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            users.delete,
        )
        self.reset_password_url = async_to_custom_streamed_response_wrapper(
            users.reset_password_url,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def entitlements(self) -> AsyncEntitlementsResourceWithStreamingResponse:
        return AsyncEntitlementsResourceWithStreamingResponse(self._users.entitlements)

    @cached_property
    def auth_context_updates(self) -> AsyncAuthContextUpdatesResourceWithStreamingResponse:
        return AsyncAuthContextUpdatesResourceWithStreamingResponse(self._users.auth_context_updates)

    @cached_property
    def current(self) -> AsyncCurrentResourceWithStreamingResponse:
        return AsyncCurrentResourceWithStreamingResponse(self._users.current)

    @cached_property
    def consents(self) -> AsyncConsentsResourceWithStreamingResponse:
        return AsyncConsentsResourceWithStreamingResponse(self._users.consents)

    @cached_property
    def lock_status(self) -> AsyncLockStatusResourceWithStreamingResponse:
        return AsyncLockStatusResourceWithStreamingResponse(self._users.lock_status)

    @cached_property
    def locks(self) -> AsyncLocksResourceWithStreamingResponse:
        return AsyncLocksResourceWithStreamingResponse(self._users.locks)

    @cached_property
    def account_access(self) -> AsyncAccountAccessResourceWithStreamingResponse:
        return AsyncAccountAccessResourceWithStreamingResponse(self._users.account_access)
