# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
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
from ...._base_client import make_request_options
from ....types.customers.customer_number_query import overview_retrieve_params

__all__ = ["OverviewResource", "AsyncOverviewResource"]


class OverviewResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OverviewResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return OverviewResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OverviewResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return OverviewResourceWithStreamingResponse(self)

    def retrieve(
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
        <p>Gets the Customer Overview specified by customer_number and bank_code.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/customers/customer-number-query/overview",
            body=maybe_transform(body, overview_retrieve_params.OverviewRetrieveParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncOverviewResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOverviewResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOverviewResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOverviewResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncOverviewResourceWithStreamingResponse(self)

    async def retrieve(
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
        <p>Gets the Customer Overview specified by customer_number and bank_code.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/customers/customer-number-query/overview",
            body=await async_maybe_transform(body, overview_retrieve_params.OverviewRetrieveParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class OverviewResourceWithRawResponse:
    def __init__(self, overview: OverviewResource) -> None:
        self._overview = overview

        self.retrieve = to_custom_raw_response_wrapper(
            overview.retrieve,
            BinaryAPIResponse,
        )


class AsyncOverviewResourceWithRawResponse:
    def __init__(self, overview: AsyncOverviewResource) -> None:
        self._overview = overview

        self.retrieve = async_to_custom_raw_response_wrapper(
            overview.retrieve,
            AsyncBinaryAPIResponse,
        )


class OverviewResourceWithStreamingResponse:
    def __init__(self, overview: OverviewResource) -> None:
        self._overview = overview

        self.retrieve = to_custom_streamed_response_wrapper(
            overview.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncOverviewResourceWithStreamingResponse:
    def __init__(self, overview: AsyncOverviewResource) -> None:
        self._overview = overview

        self.retrieve = async_to_custom_streamed_response_wrapper(
            overview.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
