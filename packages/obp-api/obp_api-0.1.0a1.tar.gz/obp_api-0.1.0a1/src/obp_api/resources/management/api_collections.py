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

__all__ = ["APICollectionsResource", "AsyncAPICollectionsResource"]


class APICollectionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> APICollectionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return APICollectionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> APICollectionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return APICollectionsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """<p>Get All API Collections.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/api-collections",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAPICollectionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAPICollectionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAPICollectionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAPICollectionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAPICollectionsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """<p>Get All API Collections.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/api-collections",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class APICollectionsResourceWithRawResponse:
    def __init__(self, api_collections: APICollectionsResource) -> None:
        self._api_collections = api_collections

        self.list = to_custom_raw_response_wrapper(
            api_collections.list,
            BinaryAPIResponse,
        )


class AsyncAPICollectionsResourceWithRawResponse:
    def __init__(self, api_collections: AsyncAPICollectionsResource) -> None:
        self._api_collections = api_collections

        self.list = async_to_custom_raw_response_wrapper(
            api_collections.list,
            AsyncBinaryAPIResponse,
        )


class APICollectionsResourceWithStreamingResponse:
    def __init__(self, api_collections: APICollectionsResource) -> None:
        self._api_collections = api_collections

        self.list = to_custom_streamed_response_wrapper(
            api_collections.list,
            StreamedBinaryAPIResponse,
        )


class AsyncAPICollectionsResourceWithStreamingResponse:
    def __init__(self, api_collections: AsyncAPICollectionsResource) -> None:
        self._api_collections = api_collections

        self.list = async_to_custom_streamed_response_wrapper(
            api_collections.list,
            AsyncStreamedBinaryAPIResponse,
        )
