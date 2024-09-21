# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .ids import (
    IDsResource,
    AsyncIDsResource,
    IDsResourceWithRawResponse,
    AsyncIDsResourceWithRawResponse,
    IDsResourceWithStreamingResponse,
    AsyncIDsResourceWithStreamingResponse,
)
from ...types import system_view_create_params, system_view_update_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["SystemViewsResource", "AsyncSystemViewsResource"]


class SystemViewsResource(SyncAPIResource):
    @cached_property
    def ids(self) -> IDsResource:
        return IDsResource(self._client)

    @cached_property
    def with_raw_response(self) -> SystemViewsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return SystemViewsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SystemViewsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return SystemViewsResourceWithStreamingResponse(self)

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
        <p>Create a system view</p><p>Authentication is Mandatory and the user needs to have access to the CanCreateSystemView entitlement.</p><p>The 'allowed_actions' field is a list containing the names of the actions allowed through this view.<br />All the actions contained in the list will be set to <code>true</code> on the view creation, the rest will be set to <code>false</code>.</p><p>The 'alias' field in the JSON can take one of three values:</p><ul><li><em>public</em>: to use the public alias if there is one specified for the other account.</li><li><em>private</em>: to use the private alias if there is one specified for the other account.</li><li><em>''(empty string)</em>: to use no alias; the view shows the real name of the other account.</li></ul><p>The 'hide_metadata_if_alias_used' field in the JSON can take boolean values. If it is set to <code>true</code> and there is an alias on the other account then the other accounts' metadata (like more_info, url, image_url, open_corporates_url, etc.) will be hidden. Otherwise the metadata will be shown.</p><p>System views cannot be public. In case you try to set it you will get the error OBP-30258: System view cannot be public</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/system-views",
            body=maybe_transform(body, system_view_create_params.SystemViewCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def retrieve(
        self,
        view_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get System View</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not view_id:
            raise ValueError(f"Expected a non-empty value for `view_id` but received {view_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/system-views/{view_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        view_id: str,
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
        <p>Update an existing view on a bank account</p><p>Authentication is Mandatory and the user needs to have access to the owner view.</p><p>The json sent is the same as during view creation (above), with one difference: the 'name' field<br />of a view is not editable (it is only set when a view is created)</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not view_id:
            raise ValueError(f"Expected a non-empty value for `view_id` but received {view_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/system-views/{view_id}",
            body=maybe_transform(body, system_view_update_params.SystemViewUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        view_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Deletes the system view specified by VIEW_ID</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not view_id:
            raise ValueError(f"Expected a non-empty value for `view_id` but received {view_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/system-views/{view_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncSystemViewsResource(AsyncAPIResource):
    @cached_property
    def ids(self) -> AsyncIDsResource:
        return AsyncIDsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSystemViewsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSystemViewsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSystemViewsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncSystemViewsResourceWithStreamingResponse(self)

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
        <p>Create a system view</p><p>Authentication is Mandatory and the user needs to have access to the CanCreateSystemView entitlement.</p><p>The 'allowed_actions' field is a list containing the names of the actions allowed through this view.<br />All the actions contained in the list will be set to <code>true</code> on the view creation, the rest will be set to <code>false</code>.</p><p>The 'alias' field in the JSON can take one of three values:</p><ul><li><em>public</em>: to use the public alias if there is one specified for the other account.</li><li><em>private</em>: to use the private alias if there is one specified for the other account.</li><li><em>''(empty string)</em>: to use no alias; the view shows the real name of the other account.</li></ul><p>The 'hide_metadata_if_alias_used' field in the JSON can take boolean values. If it is set to <code>true</code> and there is an alias on the other account then the other accounts' metadata (like more_info, url, image_url, open_corporates_url, etc.) will be hidden. Otherwise the metadata will be shown.</p><p>System views cannot be public. In case you try to set it you will get the error OBP-30258: System view cannot be public</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/system-views",
            body=await async_maybe_transform(body, system_view_create_params.SystemViewCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def retrieve(
        self,
        view_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get System View</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not view_id:
            raise ValueError(f"Expected a non-empty value for `view_id` but received {view_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/system-views/{view_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        view_id: str,
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
        <p>Update an existing view on a bank account</p><p>Authentication is Mandatory and the user needs to have access to the owner view.</p><p>The json sent is the same as during view creation (above), with one difference: the 'name' field<br />of a view is not editable (it is only set when a view is created)</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not view_id:
            raise ValueError(f"Expected a non-empty value for `view_id` but received {view_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/system-views/{view_id}",
            body=await async_maybe_transform(body, system_view_update_params.SystemViewUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        view_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Deletes the system view specified by VIEW_ID</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not view_id:
            raise ValueError(f"Expected a non-empty value for `view_id` but received {view_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/system-views/{view_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class SystemViewsResourceWithRawResponse:
    def __init__(self, system_views: SystemViewsResource) -> None:
        self._system_views = system_views

        self.create = to_custom_raw_response_wrapper(
            system_views.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            system_views.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            system_views.update,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            system_views.delete,
        )

    @cached_property
    def ids(self) -> IDsResourceWithRawResponse:
        return IDsResourceWithRawResponse(self._system_views.ids)


class AsyncSystemViewsResourceWithRawResponse:
    def __init__(self, system_views: AsyncSystemViewsResource) -> None:
        self._system_views = system_views

        self.create = async_to_custom_raw_response_wrapper(
            system_views.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            system_views.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            system_views.update,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            system_views.delete,
        )

    @cached_property
    def ids(self) -> AsyncIDsResourceWithRawResponse:
        return AsyncIDsResourceWithRawResponse(self._system_views.ids)


class SystemViewsResourceWithStreamingResponse:
    def __init__(self, system_views: SystemViewsResource) -> None:
        self._system_views = system_views

        self.create = to_custom_streamed_response_wrapper(
            system_views.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            system_views.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            system_views.update,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            system_views.delete,
        )

    @cached_property
    def ids(self) -> IDsResourceWithStreamingResponse:
        return IDsResourceWithStreamingResponse(self._system_views.ids)


class AsyncSystemViewsResourceWithStreamingResponse:
    def __init__(self, system_views: AsyncSystemViewsResource) -> None:
        self._system_views = system_views

        self.create = async_to_custom_streamed_response_wrapper(
            system_views.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            system_views.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            system_views.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            system_views.delete,
        )

    @cached_property
    def ids(self) -> AsyncIDsResourceWithStreamingResponse:
        return AsyncIDsResourceWithStreamingResponse(self._system_views.ids)
