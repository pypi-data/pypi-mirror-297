# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import dynamic_resource_doc_create_params, dynamic_resource_doc_update_params
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
from .endpoint_code import (
    EndpointCodeResource,
    AsyncEndpointCodeResource,
    EndpointCodeResourceWithRawResponse,
    AsyncEndpointCodeResourceWithRawResponse,
    EndpointCodeResourceWithStreamingResponse,
    AsyncEndpointCodeResourceWithStreamingResponse,
)
from ..._base_client import make_request_options

__all__ = ["DynamicResourceDocsResource", "AsyncDynamicResourceDocsResource"]


class DynamicResourceDocsResource(SyncAPIResource):
    @cached_property
    def endpoint_code(self) -> EndpointCodeResource:
        return EndpointCodeResource(self._client)

    @cached_property
    def with_raw_response(self) -> DynamicResourceDocsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return DynamicResourceDocsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DynamicResourceDocsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return DynamicResourceDocsResourceWithStreamingResponse(self)

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
        <p>Create a Dynamic Resource Doc.</p><p>The connector_method_body is URL-encoded format String</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/management/dynamic-resource-docs",
            body=maybe_transform(body, dynamic_resource_doc_create_params.DynamicResourceDocCreateParams),
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
        <p>Get a Dynamic Resource Doc by DYNAMIC-RESOURCE-DOC-ID.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID",
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
        <p>Update a Dynamic Resource Doc.</p><p>The connector_method_body is URL-encoded format String</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID",
            body=maybe_transform(body, dynamic_resource_doc_update_params.DynamicResourceDocUpdateParams),
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
        """<p>Get all Dynamic Resource Docs.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/dynamic-resource-docs",
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
        """<p>Delete a Dynamic Resource Doc.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            "/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncDynamicResourceDocsResource(AsyncAPIResource):
    @cached_property
    def endpoint_code(self) -> AsyncEndpointCodeResource:
        return AsyncEndpointCodeResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDynamicResourceDocsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDynamicResourceDocsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDynamicResourceDocsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncDynamicResourceDocsResourceWithStreamingResponse(self)

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
        <p>Create a Dynamic Resource Doc.</p><p>The connector_method_body is URL-encoded format String</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/management/dynamic-resource-docs",
            body=await async_maybe_transform(body, dynamic_resource_doc_create_params.DynamicResourceDocCreateParams),
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
        <p>Get a Dynamic Resource Doc by DYNAMIC-RESOURCE-DOC-ID.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID",
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
        <p>Update a Dynamic Resource Doc.</p><p>The connector_method_body is URL-encoded format String</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID",
            body=await async_maybe_transform(body, dynamic_resource_doc_update_params.DynamicResourceDocUpdateParams),
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
        """<p>Get all Dynamic Resource Docs.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/dynamic-resource-docs",
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
        """<p>Delete a Dynamic Resource Doc.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            "/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class DynamicResourceDocsResourceWithRawResponse:
    def __init__(self, dynamic_resource_docs: DynamicResourceDocsResource) -> None:
        self._dynamic_resource_docs = dynamic_resource_docs

        self.create = to_custom_raw_response_wrapper(
            dynamic_resource_docs.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            dynamic_resource_docs.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            dynamic_resource_docs.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            dynamic_resource_docs.list,
            BinaryAPIResponse,
        )
        self.delete = to_custom_raw_response_wrapper(
            dynamic_resource_docs.delete,
            BinaryAPIResponse,
        )

    @cached_property
    def endpoint_code(self) -> EndpointCodeResourceWithRawResponse:
        return EndpointCodeResourceWithRawResponse(self._dynamic_resource_docs.endpoint_code)


class AsyncDynamicResourceDocsResourceWithRawResponse:
    def __init__(self, dynamic_resource_docs: AsyncDynamicResourceDocsResource) -> None:
        self._dynamic_resource_docs = dynamic_resource_docs

        self.create = async_to_custom_raw_response_wrapper(
            dynamic_resource_docs.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            dynamic_resource_docs.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            dynamic_resource_docs.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            dynamic_resource_docs.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_custom_raw_response_wrapper(
            dynamic_resource_docs.delete,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def endpoint_code(self) -> AsyncEndpointCodeResourceWithRawResponse:
        return AsyncEndpointCodeResourceWithRawResponse(self._dynamic_resource_docs.endpoint_code)


class DynamicResourceDocsResourceWithStreamingResponse:
    def __init__(self, dynamic_resource_docs: DynamicResourceDocsResource) -> None:
        self._dynamic_resource_docs = dynamic_resource_docs

        self.create = to_custom_streamed_response_wrapper(
            dynamic_resource_docs.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            dynamic_resource_docs.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            dynamic_resource_docs.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            dynamic_resource_docs.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_custom_streamed_response_wrapper(
            dynamic_resource_docs.delete,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def endpoint_code(self) -> EndpointCodeResourceWithStreamingResponse:
        return EndpointCodeResourceWithStreamingResponse(self._dynamic_resource_docs.endpoint_code)


class AsyncDynamicResourceDocsResourceWithStreamingResponse:
    def __init__(self, dynamic_resource_docs: AsyncDynamicResourceDocsResource) -> None:
        self._dynamic_resource_docs = dynamic_resource_docs

        self.create = async_to_custom_streamed_response_wrapper(
            dynamic_resource_docs.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            dynamic_resource_docs.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            dynamic_resource_docs.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            dynamic_resource_docs.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_custom_streamed_response_wrapper(
            dynamic_resource_docs.delete,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def endpoint_code(self) -> AsyncEndpointCodeResourceWithStreamingResponse:
        return AsyncEndpointCodeResourceWithStreamingResponse(self._dynamic_resource_docs.endpoint_code)
