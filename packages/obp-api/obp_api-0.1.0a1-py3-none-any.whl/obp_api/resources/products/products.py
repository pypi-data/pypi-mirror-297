# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .fees import (
    FeesResource,
    AsyncFeesResource,
    FeesResourceWithRawResponse,
    AsyncFeesResourceWithRawResponse,
    FeesResourceWithStreamingResponse,
    AsyncFeesResourceWithStreamingResponse,
)
from ...types import product_update_params
from .cascade import (
    CascadeResource,
    AsyncCascadeResource,
    CascadeResourceWithRawResponse,
    AsyncCascadeResourceWithRawResponse,
    CascadeResourceWithStreamingResponse,
    AsyncCascadeResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from .attributes import (
    AttributesResource,
    AsyncAttributesResource,
    AttributesResourceWithRawResponse,
    AsyncAttributesResourceWithRawResponse,
    AttributesResourceWithStreamingResponse,
    AsyncAttributesResourceWithStreamingResponse,
)
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

__all__ = ["ProductsResource", "AsyncProductsResource"]


class ProductsResource(SyncAPIResource):
    @cached_property
    def attributes(self) -> AttributesResource:
        return AttributesResource(self._client)

    @cached_property
    def fees(self) -> FeesResource:
        return FeesResource(self._client)

    @cached_property
    def cascade(self) -> CascadeResource:
        return CascadeResource(self._client)

    @cached_property
    def with_raw_response(self) -> ProductsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ProductsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProductsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ProductsResourceWithStreamingResponse(self)

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
        <p>Returns information about a financial Product offered by the bank specified by BANK_ID and PRODUCT_CODE including:</p><ul><li>Name</li><li>Code</li><li>Parent Product Code</li><li>More info URL</li><li>Description</li><li>Terms and Conditions</li><li>Description</li><li>Meta</li><li>Attributes</li><li>Fees</li></ul><p>Authentication is Optional</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/products/{product_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        product_code: str,
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
        <p>Create or Update Product for the Bank.</p><p>Typical Super Family values / Asset classes are:</p><p>Debt<br />Equity<br />FX<br />Commodity<br />Derivative</p><p>Product hiearchy vs Product Collections:</p><ul><li><p>You can define a hierarchy of products - so that a child Product inherits attributes of its parent Product -  using the parent_product_code in Product.</p></li><li><p>You can define a collection (also known as baskets or buckets) of products using Product Collections.</p></li></ul><p>Authentication is Mandatory</p>

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
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/products/{product_code}",
            body=maybe_transform(body, product_update_params.ProductUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
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
        <p>Returns information about the financial products offered by a bank specified by BANK_ID including:</p><ul><li>Name</li><li>Code</li><li>Parent Product Code</li><li>More info URL</li><li>Terms And Conditions URL</li><li>Description</li><li>Terms and Conditions</li><li>License the data under this endpoint is released under</li></ul><p>Can filter with attributes name and values.<br />URL params example: /banks/some-bank-id/products?manager=John&amp;count=8</p><p>Authentication is Optional</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/products",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncProductsResource(AsyncAPIResource):
    @cached_property
    def attributes(self) -> AsyncAttributesResource:
        return AsyncAttributesResource(self._client)

    @cached_property
    def fees(self) -> AsyncFeesResource:
        return AsyncFeesResource(self._client)

    @cached_property
    def cascade(self) -> AsyncCascadeResource:
        return AsyncCascadeResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncProductsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncProductsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProductsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncProductsResourceWithStreamingResponse(self)

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
        <p>Returns information about a financial Product offered by the bank specified by BANK_ID and PRODUCT_CODE including:</p><ul><li>Name</li><li>Code</li><li>Parent Product Code</li><li>More info URL</li><li>Description</li><li>Terms and Conditions</li><li>Description</li><li>Meta</li><li>Attributes</li><li>Fees</li></ul><p>Authentication is Optional</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/products/{product_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        product_code: str,
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
        <p>Create or Update Product for the Bank.</p><p>Typical Super Family values / Asset classes are:</p><p>Debt<br />Equity<br />FX<br />Commodity<br />Derivative</p><p>Product hiearchy vs Product Collections:</p><ul><li><p>You can define a hierarchy of products - so that a child Product inherits attributes of its parent Product -  using the parent_product_code in Product.</p></li><li><p>You can define a collection (also known as baskets or buckets) of products using Product Collections.</p></li></ul><p>Authentication is Mandatory</p>

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
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/products/{product_code}",
            body=await async_maybe_transform(body, product_update_params.ProductUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
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
        <p>Returns information about the financial products offered by a bank specified by BANK_ID including:</p><ul><li>Name</li><li>Code</li><li>Parent Product Code</li><li>More info URL</li><li>Terms And Conditions URL</li><li>Description</li><li>Terms and Conditions</li><li>License the data under this endpoint is released under</li></ul><p>Can filter with attributes name and values.<br />URL params example: /banks/some-bank-id/products?manager=John&amp;count=8</p><p>Authentication is Optional</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/products",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ProductsResourceWithRawResponse:
    def __init__(self, products: ProductsResource) -> None:
        self._products = products

        self.retrieve = to_custom_raw_response_wrapper(
            products.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            products.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            products.list,
            BinaryAPIResponse,
        )

    @cached_property
    def attributes(self) -> AttributesResourceWithRawResponse:
        return AttributesResourceWithRawResponse(self._products.attributes)

    @cached_property
    def fees(self) -> FeesResourceWithRawResponse:
        return FeesResourceWithRawResponse(self._products.fees)

    @cached_property
    def cascade(self) -> CascadeResourceWithRawResponse:
        return CascadeResourceWithRawResponse(self._products.cascade)


class AsyncProductsResourceWithRawResponse:
    def __init__(self, products: AsyncProductsResource) -> None:
        self._products = products

        self.retrieve = async_to_custom_raw_response_wrapper(
            products.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            products.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            products.list,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def attributes(self) -> AsyncAttributesResourceWithRawResponse:
        return AsyncAttributesResourceWithRawResponse(self._products.attributes)

    @cached_property
    def fees(self) -> AsyncFeesResourceWithRawResponse:
        return AsyncFeesResourceWithRawResponse(self._products.fees)

    @cached_property
    def cascade(self) -> AsyncCascadeResourceWithRawResponse:
        return AsyncCascadeResourceWithRawResponse(self._products.cascade)


class ProductsResourceWithStreamingResponse:
    def __init__(self, products: ProductsResource) -> None:
        self._products = products

        self.retrieve = to_custom_streamed_response_wrapper(
            products.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            products.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            products.list,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def attributes(self) -> AttributesResourceWithStreamingResponse:
        return AttributesResourceWithStreamingResponse(self._products.attributes)

    @cached_property
    def fees(self) -> FeesResourceWithStreamingResponse:
        return FeesResourceWithStreamingResponse(self._products.fees)

    @cached_property
    def cascade(self) -> CascadeResourceWithStreamingResponse:
        return CascadeResourceWithStreamingResponse(self._products.cascade)


class AsyncProductsResourceWithStreamingResponse:
    def __init__(self, products: AsyncProductsResource) -> None:
        self._products = products

        self.retrieve = async_to_custom_streamed_response_wrapper(
            products.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            products.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            products.list,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def attributes(self) -> AsyncAttributesResourceWithStreamingResponse:
        return AsyncAttributesResourceWithStreamingResponse(self._products.attributes)

    @cached_property
    def fees(self) -> AsyncFeesResourceWithStreamingResponse:
        return AsyncFeesResourceWithStreamingResponse(self._products.fees)

    @cached_property
    def cascade(self) -> AsyncCascadeResourceWithStreamingResponse:
        return AsyncCascadeResourceWithStreamingResponse(self._products.cascade)
