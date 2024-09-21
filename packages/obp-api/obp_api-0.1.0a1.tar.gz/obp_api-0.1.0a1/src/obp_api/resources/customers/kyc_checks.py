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
from ...types.customers import kyc_check_update_params

__all__ = ["KYCChecksResource", "AsyncKYCChecksResource"]


class KYCChecksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> KYCChecksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return KYCChecksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> KYCChecksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return KYCChecksResourceWithStreamingResponse(self)

    def update(
        self,
        kyc_check_id: str,
        *,
        bank_id: str,
        customer_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """<p>Add a KYC check for the customer specified by CUSTOMER_ID.

        KYC Checks store details of checks on a customer made by the KYC team, their comments and a satisfied status</p><p>Authentication is Mandatory</p>

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
        if not kyc_check_id:
            raise ValueError(f"Expected a non-empty value for `kyc_check_id` but received {kyc_check_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}/kyc_check/{kyc_check_id}",
            body=maybe_transform(body, kyc_check_update_params.KYCCheckUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
        self,
        customer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get KYC checks for the Customer specified by CUSTOMER_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/customers/{customer_id}/kyc_checks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncKYCChecksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncKYCChecksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncKYCChecksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncKYCChecksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncKYCChecksResourceWithStreamingResponse(self)

    async def update(
        self,
        kyc_check_id: str,
        *,
        bank_id: str,
        customer_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """<p>Add a KYC check for the customer specified by CUSTOMER_ID.

        KYC Checks store details of checks on a customer made by the KYC team, their comments and a satisfied status</p><p>Authentication is Mandatory</p>

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
        if not kyc_check_id:
            raise ValueError(f"Expected a non-empty value for `kyc_check_id` but received {kyc_check_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}/kyc_check/{kyc_check_id}",
            body=await async_maybe_transform(body, kyc_check_update_params.KYCCheckUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
        self,
        customer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get KYC checks for the Customer specified by CUSTOMER_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/customers/{customer_id}/kyc_checks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class KYCChecksResourceWithRawResponse:
    def __init__(self, kyc_checks: KYCChecksResource) -> None:
        self._kyc_checks = kyc_checks

        self.update = to_custom_raw_response_wrapper(
            kyc_checks.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            kyc_checks.list,
            BinaryAPIResponse,
        )


class AsyncKYCChecksResourceWithRawResponse:
    def __init__(self, kyc_checks: AsyncKYCChecksResource) -> None:
        self._kyc_checks = kyc_checks

        self.update = async_to_custom_raw_response_wrapper(
            kyc_checks.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            kyc_checks.list,
            AsyncBinaryAPIResponse,
        )


class KYCChecksResourceWithStreamingResponse:
    def __init__(self, kyc_checks: KYCChecksResource) -> None:
        self._kyc_checks = kyc_checks

        self.update = to_custom_streamed_response_wrapper(
            kyc_checks.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            kyc_checks.list,
            StreamedBinaryAPIResponse,
        )


class AsyncKYCChecksResourceWithStreamingResponse:
    def __init__(self, kyc_checks: AsyncKYCChecksResource) -> None:
        self._kyc_checks = kyc_checks

        self.update = async_to_custom_streamed_response_wrapper(
            kyc_checks.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            kyc_checks.list,
            AsyncStreamedBinaryAPIResponse,
        )
