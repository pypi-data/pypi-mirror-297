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
from ...types.account_products import attribute_create_params, attribute_update_params

__all__ = ["AttributesResource", "AsyncAttributesResource"]


class AttributesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AttributesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AttributesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AttributesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AttributesResourceWithStreamingResponse(self)

    def create(
        self,
        product_code: str,
        *,
        bank_id: str,
        account_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Create Account Attribute</p><p>Account Attributes are used to describe a financial Product with a list of typed key value pairs.</p><p>Each Account Attribute is linked to its Account by ACCOUNT_ID</p><p>Typical account attributes might be:</p><p>ISIN (for International bonds)<br />VKN (for German bonds)<br />REDCODE (markit short code for credit derivative)<br />LOAN_ID (e.g. used for Anacredit reporting)</p><p>ISSUE_DATE (When the bond was issued in the market)<br />MATURITY_DATE (End of life time of a product)<br />TRADABLE</p><p>See <a href="http://www.fpml.org/">FPML</a> for more examples.</p><p>The type field must be one of &quot;STRING&quot;, &quot;INTEGER&quot;, &quot;DOUBLE&quot; or DATE_WITH_DAY&quot;</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not product_code:
            raise ValueError(f"Expected a non-empty value for `product_code` but received {product_code!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/products/{product_code}/attribute",
            body=maybe_transform(body, attribute_create_params.AttributeCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        account_attribute_id: str,
        *,
        bank_id: str,
        account_id: str,
        product_code: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Update Account Attribute</p><p>Account Attributes are used to describe a financial Product with a list of typed key value pairs.</p><p>Each Account Attribute is linked to its Account by ACCOUNT_ID</p><p>Typical account attributes might be:</p><p>ISIN (for International bonds)<br />VKN (for German bonds)<br />REDCODE (markit short code for credit derivative)<br />LOAN_ID (e.g. used for Anacredit reporting)</p><p>ISSUE_DATE (When the bond was issued in the market)<br />MATURITY_DATE (End of life time of a product)<br />TRADABLE</p><p>See <a href="http://www.fpml.org/">FPML</a> for more examples.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not product_code:
            raise ValueError(f"Expected a non-empty value for `product_code` but received {product_code!r}")
        if not account_attribute_id:
            raise ValueError(
                f"Expected a non-empty value for `account_attribute_id` but received {account_attribute_id!r}"
            )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/products/{product_code}/attributes/{account_attribute_id}",
            body=maybe_transform(body, attribute_update_params.AttributeUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAttributesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAttributesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAttributesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAttributesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAttributesResourceWithStreamingResponse(self)

    async def create(
        self,
        product_code: str,
        *,
        bank_id: str,
        account_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Create Account Attribute</p><p>Account Attributes are used to describe a financial Product with a list of typed key value pairs.</p><p>Each Account Attribute is linked to its Account by ACCOUNT_ID</p><p>Typical account attributes might be:</p><p>ISIN (for International bonds)<br />VKN (for German bonds)<br />REDCODE (markit short code for credit derivative)<br />LOAN_ID (e.g. used for Anacredit reporting)</p><p>ISSUE_DATE (When the bond was issued in the market)<br />MATURITY_DATE (End of life time of a product)<br />TRADABLE</p><p>See <a href="http://www.fpml.org/">FPML</a> for more examples.</p><p>The type field must be one of &quot;STRING&quot;, &quot;INTEGER&quot;, &quot;DOUBLE&quot; or DATE_WITH_DAY&quot;</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not product_code:
            raise ValueError(f"Expected a non-empty value for `product_code` but received {product_code!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/products/{product_code}/attribute",
            body=await async_maybe_transform(body, attribute_create_params.AttributeCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        account_attribute_id: str,
        *,
        bank_id: str,
        account_id: str,
        product_code: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Update Account Attribute</p><p>Account Attributes are used to describe a financial Product with a list of typed key value pairs.</p><p>Each Account Attribute is linked to its Account by ACCOUNT_ID</p><p>Typical account attributes might be:</p><p>ISIN (for International bonds)<br />VKN (for German bonds)<br />REDCODE (markit short code for credit derivative)<br />LOAN_ID (e.g. used for Anacredit reporting)</p><p>ISSUE_DATE (When the bond was issued in the market)<br />MATURITY_DATE (End of life time of a product)<br />TRADABLE</p><p>See <a href="http://www.fpml.org/">FPML</a> for more examples.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not product_code:
            raise ValueError(f"Expected a non-empty value for `product_code` but received {product_code!r}")
        if not account_attribute_id:
            raise ValueError(
                f"Expected a non-empty value for `account_attribute_id` but received {account_attribute_id!r}"
            )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/accounts/{account_id}/products/{product_code}/attributes/{account_attribute_id}",
            body=await async_maybe_transform(body, attribute_update_params.AttributeUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class AttributesResourceWithRawResponse:
    def __init__(self, attributes: AttributesResource) -> None:
        self._attributes = attributes

        self.create = to_custom_raw_response_wrapper(
            attributes.create,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            attributes.update,
            BinaryAPIResponse,
        )


class AsyncAttributesResourceWithRawResponse:
    def __init__(self, attributes: AsyncAttributesResource) -> None:
        self._attributes = attributes

        self.create = async_to_custom_raw_response_wrapper(
            attributes.create,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            attributes.update,
            AsyncBinaryAPIResponse,
        )


class AttributesResourceWithStreamingResponse:
    def __init__(self, attributes: AttributesResource) -> None:
        self._attributes = attributes

        self.create = to_custom_streamed_response_wrapper(
            attributes.create,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            attributes.update,
            StreamedBinaryAPIResponse,
        )


class AsyncAttributesResourceWithStreamingResponse:
    def __init__(self, attributes: AsyncAttributesResource) -> None:
        self._attributes = attributes

        self.create = async_to_custom_streamed_response_wrapper(
            attributes.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            attributes.update,
            AsyncStreamedBinaryAPIResponse,
        )
