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
from ...types.banks import account_web_hook_create_params, account_web_hook_update_params
from ..._base_client import make_request_options

__all__ = ["AccountWebHooksResource", "AsyncAccountWebHooksResource"]


class AccountWebHooksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AccountWebHooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AccountWebHooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AccountWebHooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AccountWebHooksResourceWithStreamingResponse(self)

    def create(
        self,
        bank_id: str,
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
        <p>Create an Account Webhook</p><p>Webhooks are used to call external URLs when certain events happen.</p><p>Account Webhooks focus on events around accounts.</p><p>For instance, a webhook could be used to notify an external service if a balance changes on an account.</p><p>This functionality is work in progress! Please note that only implemented trigger is: OnBalanceChange</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/account-web-hooks",
            body=maybe_transform(body, account_web_hook_create_params.AccountWebHookCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        bank_id: str,
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
        <p>Enable/Disable an Account Webhook</p><p>Webhooks are used to call external URLs when certain events happen.</p><p>Account Webhooks focus on events around accounts.</p><p>For instance, a webhook could be used to notify an external service if a balance changes on an account.</p><p>This functionality is work in progress! Please note that only implemented trigger is: OnBalanceChange</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/account-web-hooks",
            body=maybe_transform(body, account_web_hook_update_params.AccountWebHookUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAccountWebHooksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAccountWebHooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAccountWebHooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAccountWebHooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAccountWebHooksResourceWithStreamingResponse(self)

    async def create(
        self,
        bank_id: str,
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
        <p>Create an Account Webhook</p><p>Webhooks are used to call external URLs when certain events happen.</p><p>Account Webhooks focus on events around accounts.</p><p>For instance, a webhook could be used to notify an external service if a balance changes on an account.</p><p>This functionality is work in progress! Please note that only implemented trigger is: OnBalanceChange</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/account-web-hooks",
            body=await async_maybe_transform(body, account_web_hook_create_params.AccountWebHookCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        bank_id: str,
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
        <p>Enable/Disable an Account Webhook</p><p>Webhooks are used to call external URLs when certain events happen.</p><p>Account Webhooks focus on events around accounts.</p><p>For instance, a webhook could be used to notify an external service if a balance changes on an account.</p><p>This functionality is work in progress! Please note that only implemented trigger is: OnBalanceChange</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/account-web-hooks",
            body=await async_maybe_transform(body, account_web_hook_update_params.AccountWebHookUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class AccountWebHooksResourceWithRawResponse:
    def __init__(self, account_web_hooks: AccountWebHooksResource) -> None:
        self._account_web_hooks = account_web_hooks

        self.create = to_custom_raw_response_wrapper(
            account_web_hooks.create,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            account_web_hooks.update,
            BinaryAPIResponse,
        )


class AsyncAccountWebHooksResourceWithRawResponse:
    def __init__(self, account_web_hooks: AsyncAccountWebHooksResource) -> None:
        self._account_web_hooks = account_web_hooks

        self.create = async_to_custom_raw_response_wrapper(
            account_web_hooks.create,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            account_web_hooks.update,
            AsyncBinaryAPIResponse,
        )


class AccountWebHooksResourceWithStreamingResponse:
    def __init__(self, account_web_hooks: AccountWebHooksResource) -> None:
        self._account_web_hooks = account_web_hooks

        self.create = to_custom_streamed_response_wrapper(
            account_web_hooks.create,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            account_web_hooks.update,
            StreamedBinaryAPIResponse,
        )


class AsyncAccountWebHooksResourceWithStreamingResponse:
    def __init__(self, account_web_hooks: AsyncAccountWebHooksResource) -> None:
        self._account_web_hooks = account_web_hooks

        self.create = async_to_custom_streamed_response_wrapper(
            account_web_hooks.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            account_web_hooks.update,
            AsyncStreamedBinaryAPIResponse,
        )
