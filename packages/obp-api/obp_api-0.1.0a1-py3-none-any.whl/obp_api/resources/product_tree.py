# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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

__all__ = ["ProductTreeResource", "AsyncProductTreeResource"]


class ProductTreeResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProductTreeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ProductTreeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProductTreeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ProductTreeResourceWithStreamingResponse(self)

    def retrieve(
        self,
        product_code: str,
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
        <p>Returns information about a particular financial product specified by BANK_ID and PRODUCT_CODE<br />and it's parent product(s) recursively as specified by parent_product_code.</p><p>Each product includes the following information.</p><ul><li>Name</li><li>Code</li><li>Parent Product Code</li><li>Category</li><li>Family</li><li>Super Family</li><li>More info URL</li><li>Description</li><li>Terms and Conditions</li><li>License: The licence under which this product data is released. Licence can be an Open Data licence such as Open Data Commons Public Domain Dedication and License (PDDL) or Copyright etc.</li></ul><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not product_code:
            raise ValueError(f"Expected a non-empty value for `product_code` but received {product_code!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/product-tree/{product_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncProductTreeResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProductTreeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncProductTreeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProductTreeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncProductTreeResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        product_code: str,
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
        <p>Returns information about a particular financial product specified by BANK_ID and PRODUCT_CODE<br />and it's parent product(s) recursively as specified by parent_product_code.</p><p>Each product includes the following information.</p><ul><li>Name</li><li>Code</li><li>Parent Product Code</li><li>Category</li><li>Family</li><li>Super Family</li><li>More info URL</li><li>Description</li><li>Terms and Conditions</li><li>License: The licence under which this product data is released. Licence can be an Open Data licence such as Open Data Commons Public Domain Dedication and License (PDDL) or Copyright etc.</li></ul><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not product_code:
            raise ValueError(f"Expected a non-empty value for `product_code` but received {product_code!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/product-tree/{product_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ProductTreeResourceWithRawResponse:
    def __init__(self, product_tree: ProductTreeResource) -> None:
        self._product_tree = product_tree

        self.retrieve = to_custom_raw_response_wrapper(
            product_tree.retrieve,
            BinaryAPIResponse,
        )


class AsyncProductTreeResourceWithRawResponse:
    def __init__(self, product_tree: AsyncProductTreeResource) -> None:
        self._product_tree = product_tree

        self.retrieve = async_to_custom_raw_response_wrapper(
            product_tree.retrieve,
            AsyncBinaryAPIResponse,
        )


class ProductTreeResourceWithStreamingResponse:
    def __init__(self, product_tree: ProductTreeResource) -> None:
        self._product_tree = product_tree

        self.retrieve = to_custom_streamed_response_wrapper(
            product_tree.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncProductTreeResourceWithStreamingResponse:
    def __init__(self, product_tree: AsyncProductTreeResource) -> None:
        self._product_tree = product_tree

        self.retrieve = async_to_custom_streamed_response_wrapper(
            product_tree.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
