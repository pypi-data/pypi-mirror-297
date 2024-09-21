# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ..._base_client import make_request_options

__all__ = ["PrivateResource", "AsyncPrivateResource"]


class PrivateResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PrivateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return PrivateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PrivateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return PrivateResourceWithStreamingResponse(self)

    def list(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Returns the minimal list of private accounts at BANK_ID that the user has access to.<br />For each account, the API returns the ID, routing addresses and the views available to the current user.</p><p>If you want to see more information on the Views, use the Account Detail call.</p><p>optional request parameters:</p><ul><li>account_type_filter: one or many accountType value, split by comma</li><li>account_type_filter_operation: the filter type of account_type_filter, value must be INCLUDE or EXCLUDE</li></ul><p>whole url example:<br />/banks/BANK_ID/accounts/private?account_type_filter=330,CURRENT+PLUS&amp;account_type_filter_operation=INCLUDE</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/private",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncPrivateResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPrivateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPrivateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPrivateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncPrivateResourceWithStreamingResponse(self)

    async def list(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Returns the minimal list of private accounts at BANK_ID that the user has access to.<br />For each account, the API returns the ID, routing addresses and the views available to the current user.</p><p>If you want to see more information on the Views, use the Account Detail call.</p><p>optional request parameters:</p><ul><li>account_type_filter: one or many accountType value, split by comma</li><li>account_type_filter_operation: the filter type of account_type_filter, value must be INCLUDE or EXCLUDE</li></ul><p>whole url example:<br />/banks/BANK_ID/accounts/private?account_type_filter=330,CURRENT+PLUS&amp;account_type_filter_operation=INCLUDE</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/private",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class PrivateResourceWithRawResponse:
    def __init__(self, private: PrivateResource) -> None:
        self._private = private

        self.list = to_custom_raw_response_wrapper(
            private.list,
            BinaryAPIResponse,
        )


class AsyncPrivateResourceWithRawResponse:
    def __init__(self, private: AsyncPrivateResource) -> None:
        self._private = private

        self.list = async_to_custom_raw_response_wrapper(
            private.list,
            AsyncBinaryAPIResponse,
        )


class PrivateResourceWithStreamingResponse:
    def __init__(self, private: PrivateResource) -> None:
        self._private = private

        self.list = to_custom_streamed_response_wrapper(
            private.list,
            StreamedBinaryAPIResponse,
        )


class AsyncPrivateResourceWithStreamingResponse:
    def __init__(self, private: AsyncPrivateResource) -> None:
        self._private = private

        self.list = async_to_custom_streamed_response_wrapper(
            private.list,
            AsyncStreamedBinaryAPIResponse,
        )
