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
from ...types.customers import credit_rating_and_source_update_params

__all__ = ["CreditRatingAndSourceResource", "AsyncCreditRatingAndSourceResource"]


class CreditRatingAndSourceResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CreditRatingAndSourceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CreditRatingAndSourceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CreditRatingAndSourceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CreditRatingAndSourceResourceWithStreamingResponse(self)

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
        <p>Update the credit rating and source of the Customer specified by CUSTOMER_ID.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}/credit-rating-and-source",
            body=maybe_transform(body, credit_rating_and_source_update_params.CreditRatingAndSourceUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncCreditRatingAndSourceResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCreditRatingAndSourceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCreditRatingAndSourceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCreditRatingAndSourceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCreditRatingAndSourceResourceWithStreamingResponse(self)

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
        <p>Update the credit rating and source of the Customer specified by CUSTOMER_ID.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}/credit-rating-and-source",
            body=await async_maybe_transform(
                body, credit_rating_and_source_update_params.CreditRatingAndSourceUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class CreditRatingAndSourceResourceWithRawResponse:
    def __init__(self, credit_rating_and_source: CreditRatingAndSourceResource) -> None:
        self._credit_rating_and_source = credit_rating_and_source

        self.update = to_custom_raw_response_wrapper(
            credit_rating_and_source.update,
            BinaryAPIResponse,
        )


class AsyncCreditRatingAndSourceResourceWithRawResponse:
    def __init__(self, credit_rating_and_source: AsyncCreditRatingAndSourceResource) -> None:
        self._credit_rating_and_source = credit_rating_and_source

        self.update = async_to_custom_raw_response_wrapper(
            credit_rating_and_source.update,
            AsyncBinaryAPIResponse,
        )


class CreditRatingAndSourceResourceWithStreamingResponse:
    def __init__(self, credit_rating_and_source: CreditRatingAndSourceResource) -> None:
        self._credit_rating_and_source = credit_rating_and_source

        self.update = to_custom_streamed_response_wrapper(
            credit_rating_and_source.update,
            StreamedBinaryAPIResponse,
        )


class AsyncCreditRatingAndSourceResourceWithStreamingResponse:
    def __init__(self, credit_rating_and_source: AsyncCreditRatingAndSourceResource) -> None:
        self._credit_rating_and_source = credit_rating_and_source

        self.update = async_to_custom_streamed_response_wrapper(
            credit_rating_and_source.update,
            AsyncStreamedBinaryAPIResponse,
        )
