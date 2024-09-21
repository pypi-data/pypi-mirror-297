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
from ...types.dynamic_registration import consumer_create_params

__all__ = ["ConsumersResource", "AsyncConsumersResource"]


class ConsumersResource(SyncAPIResource):
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
        <p>Create a Consumer (mTLS access).</p><p>JWT payload:<br />- minimal<br />{ &quot;description&quot;:&quot;Description&quot; }<br />- full<br />{<br />&quot;description&quot;: &quot;Description&quot;,<br />&quot;app_name&quot;: &quot;Tesobe GmbH&quot;,<br />&quot;app_type&quot;: &quot;Sofit&quot;,<br />&quot;developer_email&quot;: &quot;<a href="&#109;ai&#x6c;&#x74;&#x6f;&#x3a;&#x6d;&#x61;&#114;&#x6b;&#111;@&#116;&#101;&#115;&#x6f;&#x62;&#101;.&#99;&#x6f;m">&#x6d;&#x61;&#x72;&#107;&#x6f;@&#116;&#101;s&#x6f;&#98;&#101;&#46;&#x63;&#x6f;m</a>&quot;,<br />&quot;redirect_url&quot;: &quot;<a href="http://localhost:8082">http://localhost:8082</a>&quot;<br />}<br />Please note that JWT must be signed with the counterpart private kew of the public key used to establish mTLS</p><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/dynamic-registration/consumers",
            body=maybe_transform(body, consumer_create_params.ConsumerCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncConsumersResource(AsyncAPIResource):
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
        <p>Create a Consumer (mTLS access).</p><p>JWT payload:<br />- minimal<br />{ &quot;description&quot;:&quot;Description&quot; }<br />- full<br />{<br />&quot;description&quot;: &quot;Description&quot;,<br />&quot;app_name&quot;: &quot;Tesobe GmbH&quot;,<br />&quot;app_type&quot;: &quot;Sofit&quot;,<br />&quot;developer_email&quot;: &quot;<a href="&#109;ai&#x6c;&#x74;&#x6f;&#x3a;&#x6d;&#x61;&#114;&#x6b;&#111;@&#116;&#101;&#115;&#x6f;&#x62;&#101;.&#99;&#x6f;m">&#x6d;&#x61;&#x72;&#107;&#x6f;@&#116;&#101;s&#x6f;&#98;&#101;&#46;&#x63;&#x6f;m</a>&quot;,<br />&quot;redirect_url&quot;: &quot;<a href="http://localhost:8082">http://localhost:8082</a>&quot;<br />}<br />Please note that JWT must be signed with the counterpart private kew of the public key used to establish mTLS</p><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/dynamic-registration/consumers",
            body=await async_maybe_transform(body, consumer_create_params.ConsumerCreateParams),
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


class AsyncConsumersResourceWithRawResponse:
    def __init__(self, consumers: AsyncConsumersResource) -> None:
        self._consumers = consumers

        self.create = async_to_custom_raw_response_wrapper(
            consumers.create,
            AsyncBinaryAPIResponse,
        )


class ConsumersResourceWithStreamingResponse:
    def __init__(self, consumers: ConsumersResource) -> None:
        self._consumers = consumers

        self.create = to_custom_streamed_response_wrapper(
            consumers.create,
            StreamedBinaryAPIResponse,
        )


class AsyncConsumersResourceWithStreamingResponse:
    def __init__(self, consumers: AsyncConsumersResource) -> None:
        self._consumers = consumers

        self.create = async_to_custom_streamed_response_wrapper(
            consumers.create,
            AsyncStreamedBinaryAPIResponse,
        )
