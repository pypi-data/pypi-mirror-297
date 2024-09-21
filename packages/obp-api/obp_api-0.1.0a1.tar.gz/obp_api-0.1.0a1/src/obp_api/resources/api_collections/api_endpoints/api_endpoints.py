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

__all__ = ["APIEndpointsResource", "AsyncAPIEndpointsResource"]


class APIEndpointsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> APIEndpointsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return APIEndpointsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> APIEndpointsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return APIEndpointsResourceWithStreamingResponse(self)

    def delete(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>glossary-item-not-found<br />Delete Api Collection Endpoint<br />Delete Api Collection Endpoint By Id</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            "/obp/v5.1.0/my/api-collection-ids/API_COLLECTION_ID/api-collection-endpoint-ids/API_COLLECTION_ENDPOINT_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAPIEndpointsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAPIEndpointsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAPIEndpointsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAPIEndpointsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAPIEndpointsResourceWithStreamingResponse(self)

    async def delete(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>glossary-item-not-found<br />Delete Api Collection Endpoint<br />Delete Api Collection Endpoint By Id</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            "/obp/v5.1.0/my/api-collection-ids/API_COLLECTION_ID/api-collection-endpoint-ids/API_COLLECTION_ENDPOINT_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class APIEndpointsResourceWithRawResponse:
    def __init__(self, api_endpoints: APIEndpointsResource) -> None:
        self._api_endpoints = api_endpoints

        self.delete = to_custom_raw_response_wrapper(
            api_endpoints.delete,
            BinaryAPIResponse,
        )


class AsyncAPIEndpointsResourceWithRawResponse:
    def __init__(self, api_endpoints: AsyncAPIEndpointsResource) -> None:
        self._api_endpoints = api_endpoints

        self.delete = async_to_custom_raw_response_wrapper(
            api_endpoints.delete,
            AsyncBinaryAPIResponse,
        )


class APIEndpointsResourceWithStreamingResponse:
    def __init__(self, api_endpoints: APIEndpointsResource) -> None:
        self._api_endpoints = api_endpoints

        self.delete = to_custom_streamed_response_wrapper(
            api_endpoints.delete,
            StreamedBinaryAPIResponse,
        )


class AsyncAPIEndpointsResourceWithStreamingResponse:
    def __init__(self, api_endpoints: AsyncAPIEndpointsResource) -> None:
        self._api_endpoints = api_endpoints

        self.delete = async_to_custom_streamed_response_wrapper(
            api_endpoints.delete,
            AsyncStreamedBinaryAPIResponse,
        )
