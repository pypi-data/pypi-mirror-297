# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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

__all__ = ["MetricsResource", "AsyncMetricsResource"]


class MetricsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return MetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return MetricsResourceWithStreamingResponse(self)

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
        <p>Search the API calls made to this API instance via Elastic Search.</p><p>Login is required.</p><p>CanSearchMetrics entitlement is required to search metrics data.</p><p>parameters:</p><p>esType  - elasticsearch type</p><p>simple query:</p><p>q       - plain_text_query</p><p>df      - default field to search</p><p>sort    - field to sort on</p><p>size    - number of hits returned, default 10</p><p>from    - show hits starting from</p><p>json query:</p><p>source  - JSON_query_(URL-escaped)</p><p>example usage:</p><p>/search/metrics/q=findThis</p><p>or:</p><p>/search/metrics/source={&quot;query&quot;:{&quot;query_string&quot;:{&quot;query&quot;:&quot;findThis&quot;}}}</p><p>Note!!</p><p>The whole JSON query string MUST be URL-encoded:</p><ul><li>For {  use %7B</li><li>For }  use %7D</li><li>For : use %3A</li><li>For &quot; use %22</li></ul><p>etc..</p><p>Only q, source and esType are passed to Elastic</p><p>Elastic simple query: <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/search-uri-request.html">https://www.elastic.co/guide/en/elasticsearch/reference/current/search-uri-request.html</a></p><p>Elastic JSON query: <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html">https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html</a></p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/search/metrics",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncMetricsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncMetricsResourceWithStreamingResponse(self)

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
        <p>Search the API calls made to this API instance via Elastic Search.</p><p>Login is required.</p><p>CanSearchMetrics entitlement is required to search metrics data.</p><p>parameters:</p><p>esType  - elasticsearch type</p><p>simple query:</p><p>q       - plain_text_query</p><p>df      - default field to search</p><p>sort    - field to sort on</p><p>size    - number of hits returned, default 10</p><p>from    - show hits starting from</p><p>json query:</p><p>source  - JSON_query_(URL-escaped)</p><p>example usage:</p><p>/search/metrics/q=findThis</p><p>or:</p><p>/search/metrics/source={&quot;query&quot;:{&quot;query_string&quot;:{&quot;query&quot;:&quot;findThis&quot;}}}</p><p>Note!!</p><p>The whole JSON query string MUST be URL-encoded:</p><ul><li>For {  use %7B</li><li>For }  use %7D</li><li>For : use %3A</li><li>For &quot; use %22</li></ul><p>etc..</p><p>Only q, source and esType are passed to Elastic</p><p>Elastic simple query: <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/search-uri-request.html">https://www.elastic.co/guide/en/elasticsearch/reference/current/search-uri-request.html</a></p><p>Elastic JSON query: <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html">https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html</a></p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/search/metrics",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class MetricsResourceWithRawResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

        self.list = to_custom_raw_response_wrapper(
            metrics.list,
            BinaryAPIResponse,
        )


class AsyncMetricsResourceWithRawResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

        self.list = async_to_custom_raw_response_wrapper(
            metrics.list,
            AsyncBinaryAPIResponse,
        )


class MetricsResourceWithStreamingResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

        self.list = to_custom_streamed_response_wrapper(
            metrics.list,
            StreamedBinaryAPIResponse,
        )


class AsyncMetricsResourceWithStreamingResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

        self.list = async_to_custom_streamed_response_wrapper(
            metrics.list,
            AsyncStreamedBinaryAPIResponse,
        )
