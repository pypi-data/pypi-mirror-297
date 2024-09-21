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
from ....types.customers.customer_number_query import overview_flat_retrieve_params

__all__ = ["OverviewFlatResource", "AsyncOverviewFlatResource"]


class OverviewFlatResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OverviewFlatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return OverviewFlatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OverviewFlatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return OverviewFlatResourceWithStreamingResponse(self)

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
        <p>Gets the Customer Overview Flat specified by customer_number and bank_code.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/customers/customer-number-query/overview-flat",
            body=maybe_transform(body, overview_flat_retrieve_params.OverviewFlatRetrieveParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncOverviewFlatResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOverviewFlatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOverviewFlatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOverviewFlatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncOverviewFlatResourceWithStreamingResponse(self)

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
        <p>Gets the Customer Overview Flat specified by customer_number and bank_code.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/customers/customer-number-query/overview-flat",
            body=await async_maybe_transform(body, overview_flat_retrieve_params.OverviewFlatRetrieveParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class OverviewFlatResourceWithRawResponse:
    def __init__(self, overview_flat: OverviewFlatResource) -> None:
        self._overview_flat = overview_flat

        self.retrieve = to_custom_raw_response_wrapper(
            overview_flat.retrieve,
            BinaryAPIResponse,
        )


class AsyncOverviewFlatResourceWithRawResponse:
    def __init__(self, overview_flat: AsyncOverviewFlatResource) -> None:
        self._overview_flat = overview_flat

        self.retrieve = async_to_custom_raw_response_wrapper(
            overview_flat.retrieve,
            AsyncBinaryAPIResponse,
        )


class OverviewFlatResourceWithStreamingResponse:
    def __init__(self, overview_flat: OverviewFlatResource) -> None:
        self._overview_flat = overview_flat

        self.retrieve = to_custom_streamed_response_wrapper(
            overview_flat.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncOverviewFlatResourceWithStreamingResponse:
    def __init__(self, overview_flat: AsyncOverviewFlatResource) -> None:
        self._overview_flat = overview_flat

        self.retrieve = async_to_custom_streamed_response_wrapper(
            overview_flat.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
