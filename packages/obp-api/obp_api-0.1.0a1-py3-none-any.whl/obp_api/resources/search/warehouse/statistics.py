# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.search.warehouse import statistic_create_params

__all__ = ["StatisticsResource", "AsyncStatisticsResource"]


class StatisticsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StatisticsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return StatisticsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StatisticsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return StatisticsResourceWithStreamingResponse(self)

    def create(
        self,
        field: str,
        *,
        index: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Search the data warehouse and get statistical aggregations over a warehouse field</p><p>Does a stats aggregation over some numeric field:</p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-stats-aggregation.html">https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-stats-aggregation.html</a></p><p>Authentication is Mandatory</p><p>CanSearchWarehouseStats Role is required. You can request this below.</p><p>Elastic (search) is used in the background. See links below for syntax.</p><p>Examples of usage:</p><p>POST /search/warehouse/statistics/INDEX/FIELD</p><p>POST /search/warehouse/statistics/ALL/FIELD</p><p>{ Any valid elasticsearch query DSL in the body }</p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html">Elasticsearch query DSL</a></p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.2/search-request-body.html">Elastic simple query</a></p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.2/search-aggregations.html">Elastic aggregations</a></p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index:
            raise ValueError(f"Expected a non-empty value for `index` but received {index!r}")
        if not field:
            raise ValueError(f"Expected a non-empty value for `field` but received {field!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/search/warehouse/statistics/{index}/{field}",
            body=maybe_transform(body, statistic_create_params.StatisticCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncStatisticsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStatisticsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncStatisticsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStatisticsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncStatisticsResourceWithStreamingResponse(self)

    async def create(
        self,
        field: str,
        *,
        index: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Search the data warehouse and get statistical aggregations over a warehouse field</p><p>Does a stats aggregation over some numeric field:</p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-stats-aggregation.html">https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-stats-aggregation.html</a></p><p>Authentication is Mandatory</p><p>CanSearchWarehouseStats Role is required. You can request this below.</p><p>Elastic (search) is used in the background. See links below for syntax.</p><p>Examples of usage:</p><p>POST /search/warehouse/statistics/INDEX/FIELD</p><p>POST /search/warehouse/statistics/ALL/FIELD</p><p>{ Any valid elasticsearch query DSL in the body }</p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html">Elasticsearch query DSL</a></p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.2/search-request-body.html">Elastic simple query</a></p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.2/search-aggregations.html">Elastic aggregations</a></p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index:
            raise ValueError(f"Expected a non-empty value for `index` but received {index!r}")
        if not field:
            raise ValueError(f"Expected a non-empty value for `field` but received {field!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/search/warehouse/statistics/{index}/{field}",
            body=await async_maybe_transform(body, statistic_create_params.StatisticCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class StatisticsResourceWithRawResponse:
    def __init__(self, statistics: StatisticsResource) -> None:
        self._statistics = statistics

        self.create = to_custom_raw_response_wrapper(
            statistics.create,
            BinaryAPIResponse,
        )


class AsyncStatisticsResourceWithRawResponse:
    def __init__(self, statistics: AsyncStatisticsResource) -> None:
        self._statistics = statistics

        self.create = async_to_custom_raw_response_wrapper(
            statistics.create,
            AsyncBinaryAPIResponse,
        )


class StatisticsResourceWithStreamingResponse:
    def __init__(self, statistics: StatisticsResource) -> None:
        self._statistics = statistics

        self.create = to_custom_streamed_response_wrapper(
            statistics.create,
            StreamedBinaryAPIResponse,
        )


class AsyncStatisticsResourceWithStreamingResponse:
    def __init__(self, statistics: AsyncStatisticsResource) -> None:
        self._statistics = statistics

        self.create = async_to_custom_streamed_response_wrapper(
            statistics.create,
            AsyncStreamedBinaryAPIResponse,
        )
