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
from ..._base_client import make_request_options
from ...types.customers import customer_number_retrieve_params

__all__ = ["CustomerNumberResource", "AsyncCustomerNumberResource"]


class CustomerNumberResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CustomerNumberResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CustomerNumberResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CustomerNumberResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CustomerNumberResourceWithStreamingResponse(self)

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
        <p>Gets the Customer specified by CUSTOMER_NUMBER.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/customers/customer-number",
            body=maybe_transform(body, customer_number_retrieve_params.CustomerNumberRetrieveParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncCustomerNumberResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCustomerNumberResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCustomerNumberResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCustomerNumberResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCustomerNumberResourceWithStreamingResponse(self)

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
        <p>Gets the Customer specified by CUSTOMER_NUMBER.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/customers/customer-number",
            body=await async_maybe_transform(body, customer_number_retrieve_params.CustomerNumberRetrieveParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class CustomerNumberResourceWithRawResponse:
    def __init__(self, customer_number: CustomerNumberResource) -> None:
        self._customer_number = customer_number

        self.retrieve = to_custom_raw_response_wrapper(
            customer_number.retrieve,
            BinaryAPIResponse,
        )


class AsyncCustomerNumberResourceWithRawResponse:
    def __init__(self, customer_number: AsyncCustomerNumberResource) -> None:
        self._customer_number = customer_number

        self.retrieve = async_to_custom_raw_response_wrapper(
            customer_number.retrieve,
            AsyncBinaryAPIResponse,
        )


class CustomerNumberResourceWithStreamingResponse:
    def __init__(self, customer_number: CustomerNumberResource) -> None:
        self._customer_number = customer_number

        self.retrieve = to_custom_streamed_response_wrapper(
            customer_number.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncCustomerNumberResourceWithStreamingResponse:
    def __init__(self, customer_number: AsyncCustomerNumberResource) -> None:
        self._customer_number = customer_number

        self.retrieve = async_to_custom_streamed_response_wrapper(
            customer_number.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
