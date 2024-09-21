# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ...._base_client import make_request_options

__all__ = ["CounterpartyNamesResource", "AsyncCounterpartyNamesResource"]


class CounterpartyNamesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CounterpartyNamesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CounterpartyNamesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CounterpartyNamesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CounterpartyNamesResourceWithStreamingResponse(self)

    def retrieve(
        self,
        counterparty_name: str,
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
        <p>Authentication is Mandatory</p>

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
        if not counterparty_name:
            raise ValueError(f"Expected a non-empty value for `counterparty_name` but received {counterparty_name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/{view_id}/counterparty-names/{counterparty_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncCounterpartyNamesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCounterpartyNamesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCounterpartyNamesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCounterpartyNamesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCounterpartyNamesResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        counterparty_name: str,
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
        <p>Authentication is Mandatory</p>

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
        if not counterparty_name:
            raise ValueError(f"Expected a non-empty value for `counterparty_name` but received {counterparty_name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/management/banks/{bank_id}/accounts/{account_id}/{view_id}/counterparty-names/{counterparty_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class CounterpartyNamesResourceWithRawResponse:
    def __init__(self, counterparty_names: CounterpartyNamesResource) -> None:
        self._counterparty_names = counterparty_names

        self.retrieve = to_custom_raw_response_wrapper(
            counterparty_names.retrieve,
            BinaryAPIResponse,
        )


class AsyncCounterpartyNamesResourceWithRawResponse:
    def __init__(self, counterparty_names: AsyncCounterpartyNamesResource) -> None:
        self._counterparty_names = counterparty_names

        self.retrieve = async_to_custom_raw_response_wrapper(
            counterparty_names.retrieve,
            AsyncBinaryAPIResponse,
        )


class CounterpartyNamesResourceWithStreamingResponse:
    def __init__(self, counterparty_names: CounterpartyNamesResource) -> None:
        self._counterparty_names = counterparty_names

        self.retrieve = to_custom_streamed_response_wrapper(
            counterparty_names.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncCounterpartyNamesResourceWithStreamingResponse:
    def __init__(self, counterparty_names: AsyncCounterpartyNamesResource) -> None:
        self._counterparty_names = counterparty_names

        self.retrieve = async_to_custom_streamed_response_wrapper(
            counterparty_names.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
