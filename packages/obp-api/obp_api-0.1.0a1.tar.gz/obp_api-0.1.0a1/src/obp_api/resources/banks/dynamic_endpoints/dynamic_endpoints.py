# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .host import (
    HostResource,
    AsyncHostResource,
    HostResourceWithRawResponse,
    AsyncHostResourceWithRawResponse,
    HostResourceWithStreamingResponse,
    AsyncHostResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...._base_client import make_request_options

__all__ = ["DynamicEndpointsResource", "AsyncDynamicEndpointsResource"]


class DynamicEndpointsResource(SyncAPIResource):
    @cached_property
    def host(self) -> HostResource:
        return HostResource(self._client)

    @cached_property
    def with_raw_response(self) -> DynamicEndpointsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return DynamicEndpointsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DynamicEndpointsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return DynamicEndpointsResourceWithStreamingResponse(self)

    def retrieve(
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
        <p>Get a Bank Level Dynamic Endpoint.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-endpoints/DYNAMIC_ENDPOINT_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete a Bank Level DynamicEndpoint specified by DYNAMIC_ENDPOINT_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-endpoints/DYNAMIC_ENDPOINT_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncDynamicEndpointsResource(AsyncAPIResource):
    @cached_property
    def host(self) -> AsyncHostResource:
        return AsyncHostResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDynamicEndpointsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDynamicEndpointsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDynamicEndpointsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncDynamicEndpointsResourceWithStreamingResponse(self)

    async def retrieve(
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
        <p>Get a Bank Level Dynamic Endpoint.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-endpoints/DYNAMIC_ENDPOINT_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete a Bank Level DynamicEndpoint specified by DYNAMIC_ENDPOINT_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-endpoints/DYNAMIC_ENDPOINT_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class DynamicEndpointsResourceWithRawResponse:
    def __init__(self, dynamic_endpoints: DynamicEndpointsResource) -> None:
        self._dynamic_endpoints = dynamic_endpoints

        self.retrieve = to_custom_raw_response_wrapper(
            dynamic_endpoints.retrieve,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            dynamic_endpoints.delete,
        )

    @cached_property
    def host(self) -> HostResourceWithRawResponse:
        return HostResourceWithRawResponse(self._dynamic_endpoints.host)


class AsyncDynamicEndpointsResourceWithRawResponse:
    def __init__(self, dynamic_endpoints: AsyncDynamicEndpointsResource) -> None:
        self._dynamic_endpoints = dynamic_endpoints

        self.retrieve = async_to_custom_raw_response_wrapper(
            dynamic_endpoints.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            dynamic_endpoints.delete,
        )

    @cached_property
    def host(self) -> AsyncHostResourceWithRawResponse:
        return AsyncHostResourceWithRawResponse(self._dynamic_endpoints.host)


class DynamicEndpointsResourceWithStreamingResponse:
    def __init__(self, dynamic_endpoints: DynamicEndpointsResource) -> None:
        self._dynamic_endpoints = dynamic_endpoints

        self.retrieve = to_custom_streamed_response_wrapper(
            dynamic_endpoints.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            dynamic_endpoints.delete,
        )

    @cached_property
    def host(self) -> HostResourceWithStreamingResponse:
        return HostResourceWithStreamingResponse(self._dynamic_endpoints.host)


class AsyncDynamicEndpointsResourceWithStreamingResponse:
    def __init__(self, dynamic_endpoints: AsyncDynamicEndpointsResource) -> None:
        self._dynamic_endpoints = dynamic_endpoints

        self.retrieve = async_to_custom_streamed_response_wrapper(
            dynamic_endpoints.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            dynamic_endpoints.delete,
        )

    @cached_property
    def host(self) -> AsyncHostResourceWithStreamingResponse:
        return AsyncHostResourceWithStreamingResponse(self._dynamic_endpoints.host)
