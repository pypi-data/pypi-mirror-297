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
from ...types.users import auth_context_update_create_params, auth_context_update_challenge_params
from ..._base_client import make_request_options

__all__ = ["AuthContextUpdatesResource", "AsyncAuthContextUpdatesResource"]


class AuthContextUpdatesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AuthContextUpdatesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AuthContextUpdatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AuthContextUpdatesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AuthContextUpdatesResourceWithStreamingResponse(self)

    def create(
        self,
        sca_method: str,
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
        <p>Create User Auth Context Update Request.<br />Authentication is Mandatory</p><p>A One Time Password (OTP) (AKA security challenge) is sent Out of Band (OOB) to the User via the transport defined in SCA_METHOD<br />SCA_METHOD is typically &quot;SMS&quot; or &quot;EMAIL&quot;. &quot;EMAIL&quot; is used for testing purposes.</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not sca_method:
            raise ValueError(f"Expected a non-empty value for `sca_method` but received {sca_method!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/users/current/auth-context-updates/{sca_method}",
            body=maybe_transform(body, auth_context_update_create_params.AuthContextUpdateCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def challenge(
        self,
        auth_context_update_id: str,
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
        <p>Answer User Auth Context Update Challenge.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not auth_context_update_id:
            raise ValueError(
                f"Expected a non-empty value for `auth_context_update_id` but received {auth_context_update_id!r}"
            )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/users/current/auth-context-updates/{auth_context_update_id}/challenge",
            body=maybe_transform(body, auth_context_update_challenge_params.AuthContextUpdateChallengeParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAuthContextUpdatesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAuthContextUpdatesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAuthContextUpdatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAuthContextUpdatesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAuthContextUpdatesResourceWithStreamingResponse(self)

    async def create(
        self,
        sca_method: str,
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
        <p>Create User Auth Context Update Request.<br />Authentication is Mandatory</p><p>A One Time Password (OTP) (AKA security challenge) is sent Out of Band (OOB) to the User via the transport defined in SCA_METHOD<br />SCA_METHOD is typically &quot;SMS&quot; or &quot;EMAIL&quot;. &quot;EMAIL&quot; is used for testing purposes.</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not sca_method:
            raise ValueError(f"Expected a non-empty value for `sca_method` but received {sca_method!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/users/current/auth-context-updates/{sca_method}",
            body=await async_maybe_transform(body, auth_context_update_create_params.AuthContextUpdateCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def challenge(
        self,
        auth_context_update_id: str,
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
        <p>Answer User Auth Context Update Challenge.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not auth_context_update_id:
            raise ValueError(
                f"Expected a non-empty value for `auth_context_update_id` but received {auth_context_update_id!r}"
            )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/users/current/auth-context-updates/{auth_context_update_id}/challenge",
            body=await async_maybe_transform(
                body, auth_context_update_challenge_params.AuthContextUpdateChallengeParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class AuthContextUpdatesResourceWithRawResponse:
    def __init__(self, auth_context_updates: AuthContextUpdatesResource) -> None:
        self._auth_context_updates = auth_context_updates

        self.create = to_custom_raw_response_wrapper(
            auth_context_updates.create,
            BinaryAPIResponse,
        )
        self.challenge = to_custom_raw_response_wrapper(
            auth_context_updates.challenge,
            BinaryAPIResponse,
        )


class AsyncAuthContextUpdatesResourceWithRawResponse:
    def __init__(self, auth_context_updates: AsyncAuthContextUpdatesResource) -> None:
        self._auth_context_updates = auth_context_updates

        self.create = async_to_custom_raw_response_wrapper(
            auth_context_updates.create,
            AsyncBinaryAPIResponse,
        )
        self.challenge = async_to_custom_raw_response_wrapper(
            auth_context_updates.challenge,
            AsyncBinaryAPIResponse,
        )


class AuthContextUpdatesResourceWithStreamingResponse:
    def __init__(self, auth_context_updates: AuthContextUpdatesResource) -> None:
        self._auth_context_updates = auth_context_updates

        self.create = to_custom_streamed_response_wrapper(
            auth_context_updates.create,
            StreamedBinaryAPIResponse,
        )
        self.challenge = to_custom_streamed_response_wrapper(
            auth_context_updates.challenge,
            StreamedBinaryAPIResponse,
        )


class AsyncAuthContextUpdatesResourceWithStreamingResponse:
    def __init__(self, auth_context_updates: AsyncAuthContextUpdatesResource) -> None:
        self._auth_context_updates = auth_context_updates

        self.create = async_to_custom_streamed_response_wrapper(
            auth_context_updates.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.challenge = async_to_custom_streamed_response_wrapper(
            auth_context_updates.challenge,
            AsyncStreamedBinaryAPIResponse,
        )
