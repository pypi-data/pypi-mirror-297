# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .scopes import (
    ScopesResource,
    AsyncScopesResource,
    ScopesResourceWithRawResponse,
    AsyncScopesResourceWithRawResponse,
    ScopesResourceWithStreamingResponse,
    AsyncScopesResourceWithStreamingResponse,
)
from ...types import consumer_create_params, consumer_update_params
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
from .call_limits import (
    CallLimitsResource,
    AsyncCallLimitsResource,
    CallLimitsResourceWithRawResponse,
    AsyncCallLimitsResourceWithRawResponse,
    CallLimitsResourceWithStreamingResponse,
    AsyncCallLimitsResourceWithStreamingResponse,
)
from .redirect_url import (
    RedirectURLResource,
    AsyncRedirectURLResource,
    RedirectURLResourceWithRawResponse,
    AsyncRedirectURLResourceWithRawResponse,
    RedirectURLResourceWithStreamingResponse,
    AsyncRedirectURLResourceWithStreamingResponse,
)
from ..._base_client import make_request_options

__all__ = ["ConsumersResource", "AsyncConsumersResource"]


class ConsumersResource(SyncAPIResource):
    @cached_property
    def scopes(self) -> ScopesResource:
        return ScopesResource(self._client)

    @cached_property
    def call_limits(self) -> CallLimitsResource:
        return CallLimitsResource(self._client)

    @cached_property
    def redirect_url(self) -> RedirectURLResource:
        return RedirectURLResource(self._client)

    @cached_property
    def with_raw_response(self) -> ConsumersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ConsumersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConsumersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ConsumersResourceWithStreamingResponse(self)

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
        <p>Create a Consumer (Authenticated access).</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/management/consumers",
            body=maybe_transform(body, consumer_create_params.ConsumerCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def retrieve(
        self,
        consumer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get the Consumer specified by CONSUMER_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not consumer_id:
            raise ValueError(f"Expected a non-empty value for `consumer_id` but received {consumer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/management/consumers/{consumer_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        consumer_id: str,
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
        <p>Enable/Disable a Consumer specified by CONSUMER_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not consumer_id:
            raise ValueError(f"Expected a non-empty value for `consumer_id` but received {consumer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/management/consumers/{consumer_id}",
            body=maybe_transform(body, consumer_update_params.ConsumerUpdateParams),
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
        <p>Get the all Consumers.</p><p>Authentication is Mandatory</p><p>Possible custom url parameters for pagination:</p><ul><li>limit=NUMBER ==&gt; default value: 50</li><li>offset=NUMBER ==&gt; default value: 0</li></ul><p>eg1:?limit=100&amp;offset=0</p><ul><li>sort_direction=ASC/DESC ==&gt; default value: DESC.</li></ul><p>eg2:?limit=100&amp;offset=0&amp;sort_direction=ASC</p><ul><li>from_date=DATE =&gt; example value: 1970-01-01T00:00:00.000Z. NOTE! The default value is one year ago (1970-01-01T00:00:00.000Z).</li><li>to_date=DATE =&gt; example value: 2024-07-25T13:48:58.024Z. NOTE! The default value is now (2024-07-25T13:48:58.024Z).</li></ul><p>Date format parameter: yyyy-MM-dd'T'HH:mm:ss.SSS'Z'(1100-01-01T01:01:01.000Z) ==&gt; time zone is UTC.</p><p>eg3:?sort_direction=ASC&amp;limit=100&amp;offset=0&amp;from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:01.000Z</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/consumers",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncConsumersResource(AsyncAPIResource):
    @cached_property
    def scopes(self) -> AsyncScopesResource:
        return AsyncScopesResource(self._client)

    @cached_property
    def call_limits(self) -> AsyncCallLimitsResource:
        return AsyncCallLimitsResource(self._client)

    @cached_property
    def redirect_url(self) -> AsyncRedirectURLResource:
        return AsyncRedirectURLResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncConsumersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConsumersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConsumersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncConsumersResourceWithStreamingResponse(self)

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
        <p>Create a Consumer (Authenticated access).</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/management/consumers",
            body=await async_maybe_transform(body, consumer_create_params.ConsumerCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def retrieve(
        self,
        consumer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get the Consumer specified by CONSUMER_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not consumer_id:
            raise ValueError(f"Expected a non-empty value for `consumer_id` but received {consumer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/management/consumers/{consumer_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        consumer_id: str,
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
        <p>Enable/Disable a Consumer specified by CONSUMER_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not consumer_id:
            raise ValueError(f"Expected a non-empty value for `consumer_id` but received {consumer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/management/consumers/{consumer_id}",
            body=await async_maybe_transform(body, consumer_update_params.ConsumerUpdateParams),
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
        <p>Get the all Consumers.</p><p>Authentication is Mandatory</p><p>Possible custom url parameters for pagination:</p><ul><li>limit=NUMBER ==&gt; default value: 50</li><li>offset=NUMBER ==&gt; default value: 0</li></ul><p>eg1:?limit=100&amp;offset=0</p><ul><li>sort_direction=ASC/DESC ==&gt; default value: DESC.</li></ul><p>eg2:?limit=100&amp;offset=0&amp;sort_direction=ASC</p><ul><li>from_date=DATE =&gt; example value: 1970-01-01T00:00:00.000Z. NOTE! The default value is one year ago (1970-01-01T00:00:00.000Z).</li><li>to_date=DATE =&gt; example value: 2024-07-25T13:48:58.024Z. NOTE! The default value is now (2024-07-25T13:48:58.024Z).</li></ul><p>Date format parameter: yyyy-MM-dd'T'HH:mm:ss.SSS'Z'(1100-01-01T01:01:01.000Z) ==&gt; time zone is UTC.</p><p>eg3:?sort_direction=ASC&amp;limit=100&amp;offset=0&amp;from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:01.000Z</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/consumers",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ConsumersResourceWithRawResponse:
    def __init__(self, consumers: ConsumersResource) -> None:
        self._consumers = consumers

        self.create = to_custom_raw_response_wrapper(
            consumers.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            consumers.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            consumers.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            consumers.list,
            BinaryAPIResponse,
        )

    @cached_property
    def scopes(self) -> ScopesResourceWithRawResponse:
        return ScopesResourceWithRawResponse(self._consumers.scopes)

    @cached_property
    def call_limits(self) -> CallLimitsResourceWithRawResponse:
        return CallLimitsResourceWithRawResponse(self._consumers.call_limits)

    @cached_property
    def redirect_url(self) -> RedirectURLResourceWithRawResponse:
        return RedirectURLResourceWithRawResponse(self._consumers.redirect_url)


class AsyncConsumersResourceWithRawResponse:
    def __init__(self, consumers: AsyncConsumersResource) -> None:
        self._consumers = consumers

        self.create = async_to_custom_raw_response_wrapper(
            consumers.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            consumers.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            consumers.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            consumers.list,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def scopes(self) -> AsyncScopesResourceWithRawResponse:
        return AsyncScopesResourceWithRawResponse(self._consumers.scopes)

    @cached_property
    def call_limits(self) -> AsyncCallLimitsResourceWithRawResponse:
        return AsyncCallLimitsResourceWithRawResponse(self._consumers.call_limits)

    @cached_property
    def redirect_url(self) -> AsyncRedirectURLResourceWithRawResponse:
        return AsyncRedirectURLResourceWithRawResponse(self._consumers.redirect_url)


class ConsumersResourceWithStreamingResponse:
    def __init__(self, consumers: ConsumersResource) -> None:
        self._consumers = consumers

        self.create = to_custom_streamed_response_wrapper(
            consumers.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            consumers.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            consumers.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            consumers.list,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def scopes(self) -> ScopesResourceWithStreamingResponse:
        return ScopesResourceWithStreamingResponse(self._consumers.scopes)

    @cached_property
    def call_limits(self) -> CallLimitsResourceWithStreamingResponse:
        return CallLimitsResourceWithStreamingResponse(self._consumers.call_limits)

    @cached_property
    def redirect_url(self) -> RedirectURLResourceWithStreamingResponse:
        return RedirectURLResourceWithStreamingResponse(self._consumers.redirect_url)


class AsyncConsumersResourceWithStreamingResponse:
    def __init__(self, consumers: AsyncConsumersResource) -> None:
        self._consumers = consumers

        self.create = async_to_custom_streamed_response_wrapper(
            consumers.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            consumers.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            consumers.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            consumers.list,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def scopes(self) -> AsyncScopesResourceWithStreamingResponse:
        return AsyncScopesResourceWithStreamingResponse(self._consumers.scopes)

    @cached_property
    def call_limits(self) -> AsyncCallLimitsResourceWithStreamingResponse:
        return AsyncCallLimitsResourceWithStreamingResponse(self._consumers.call_limits)

    @cached_property
    def redirect_url(self) -> AsyncRedirectURLResourceWithStreamingResponse:
        return AsyncRedirectURLResourceWithStreamingResponse(self._consumers.redirect_url)
