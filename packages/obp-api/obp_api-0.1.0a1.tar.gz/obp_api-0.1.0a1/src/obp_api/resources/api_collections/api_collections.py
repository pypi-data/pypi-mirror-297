# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import api_collection_create_params, api_collection_update_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .featured import (
    FeaturedResource,
    AsyncFeaturedResource,
    FeaturedResourceWithRawResponse,
    AsyncFeaturedResourceWithRawResponse,
    FeaturedResourceWithStreamingResponse,
    AsyncFeaturedResourceWithStreamingResponse,
)
from .sharable import (
    SharableResource,
    AsyncSharableResource,
    SharableResourceWithRawResponse,
    AsyncSharableResourceWithRawResponse,
    SharableResourceWithStreamingResponse,
    AsyncSharableResourceWithStreamingResponse,
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
from .api_endpoints import (
    APIEndpointsResource,
    AsyncAPIEndpointsResource,
    APIEndpointsResourceWithRawResponse,
    AsyncAPIEndpointsResourceWithRawResponse,
    APIEndpointsResourceWithStreamingResponse,
    AsyncAPIEndpointsResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from .api_collection_endpoints import (
    APICollectionEndpointsResource,
    AsyncAPICollectionEndpointsResource,
    APICollectionEndpointsResourceWithRawResponse,
    AsyncAPICollectionEndpointsResourceWithRawResponse,
    APICollectionEndpointsResourceWithStreamingResponse,
    AsyncAPICollectionEndpointsResourceWithStreamingResponse,
)
from .api_endpoints.api_endpoints import APIEndpointsResource, AsyncAPIEndpointsResource

__all__ = ["APICollectionsResource", "AsyncAPICollectionsResource"]


class APICollectionsResource(SyncAPIResource):
    @cached_property
    def api_collection_endpoints(self) -> APICollectionEndpointsResource:
        return APICollectionEndpointsResource(self._client)

    @cached_property
    def featured(self) -> FeaturedResource:
        return FeaturedResource(self._client)

    @cached_property
    def sharable(self) -> SharableResource:
        return SharableResource(self._client)

    @cached_property
    def api_endpoints(self) -> APIEndpointsResource:
        return APIEndpointsResource(self._client)

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
        <p>Create Api Collection for logged in user.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/my/api-collections",
            body=maybe_transform(body, api_collection_create_params.APICollectionCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def retrieve(
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
        <p>Get Api Collection By API_COLLECTION_NAME.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/my/api-collections/name/API_COLLECTION_NAME",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
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
        <p>Update Api Collection for logged in user.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/obp/v5.1.0/my/api-collections/API_COLLECTION_ID",
            body=maybe_transform(body, api_collection_update_params.APICollectionUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

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
        """
        <p>Get all the apiCollections for logged in user.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/my/api-collections",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

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
        <p>Delete Api Collection By API_COLLECTION_ID</p><p>glossary-item-not-found</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            "/obp/v5.1.0/my/api-collections/API_COLLECTION_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAPICollectionsResource(AsyncAPIResource):
    @cached_property
    def api_collection_endpoints(self) -> AsyncAPICollectionEndpointsResource:
        return AsyncAPICollectionEndpointsResource(self._client)

    @cached_property
    def featured(self) -> AsyncFeaturedResource:
        return AsyncFeaturedResource(self._client)

    @cached_property
    def sharable(self) -> AsyncSharableResource:
        return AsyncSharableResource(self._client)

    @cached_property
    def api_endpoints(self) -> AsyncAPIEndpointsResource:
        return AsyncAPIEndpointsResource(self._client)

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
        <p>Create Api Collection for logged in user.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/my/api-collections",
            body=await async_maybe_transform(body, api_collection_create_params.APICollectionCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def retrieve(
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
        <p>Get Api Collection By API_COLLECTION_NAME.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/my/api-collections/name/API_COLLECTION_NAME",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
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
        <p>Update Api Collection for logged in user.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/obp/v5.1.0/my/api-collections/API_COLLECTION_ID",
            body=await async_maybe_transform(body, api_collection_update_params.APICollectionUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

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
        """
        <p>Get all the apiCollections for logged in user.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/my/api-collections",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

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
        <p>Delete Api Collection By API_COLLECTION_ID</p><p>glossary-item-not-found</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            "/obp/v5.1.0/my/api-collections/API_COLLECTION_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class APICollectionsResourceWithRawResponse:
    def __init__(self, api_collections: APICollectionsResource) -> None:
        self._api_collections = api_collections

        self.create = to_custom_raw_response_wrapper(
            api_collections.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            api_collections.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            api_collections.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            api_collections.list,
            BinaryAPIResponse,
        )
        self.delete = to_custom_raw_response_wrapper(
            api_collections.delete,
            BinaryAPIResponse,
        )

    @cached_property
    def api_collection_endpoints(self) -> APICollectionEndpointsResourceWithRawResponse:
        return APICollectionEndpointsResourceWithRawResponse(self._api_collections.api_collection_endpoints)

    @cached_property
    def featured(self) -> FeaturedResourceWithRawResponse:
        return FeaturedResourceWithRawResponse(self._api_collections.featured)

    @cached_property
    def sharable(self) -> SharableResourceWithRawResponse:
        return SharableResourceWithRawResponse(self._api_collections.sharable)

    @cached_property
    def api_endpoints(self) -> APIEndpointsResourceWithRawResponse:
        return APIEndpointsResourceWithRawResponse(self._api_collections.api_endpoints)


class AsyncAPICollectionsResourceWithRawResponse:
    def __init__(self, api_collections: AsyncAPICollectionsResource) -> None:
        self._api_collections = api_collections

        self.create = async_to_custom_raw_response_wrapper(
            api_collections.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            api_collections.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            api_collections.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            api_collections.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_custom_raw_response_wrapper(
            api_collections.delete,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def api_collection_endpoints(self) -> AsyncAPICollectionEndpointsResourceWithRawResponse:
        return AsyncAPICollectionEndpointsResourceWithRawResponse(self._api_collections.api_collection_endpoints)

    @cached_property
    def featured(self) -> AsyncFeaturedResourceWithRawResponse:
        return AsyncFeaturedResourceWithRawResponse(self._api_collections.featured)

    @cached_property
    def sharable(self) -> AsyncSharableResourceWithRawResponse:
        return AsyncSharableResourceWithRawResponse(self._api_collections.sharable)

    @cached_property
    def api_endpoints(self) -> AsyncAPIEndpointsResourceWithRawResponse:
        return AsyncAPIEndpointsResourceWithRawResponse(self._api_collections.api_endpoints)


class APICollectionsResourceWithStreamingResponse:
    def __init__(self, api_collections: APICollectionsResource) -> None:
        self._api_collections = api_collections

        self.create = to_custom_streamed_response_wrapper(
            api_collections.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            api_collections.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            api_collections.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            api_collections.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_custom_streamed_response_wrapper(
            api_collections.delete,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def api_collection_endpoints(self) -> APICollectionEndpointsResourceWithStreamingResponse:
        return APICollectionEndpointsResourceWithStreamingResponse(self._api_collections.api_collection_endpoints)

    @cached_property
    def featured(self) -> FeaturedResourceWithStreamingResponse:
        return FeaturedResourceWithStreamingResponse(self._api_collections.featured)

    @cached_property
    def sharable(self) -> SharableResourceWithStreamingResponse:
        return SharableResourceWithStreamingResponse(self._api_collections.sharable)

    @cached_property
    def api_endpoints(self) -> APIEndpointsResourceWithStreamingResponse:
        return APIEndpointsResourceWithStreamingResponse(self._api_collections.api_endpoints)


class AsyncAPICollectionsResourceWithStreamingResponse:
    def __init__(self, api_collections: AsyncAPICollectionsResource) -> None:
        self._api_collections = api_collections

        self.create = async_to_custom_streamed_response_wrapper(
            api_collections.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            api_collections.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            api_collections.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            api_collections.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_custom_streamed_response_wrapper(
            api_collections.delete,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def api_collection_endpoints(self) -> AsyncAPICollectionEndpointsResourceWithStreamingResponse:
        return AsyncAPICollectionEndpointsResourceWithStreamingResponse(self._api_collections.api_collection_endpoints)

    @cached_property
    def featured(self) -> AsyncFeaturedResourceWithStreamingResponse:
        return AsyncFeaturedResourceWithStreamingResponse(self._api_collections.featured)

    @cached_property
    def sharable(self) -> AsyncSharableResourceWithStreamingResponse:
        return AsyncSharableResourceWithStreamingResponse(self._api_collections.sharable)

    @cached_property
    def api_endpoints(self) -> AsyncAPIEndpointsResourceWithStreamingResponse:
        return AsyncAPIEndpointsResourceWithStreamingResponse(self._api_collections.api_endpoints)
