# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import product_collection_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["ProductCollectionsResource", "AsyncProductCollectionsResource"]


class ProductCollectionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProductCollectionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ProductCollectionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProductCollectionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ProductCollectionsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        collection_code: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Returns information about the financial Product Collection specified by BANK_ID and COLLECTION_CODE:</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not collection_code:
            raise ValueError(f"Expected a non-empty value for `collection_code` but received {collection_code!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/product-collections/{collection_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        collection_code: str,
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
        <p>Create or Update a Product Collection at the Bank.</p><p>Use Product Collections to create Product &quot;Baskets&quot;, &quot;Portfolios&quot;, &quot;Indices&quot;, &quot;Collections&quot;, &quot;Underlyings-lists&quot;, &quot;Buckets&quot; etc. etc.</p><p>There is a many to many relationship between Products and Product Collections:</p><ul><li><p>A Product can exist in many Collections</p></li><li><p>A Collection can contain many Products.</p></li></ul><p>A collection has collection code, one parent Product and one or more child Products.</p><p>Product hiearchy vs Product Collections:</p><ul><li><p>You can define a hierarchy of products - so that a child Product inherits attributes of its parent Product -  using the parent_product_code in Product.</p></li><li><p>You can define a collection (also known as baskets or buckets) of products using Product Collections.</p></li></ul><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not collection_code:
            raise ValueError(f"Expected a non-empty value for `collection_code` but received {collection_code!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/product-collections/{collection_code}",
            body=maybe_transform(body, product_collection_update_params.ProductCollectionUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncProductCollectionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProductCollectionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncProductCollectionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProductCollectionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncProductCollectionsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        collection_code: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Returns information about the financial Product Collection specified by BANK_ID and COLLECTION_CODE:</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not collection_code:
            raise ValueError(f"Expected a non-empty value for `collection_code` but received {collection_code!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/product-collections/{collection_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        collection_code: str,
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
        <p>Create or Update a Product Collection at the Bank.</p><p>Use Product Collections to create Product &quot;Baskets&quot;, &quot;Portfolios&quot;, &quot;Indices&quot;, &quot;Collections&quot;, &quot;Underlyings-lists&quot;, &quot;Buckets&quot; etc. etc.</p><p>There is a many to many relationship between Products and Product Collections:</p><ul><li><p>A Product can exist in many Collections</p></li><li><p>A Collection can contain many Products.</p></li></ul><p>A collection has collection code, one parent Product and one or more child Products.</p><p>Product hiearchy vs Product Collections:</p><ul><li><p>You can define a hierarchy of products - so that a child Product inherits attributes of its parent Product -  using the parent_product_code in Product.</p></li><li><p>You can define a collection (also known as baskets or buckets) of products using Product Collections.</p></li></ul><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not collection_code:
            raise ValueError(f"Expected a non-empty value for `collection_code` but received {collection_code!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/product-collections/{collection_code}",
            body=await async_maybe_transform(body, product_collection_update_params.ProductCollectionUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ProductCollectionsResourceWithRawResponse:
    def __init__(self, product_collections: ProductCollectionsResource) -> None:
        self._product_collections = product_collections

        self.retrieve = to_custom_raw_response_wrapper(
            product_collections.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            product_collections.update,
            BinaryAPIResponse,
        )


class AsyncProductCollectionsResourceWithRawResponse:
    def __init__(self, product_collections: AsyncProductCollectionsResource) -> None:
        self._product_collections = product_collections

        self.retrieve = async_to_custom_raw_response_wrapper(
            product_collections.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            product_collections.update,
            AsyncBinaryAPIResponse,
        )


class ProductCollectionsResourceWithStreamingResponse:
    def __init__(self, product_collections: ProductCollectionsResource) -> None:
        self._product_collections = product_collections

        self.retrieve = to_custom_streamed_response_wrapper(
            product_collections.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            product_collections.update,
            StreamedBinaryAPIResponse,
        )


class AsyncProductCollectionsResourceWithStreamingResponse:
    def __init__(self, product_collections: AsyncProductCollectionsResource) -> None:
        self._product_collections = product_collections

        self.retrieve = async_to_custom_streamed_response_wrapper(
            product_collections.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            product_collections.update,
            AsyncStreamedBinaryAPIResponse,
        )
