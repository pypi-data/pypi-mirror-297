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
from ...types.dynamic_resource_docs import endpoint_code_create_params

__all__ = ["EndpointCodeResource", "AsyncEndpointCodeResource"]


class EndpointCodeResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EndpointCodeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return EndpointCodeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EndpointCodeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return EndpointCodeResourceWithStreamingResponse(self)

    def create(
        self,
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
        <p>Create a Dynamic Resource Doc endpoint code.</p><p>copy the response and past to PractiseEndpoint, So you can have the benefits of<br />auto compilation and debug</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/management/dynamic-resource-docs/endpoint-code",
            body=maybe_transform(body, endpoint_code_create_params.EndpointCodeCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncEndpointCodeResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEndpointCodeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEndpointCodeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEndpointCodeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncEndpointCodeResourceWithStreamingResponse(self)

    async def create(
        self,
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
        <p>Create a Dynamic Resource Doc endpoint code.</p><p>copy the response and past to PractiseEndpoint, So you can have the benefits of<br />auto compilation and debug</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/management/dynamic-resource-docs/endpoint-code",
            body=await async_maybe_transform(body, endpoint_code_create_params.EndpointCodeCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class EndpointCodeResourceWithRawResponse:
    def __init__(self, endpoint_code: EndpointCodeResource) -> None:
        self._endpoint_code = endpoint_code

        self.create = to_custom_raw_response_wrapper(
            endpoint_code.create,
            BinaryAPIResponse,
        )


class AsyncEndpointCodeResourceWithRawResponse:
    def __init__(self, endpoint_code: AsyncEndpointCodeResource) -> None:
        self._endpoint_code = endpoint_code

        self.create = async_to_custom_raw_response_wrapper(
            endpoint_code.create,
            AsyncBinaryAPIResponse,
        )


class EndpointCodeResourceWithStreamingResponse:
    def __init__(self, endpoint_code: EndpointCodeResource) -> None:
        self._endpoint_code = endpoint_code

        self.create = to_custom_streamed_response_wrapper(
            endpoint_code.create,
            StreamedBinaryAPIResponse,
        )


class AsyncEndpointCodeResourceWithStreamingResponse:
    def __init__(self, endpoint_code: AsyncEndpointCodeResource) -> None:
        self._endpoint_code = endpoint_code

        self.create = async_to_custom_streamed_response_wrapper(
            endpoint_code.create,
            AsyncStreamedBinaryAPIResponse,
        )
