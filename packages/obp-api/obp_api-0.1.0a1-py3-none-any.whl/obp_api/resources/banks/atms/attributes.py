# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
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
from ....types.banks.atms import attribute_create_params, attribute_update_params

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
        atm_id: str,
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
        <p>Create ATM Attribute</p><p>The type field must be one of &quot;STRING&quot;, &quot;INTEGER&quot;, &quot;DOUBLE&quot; or DATE_WITH_DAY&quot;</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/attributes",
            body=maybe_transform(body, attribute_create_params.AttributeCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def retrieve(
        self,
        atm_attribute_id: str,
        *,
        bank_id: str,
        atm_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get ATM Attribute By ATM_ATTRIBUTE_ID</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        if not atm_attribute_id:
            raise ValueError(f"Expected a non-empty value for `atm_attribute_id` but received {atm_attribute_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/attributes/{atm_attribute_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        atm_attribute_id: str,
        *,
        bank_id: str,
        atm_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Update ATM Attribute.</p><p>Update an ATM Attribute by its id.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        if not atm_attribute_id:
            raise ValueError(f"Expected a non-empty value for `atm_attribute_id` but received {atm_attribute_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/attributes/{atm_attribute_id}",
            body=maybe_transform(body, attribute_update_params.AttributeUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
        self,
        atm_id: str,
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
        <p>Get ATM Attributes</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/attributes",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        atm_attribute_id: str,
        *,
        bank_id: str,
        atm_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete ATM Attribute</p><p>Delete a Atm Attribute by its id.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        if not atm_attribute_id:
            raise ValueError(f"Expected a non-empty value for `atm_attribute_id` but received {atm_attribute_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/attributes/{atm_attribute_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
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
        atm_id: str,
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
        <p>Create ATM Attribute</p><p>The type field must be one of &quot;STRING&quot;, &quot;INTEGER&quot;, &quot;DOUBLE&quot; or DATE_WITH_DAY&quot;</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/attributes",
            body=await async_maybe_transform(body, attribute_create_params.AttributeCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def retrieve(
        self,
        atm_attribute_id: str,
        *,
        bank_id: str,
        atm_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get ATM Attribute By ATM_ATTRIBUTE_ID</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        if not atm_attribute_id:
            raise ValueError(f"Expected a non-empty value for `atm_attribute_id` but received {atm_attribute_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/attributes/{atm_attribute_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        atm_attribute_id: str,
        *,
        bank_id: str,
        atm_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Update ATM Attribute.</p><p>Update an ATM Attribute by its id.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        if not atm_attribute_id:
            raise ValueError(f"Expected a non-empty value for `atm_attribute_id` but received {atm_attribute_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/attributes/{atm_attribute_id}",
            body=await async_maybe_transform(body, attribute_update_params.AttributeUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
        self,
        atm_id: str,
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
        <p>Get ATM Attributes</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/attributes",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        atm_attribute_id: str,
        *,
        bank_id: str,
        atm_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete ATM Attribute</p><p>Delete a Atm Attribute by its id.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        if not atm_attribute_id:
            raise ValueError(f"Expected a non-empty value for `atm_attribute_id` but received {atm_attribute_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/attributes/{atm_attribute_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AttributesResourceWithRawResponse:
    def __init__(self, attributes: AttributesResource) -> None:
        self._attributes = attributes

        self.create = to_custom_raw_response_wrapper(
            attributes.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            attributes.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            attributes.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            attributes.list,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            attributes.delete,
        )


class AsyncAttributesResourceWithRawResponse:
    def __init__(self, attributes: AsyncAttributesResource) -> None:
        self._attributes = attributes

        self.create = async_to_custom_raw_response_wrapper(
            attributes.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            attributes.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            attributes.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            attributes.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            attributes.delete,
        )


class AttributesResourceWithStreamingResponse:
    def __init__(self, attributes: AttributesResource) -> None:
        self._attributes = attributes

        self.create = to_custom_streamed_response_wrapper(
            attributes.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            attributes.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            attributes.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            attributes.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            attributes.delete,
        )


class AsyncAttributesResourceWithStreamingResponse:
    def __init__(self, attributes: AsyncAttributesResource) -> None:
        self._attributes = attributes

        self.create = async_to_custom_streamed_response_wrapper(
            attributes.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            attributes.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            attributes.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            attributes.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            attributes.delete,
        )
