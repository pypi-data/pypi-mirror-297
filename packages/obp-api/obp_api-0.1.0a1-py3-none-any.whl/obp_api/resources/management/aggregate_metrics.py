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

__all__ = ["AggregateMetricsResource", "AsyncAggregateMetricsResource"]


class AggregateMetricsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AggregateMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AggregateMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AggregateMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AggregateMetricsResourceWithStreamingResponse(self)

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
        """<p>Returns aggregate metrics on api usage eg.

        total count, response time (in ms), etc.</p><p>Should be able to filter on the following fields</p><p>eg: /management/aggregate-metrics?from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:01.000Z&amp;consumer_id=5<br />&amp;user_id=66214b8e-259e-44ad-8868-3eb47be70646&amp;implemented_by_partial_function=getTransactionsForBankAccount<br />&amp;implemented_in_version=v3.0.0&amp;url=/obp/v3.0.0/banks/gh.29.uk/accounts/8ca8a7e4-6d02-48e3-a029-0b2bf89de9f0/owner/transactions<br />&amp;verb=GET&amp;anon=false&amp;app_name=MapperPostman<br />&amp;exclude_app_names=API-EXPLORER,API-Manager,SOFI,null</p><p>1 from_date (defaults to the day before the current date): eg:from_date=1100-01-01T01:01:01.000Z</p><p>2 to_date (defaults to the current date) eg:to_date=1100-01-01T01:01:01.000Z</p><p>3 consumer_id  (if null ignore)</p><p>4 user_id (if null ignore)</p><p>5 anon (if null ignore) only support two value : true (return where user_id is null.) or false (return where user_id is not null.)</p><p>6 url (if null ignore), note: can not contain '&amp;'.</p><p>7 app_name (if null ignore)</p><p>8 implemented_by_partial_function (if null ignore),</p><p>9 implemented_in_version (if null ignore)</p><p>10 verb (if null ignore)</p><p>11 correlation_id (if null ignore)</p><p>12 include_app_names (if null ignore).eg: &amp;include_app_names=API-EXPLORER,API-Manager,SOFI,null</p><p>13 include_url_patterns (if null ignore).you can design you own SQL LIKE pattern. eg: &amp;include_url_patterns=%management/metrics%,%management/aggregate-metrics%</p><p>14 include_implemented_by_partial_functions (if null ignore).eg: &amp;include_implemented_by_partial_functions=getMetrics,getConnectorMetrics,getAggregateMetrics</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/aggregate-metrics",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAggregateMetricsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAggregateMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAggregateMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAggregateMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAggregateMetricsResourceWithStreamingResponse(self)

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
        """<p>Returns aggregate metrics on api usage eg.

        total count, response time (in ms), etc.</p><p>Should be able to filter on the following fields</p><p>eg: /management/aggregate-metrics?from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:01.000Z&amp;consumer_id=5<br />&amp;user_id=66214b8e-259e-44ad-8868-3eb47be70646&amp;implemented_by_partial_function=getTransactionsForBankAccount<br />&amp;implemented_in_version=v3.0.0&amp;url=/obp/v3.0.0/banks/gh.29.uk/accounts/8ca8a7e4-6d02-48e3-a029-0b2bf89de9f0/owner/transactions<br />&amp;verb=GET&amp;anon=false&amp;app_name=MapperPostman<br />&amp;exclude_app_names=API-EXPLORER,API-Manager,SOFI,null</p><p>1 from_date (defaults to the day before the current date): eg:from_date=1100-01-01T01:01:01.000Z</p><p>2 to_date (defaults to the current date) eg:to_date=1100-01-01T01:01:01.000Z</p><p>3 consumer_id  (if null ignore)</p><p>4 user_id (if null ignore)</p><p>5 anon (if null ignore) only support two value : true (return where user_id is null.) or false (return where user_id is not null.)</p><p>6 url (if null ignore), note: can not contain '&amp;'.</p><p>7 app_name (if null ignore)</p><p>8 implemented_by_partial_function (if null ignore),</p><p>9 implemented_in_version (if null ignore)</p><p>10 verb (if null ignore)</p><p>11 correlation_id (if null ignore)</p><p>12 include_app_names (if null ignore).eg: &amp;include_app_names=API-EXPLORER,API-Manager,SOFI,null</p><p>13 include_url_patterns (if null ignore).you can design you own SQL LIKE pattern. eg: &amp;include_url_patterns=%management/metrics%,%management/aggregate-metrics%</p><p>14 include_implemented_by_partial_functions (if null ignore).eg: &amp;include_implemented_by_partial_functions=getMetrics,getConnectorMetrics,getAggregateMetrics</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/aggregate-metrics",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class AggregateMetricsResourceWithRawResponse:
    def __init__(self, aggregate_metrics: AggregateMetricsResource) -> None:
        self._aggregate_metrics = aggregate_metrics

        self.list = to_custom_raw_response_wrapper(
            aggregate_metrics.list,
            BinaryAPIResponse,
        )


class AsyncAggregateMetricsResourceWithRawResponse:
    def __init__(self, aggregate_metrics: AsyncAggregateMetricsResource) -> None:
        self._aggregate_metrics = aggregate_metrics

        self.list = async_to_custom_raw_response_wrapper(
            aggregate_metrics.list,
            AsyncBinaryAPIResponse,
        )


class AggregateMetricsResourceWithStreamingResponse:
    def __init__(self, aggregate_metrics: AggregateMetricsResource) -> None:
        self._aggregate_metrics = aggregate_metrics

        self.list = to_custom_streamed_response_wrapper(
            aggregate_metrics.list,
            StreamedBinaryAPIResponse,
        )


class AsyncAggregateMetricsResourceWithStreamingResponse:
    def __init__(self, aggregate_metrics: AsyncAggregateMetricsResource) -> None:
        self._aggregate_metrics = aggregate_metrics

        self.list = async_to_custom_streamed_response_wrapper(
            aggregate_metrics.list,
            AsyncStreamedBinaryAPIResponse,
        )
