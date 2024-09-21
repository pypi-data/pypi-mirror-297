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
from ...types.customers import mobile_number_update_params

__all__ = ["MobileNumberResource", "AsyncMobileNumberResource"]


class MobileNumberResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MobileNumberResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return MobileNumberResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MobileNumberResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return MobileNumberResourceWithStreamingResponse(self)

    def update(
        self,
        customer_id: str,
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
        <p>Update the mobile number of the Customer specified by CUSTOMER_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}/mobile-number",
            body=maybe_transform(body, mobile_number_update_params.MobileNumberUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncMobileNumberResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMobileNumberResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMobileNumberResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMobileNumberResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncMobileNumberResourceWithStreamingResponse(self)

    async def update(
        self,
        customer_id: str,
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
        <p>Update the mobile number of the Customer specified by CUSTOMER_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}/mobile-number",
            body=await async_maybe_transform(body, mobile_number_update_params.MobileNumberUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class MobileNumberResourceWithRawResponse:
    def __init__(self, mobile_number: MobileNumberResource) -> None:
        self._mobile_number = mobile_number

        self.update = to_custom_raw_response_wrapper(
            mobile_number.update,
            BinaryAPIResponse,
        )


class AsyncMobileNumberResourceWithRawResponse:
    def __init__(self, mobile_number: AsyncMobileNumberResource) -> None:
        self._mobile_number = mobile_number

        self.update = async_to_custom_raw_response_wrapper(
            mobile_number.update,
            AsyncBinaryAPIResponse,
        )


class MobileNumberResourceWithStreamingResponse:
    def __init__(self, mobile_number: MobileNumberResource) -> None:
        self._mobile_number = mobile_number

        self.update = to_custom_streamed_response_wrapper(
            mobile_number.update,
            StreamedBinaryAPIResponse,
        )


class AsyncMobileNumberResourceWithStreamingResponse:
    def __init__(self, mobile_number: AsyncMobileNumberResource) -> None:
        self._mobile_number = mobile_number

        self.update = async_to_custom_streamed_response_wrapper(
            mobile_number.update,
            AsyncStreamedBinaryAPIResponse,
        )
