# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .checkbook import (
    CheckbookResource,
    AsyncCheckbookResource,
    CheckbookResourceWithRawResponse,
    AsyncCheckbookResourceWithRawResponse,
    CheckbookResourceWithStreamingResponse,
    AsyncCheckbookResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from .counterparties import (
    CounterpartiesResource,
    AsyncCounterpartiesResource,
    CounterpartiesResourceWithRawResponse,
    AsyncCounterpartiesResourceWithRawResponse,
    CounterpartiesResourceWithStreamingResponse,
    AsyncCounterpartiesResourceWithStreamingResponse,
)
from ...._base_client import make_request_options
from .counterparties.counterparties import CounterpartiesResource, AsyncCounterpartiesResource

__all__ = ["ViewResource", "AsyncViewResource"]


class ViewResource(SyncAPIResource):
    @cached_property
    def checkbook(self) -> CheckbookResource:
        return CheckbookResource(self._client)

    @cached_property
    def counterparties(self) -> CounterpartiesResource:
        return CounterpartiesResource(self._client)

    @cached_property
    def with_raw_response(self) -> ViewResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ViewResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ViewResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ViewResourceWithStreamingResponse(self)

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
        <p>Information returned about an account specified by ACCOUNT_ID as moderated by the view (VIEW_ID):</p><ul><li>Number</li><li>Owners</li><li>Type</li><li>Balance</li><li>IBAN</li><li>Available views (sorted by short_name)</li></ul><p>More details about the data moderation by the view <a href="#1_2_1-getViewsForBankAccount">here</a>.</p><p>PSD2 Context: PSD2 requires customers to have access to their account information via third party applications.<br />This call provides balance and other account information via delegated authentication using OAuth.</p><p>Authentication is required if the 'is_public' field in view (VIEW_ID) is not set to <code>true</code>.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/account",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncViewResource(AsyncAPIResource):
    @cached_property
    def checkbook(self) -> AsyncCheckbookResource:
        return AsyncCheckbookResource(self._client)

    @cached_property
    def counterparties(self) -> AsyncCounterpartiesResource:
        return AsyncCounterpartiesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncViewResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncViewResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncViewResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncViewResourceWithStreamingResponse(self)

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
        <p>Information returned about an account specified by ACCOUNT_ID as moderated by the view (VIEW_ID):</p><ul><li>Number</li><li>Owners</li><li>Type</li><li>Balance</li><li>IBAN</li><li>Available views (sorted by short_name)</li></ul><p>More details about the data moderation by the view <a href="#1_2_1-getViewsForBankAccount">here</a>.</p><p>PSD2 Context: PSD2 requires customers to have access to their account information via third party applications.<br />This call provides balance and other account information via delegated authentication using OAuth.</p><p>Authentication is required if the 'is_public' field in view (VIEW_ID) is not set to <code>true</code>.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/{view_id}/account",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ViewResourceWithRawResponse:
    def __init__(self, view: ViewResource) -> None:
        self._view = view

        self.retrieve = to_custom_raw_response_wrapper(
            view.retrieve,
            BinaryAPIResponse,
        )

    @cached_property
    def checkbook(self) -> CheckbookResourceWithRawResponse:
        return CheckbookResourceWithRawResponse(self._view.checkbook)

    @cached_property
    def counterparties(self) -> CounterpartiesResourceWithRawResponse:
        return CounterpartiesResourceWithRawResponse(self._view.counterparties)


class AsyncViewResourceWithRawResponse:
    def __init__(self, view: AsyncViewResource) -> None:
        self._view = view

        self.retrieve = async_to_custom_raw_response_wrapper(
            view.retrieve,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def checkbook(self) -> AsyncCheckbookResourceWithRawResponse:
        return AsyncCheckbookResourceWithRawResponse(self._view.checkbook)

    @cached_property
    def counterparties(self) -> AsyncCounterpartiesResourceWithRawResponse:
        return AsyncCounterpartiesResourceWithRawResponse(self._view.counterparties)


class ViewResourceWithStreamingResponse:
    def __init__(self, view: ViewResource) -> None:
        self._view = view

        self.retrieve = to_custom_streamed_response_wrapper(
            view.retrieve,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def checkbook(self) -> CheckbookResourceWithStreamingResponse:
        return CheckbookResourceWithStreamingResponse(self._view.checkbook)

    @cached_property
    def counterparties(self) -> CounterpartiesResourceWithStreamingResponse:
        return CounterpartiesResourceWithStreamingResponse(self._view.counterparties)


class AsyncViewResourceWithStreamingResponse:
    def __init__(self, view: AsyncViewResource) -> None:
        self._view = view

        self.retrieve = async_to_custom_streamed_response_wrapper(
            view.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def checkbook(self) -> AsyncCheckbookResourceWithStreamingResponse:
        return AsyncCheckbookResourceWithStreamingResponse(self._view.checkbook)

    @cached_property
    def counterparties(self) -> AsyncCounterpartiesResourceWithStreamingResponse:
        return AsyncCounterpartiesResourceWithStreamingResponse(self._view.counterparties)
