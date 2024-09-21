# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from .statistics import (
    StatisticsResource,
    AsyncStatisticsResource,
    StatisticsResourceWithRawResponse,
    AsyncStatisticsResourceWithRawResponse,
    StatisticsResourceWithStreamingResponse,
    AsyncStatisticsResourceWithStreamingResponse,
)
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
from ....types.search import warehouse_create_params

__all__ = ["WarehouseResource", "AsyncWarehouseResource"]


class WarehouseResource(SyncAPIResource):
    @cached_property
    def statistics(self) -> StatisticsResource:
        return StatisticsResource(self._client)

    @cached_property
    def with_raw_response(self) -> WarehouseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return WarehouseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WarehouseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return WarehouseResourceWithStreamingResponse(self)

    def create(
        self,
        index: str,
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
        <p>Search the data warehouse and get row level results.</p><p>Authentication is Mandatory</p><p>CanSearchWarehouse entitlement is required. You can request the Role below.</p><p>Elastic (search) is used in the background. See links below for syntax.</p><p>Examples of usage:</p><p>POST /search/warehouse/THE_INDEX_YOU_WANT_TO_USE</p><p>POST /search/warehouse/INDEX1,INDEX2</p><p>POST /search/warehouse/ALL</p><p>{ Any valid elasticsearch query DSL in the body }</p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html">Elasticsearch query DSL</a></p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.2/search-request-body.html">Elastic simple query</a></p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.2/search-aggregations.html">Elastic aggregations</a></p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index:
            raise ValueError(f"Expected a non-empty value for `index` but received {index!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/search/warehouse/{index}",
            body=maybe_transform(body, warehouse_create_params.WarehouseCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncWarehouseResource(AsyncAPIResource):
    @cached_property
    def statistics(self) -> AsyncStatisticsResource:
        return AsyncStatisticsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncWarehouseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWarehouseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWarehouseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncWarehouseResourceWithStreamingResponse(self)

    async def create(
        self,
        index: str,
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
        <p>Search the data warehouse and get row level results.</p><p>Authentication is Mandatory</p><p>CanSearchWarehouse entitlement is required. You can request the Role below.</p><p>Elastic (search) is used in the background. See links below for syntax.</p><p>Examples of usage:</p><p>POST /search/warehouse/THE_INDEX_YOU_WANT_TO_USE</p><p>POST /search/warehouse/INDEX1,INDEX2</p><p>POST /search/warehouse/ALL</p><p>{ Any valid elasticsearch query DSL in the body }</p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html">Elasticsearch query DSL</a></p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.2/search-request-body.html">Elastic simple query</a></p><p><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.2/search-aggregations.html">Elastic aggregations</a></p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index:
            raise ValueError(f"Expected a non-empty value for `index` but received {index!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/search/warehouse/{index}",
            body=await async_maybe_transform(body, warehouse_create_params.WarehouseCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class WarehouseResourceWithRawResponse:
    def __init__(self, warehouse: WarehouseResource) -> None:
        self._warehouse = warehouse

        self.create = to_custom_raw_response_wrapper(
            warehouse.create,
            BinaryAPIResponse,
        )

    @cached_property
    def statistics(self) -> StatisticsResourceWithRawResponse:
        return StatisticsResourceWithRawResponse(self._warehouse.statistics)


class AsyncWarehouseResourceWithRawResponse:
    def __init__(self, warehouse: AsyncWarehouseResource) -> None:
        self._warehouse = warehouse

        self.create = async_to_custom_raw_response_wrapper(
            warehouse.create,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def statistics(self) -> AsyncStatisticsResourceWithRawResponse:
        return AsyncStatisticsResourceWithRawResponse(self._warehouse.statistics)


class WarehouseResourceWithStreamingResponse:
    def __init__(self, warehouse: WarehouseResource) -> None:
        self._warehouse = warehouse

        self.create = to_custom_streamed_response_wrapper(
            warehouse.create,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def statistics(self) -> StatisticsResourceWithStreamingResponse:
        return StatisticsResourceWithStreamingResponse(self._warehouse.statistics)


class AsyncWarehouseResourceWithStreamingResponse:
    def __init__(self, warehouse: AsyncWarehouseResource) -> None:
        self._warehouse = warehouse

        self.create = async_to_custom_streamed_response_wrapper(
            warehouse.create,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def statistics(self) -> AsyncStatisticsResourceWithStreamingResponse:
        return AsyncStatisticsResourceWithStreamingResponse(self._warehouse.statistics)
