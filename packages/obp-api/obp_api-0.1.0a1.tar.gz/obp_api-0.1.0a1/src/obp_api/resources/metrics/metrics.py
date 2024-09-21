# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .banks import (
    BanksResource,
    AsyncBanksResource,
    BanksResourceWithRawResponse,
    AsyncBanksResourceWithRawResponse,
    BanksResourceWithStreamingResponse,
    AsyncBanksResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .top_apis import (
    TopAPIsResource,
    AsyncTopAPIsResource,
    TopAPIsResourceWithRawResponse,
    AsyncTopAPIsResourceWithRawResponse,
    TopAPIsResourceWithStreamingResponse,
    AsyncTopAPIsResourceWithStreamingResponse,
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
from .top_consumers import (
    TopConsumersResource,
    AsyncTopConsumersResource,
    TopConsumersResourceWithRawResponse,
    AsyncTopConsumersResourceWithRawResponse,
    TopConsumersResourceWithStreamingResponse,
    AsyncTopConsumersResourceWithStreamingResponse,
)
from ..._base_client import make_request_options

__all__ = ["MetricsResource", "AsyncMetricsResource"]


class MetricsResource(SyncAPIResource):
    @cached_property
    def banks(self) -> BanksResource:
        return BanksResource(self._client)

    @cached_property
    def top_apis(self) -> TopAPIsResource:
        return TopAPIsResource(self._client)

    @cached_property
    def top_consumers(self) -> TopConsumersResource:
        return TopConsumersResource(self._client)

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
        """<p>Get API metrics rows.

        These are records of each REST API call.</p><p>require CanReadMetrics role</p><p>Filters Part 1.<em>filtering</em> (no wilde cards etc.) parameters to GET /management/metrics</p><p>You can filter by the following fields by applying url parameters</p><p>eg: /management/metrics?from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:01.000Z&amp;limit=50&amp;offset=2</p><p>1 from_date e.g.:from_date=1100-01-01T01:01:01.000Z Defaults to the Unix Epoch i.e. Thu Jan 01 00:00:00 UTC 1970</p><p>2 to_date e.g.:to_date=1100-01-01T01:01:01.000Z Defaults to a far future date i.e. Sat Jan 01 00:00:00 UTC 4000</p><p>Note: it is recommended you send a valid from_date (e.g. 5 seconds ago) and to_date (now + 1 second) if you want to get the latest records<br />Otherwise you may receive stale cached results.</p><p>3 limit (for pagination: defaults to 50)  eg:limit=200</p><p>4 offset (for pagination: zero index, defaults to 0) eg: offset=10</p><p>5 sort_by (defaults to date field) eg: sort_by=date<br />possible values:<br />&quot;url&quot;,<br />&quot;date&quot;,<br />&quot;user_name&quot;,<br />&quot;app_name&quot;,<br />&quot;developer_email&quot;,<br />&quot;implemented_by_partial_function&quot;,<br />&quot;implemented_in_version&quot;,<br />&quot;consumer_id&quot;,<br />&quot;verb&quot;</p><p>6 direction (defaults to date desc) eg: direction=desc</p><p>eg: /management/metrics?from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:<a href="&#x6d;&#x61;&#x69;&#x6c;&#116;&#x6f;&#x3a;&#48;&#x31;&#x2e;&#48;&#48;&#x30;Z&#x26;&#108;&#105;&#109;it&#61;1&#x30;&#x30;&#48;&#48;&#38;&#x6f;ff&#x73;&#x65;&#116;&#61;0&#x26;&#x61;n&#111;&#110;=false&#38;a&#x70;&#112;_&#x6e;a&#x6d;&#x65;&#x3d;&#84;&#101;&#x61;t&#65;&#112;&#x70;&amp;&#x69;&#x6d;p&#108;&#x65;m&#101;&#x6e;t&#x65;d&#x5f;&#x69;n&#95;&#118;&#x65;&#x72;&#x73;&#x69;&#x6f;&#x6e;&#61;&#118;&#x32;.1&#46;0&amp;&#x76;&#x65;&#x72;&#x62;&#x3d;&#80;O&#83;T&#x26;&#117;s&#x65;&#x72;&#95;&#105;&#x64;&#61;&#99;&#55;b6&#x63;&#98;&#x34;7-&#99;&#x62;&#57;&#54;-&#x34;&#x34;&#52;&#49;&#45;&#x38;&#56;&#48;&#49;&#45;3&#53;&#x62;&#x35;7&#x34;&#53;&#54;&#55;&#x35;&#x33;&#97;&#38;us&#101;&#114;&#95;&#110;&#x61;m&#x65;&#x3d;&#x73;&#117;&#x73;&#97;&#x6e;&#46;u&#x6b;&#x2e;&#50;9&#x40;&#101;&#x78;&#97;&#109;&#x70;&#108;&#x65;&#x2e;&#99;&#x6f;&#109;">&#x30;&#49;&#x2e;&#48;0&#48;Z&#x26;&#108;&#105;&#109;i&#x74;&#x3d;1&#x30;&#48;0&#48;&amp;&#111;&#x66;&#x66;&#115;&#101;&#x74;=&#48;&#38;a&#110;&#111;n&#61;&#102;&#x61;&#108;&#115;&#x65;&amp;&#x61;&#x70;p&#x5f;&#110;&#x61;&#109;&#x65;&#61;&#84;&#x65;a&#116;&#65;&#112;&#x70;&amp;im&#x70;le&#109;e&#110;&#116;ed&#95;&#105;&#110;&#x5f;&#x76;&#x65;&#114;&#x73;&#105;&#111;&#x6e;&#61;&#x76;&#x32;&#x2e;1&#x2e;&#x30;&#x26;&#x76;&#101;&#114;&#98;=P&#x4f;&#x53;&#x54;&amp;&#117;s&#x65;&#x72;_&#105;&#100;=&#99;&#x37;&#x62;&#x36;c&#x62;4&#x37;&#x2d;&#99;&#x62;&#x39;&#54;&#45;&#x34;&#52;&#52;&#49;&#45;8&#x38;0&#49;&#45;&#51;&#x35;&#x62;&#53;745&#x36;&#x37;&#53;&#51;&#97;&#x26;&#x75;&#x73;&#x65;&#x72;&#95;na&#109;&#x65;=&#115;&#x75;&#115;&#97;&#x6e;&#x2e;&#x75;k&#46;&#x32;9&#x40;&#x65;&#120;&#x61;m&#112;l&#101;.&#99;&#x6f;m</a>&amp;consumer_id=78</p><p>Other filters:</p><p>7 consumer_id  (if null ignore)</p><p>8 user_id (if null ignore)</p><p>9 anon (if null ignore) only support two value : true (return where user_id is null.) or false (return where user_id is not null.)</p><p>10 url (if null ignore), note: can not contain '&amp;'.</p><p>11 app_name (if null ignore)</p><p>12 implemented_by_partial_function (if null ignore),</p><p>13 implemented_in_version (if null ignore)</p><p>14 verb (if null ignore)</p><p>15 correlation_id (if null ignore)</p><p>16 duration (if null ignore) non digit chars will be silently omitted</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/metrics",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncMetricsResource(AsyncAPIResource):
    @cached_property
    def banks(self) -> AsyncBanksResource:
        return AsyncBanksResource(self._client)

    @cached_property
    def top_apis(self) -> AsyncTopAPIsResource:
        return AsyncTopAPIsResource(self._client)

    @cached_property
    def top_consumers(self) -> AsyncTopConsumersResource:
        return AsyncTopConsumersResource(self._client)

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
        """<p>Get API metrics rows.

        These are records of each REST API call.</p><p>require CanReadMetrics role</p><p>Filters Part 1.<em>filtering</em> (no wilde cards etc.) parameters to GET /management/metrics</p><p>You can filter by the following fields by applying url parameters</p><p>eg: /management/metrics?from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:01.000Z&amp;limit=50&amp;offset=2</p><p>1 from_date e.g.:from_date=1100-01-01T01:01:01.000Z Defaults to the Unix Epoch i.e. Thu Jan 01 00:00:00 UTC 1970</p><p>2 to_date e.g.:to_date=1100-01-01T01:01:01.000Z Defaults to a far future date i.e. Sat Jan 01 00:00:00 UTC 4000</p><p>Note: it is recommended you send a valid from_date (e.g. 5 seconds ago) and to_date (now + 1 second) if you want to get the latest records<br />Otherwise you may receive stale cached results.</p><p>3 limit (for pagination: defaults to 50)  eg:limit=200</p><p>4 offset (for pagination: zero index, defaults to 0) eg: offset=10</p><p>5 sort_by (defaults to date field) eg: sort_by=date<br />possible values:<br />&quot;url&quot;,<br />&quot;date&quot;,<br />&quot;user_name&quot;,<br />&quot;app_name&quot;,<br />&quot;developer_email&quot;,<br />&quot;implemented_by_partial_function&quot;,<br />&quot;implemented_in_version&quot;,<br />&quot;consumer_id&quot;,<br />&quot;verb&quot;</p><p>6 direction (defaults to date desc) eg: direction=desc</p><p>eg: /management/metrics?from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:<a href="&#x6d;&#x61;&#x69;&#x6c;&#116;&#x6f;&#x3a;&#48;&#x31;&#x2e;&#48;&#48;&#x30;Z&#x26;&#108;&#105;&#109;it&#61;1&#x30;&#x30;&#48;&#48;&#38;&#x6f;ff&#x73;&#x65;&#116;&#61;0&#x26;&#x61;n&#111;&#110;=false&#38;a&#x70;&#112;_&#x6e;a&#x6d;&#x65;&#x3d;&#84;&#101;&#x61;t&#65;&#112;&#x70;&amp;&#x69;&#x6d;p&#108;&#x65;m&#101;&#x6e;t&#x65;d&#x5f;&#x69;n&#95;&#118;&#x65;&#x72;&#x73;&#x69;&#x6f;&#x6e;&#61;&#118;&#x32;.1&#46;0&amp;&#x76;&#x65;&#x72;&#x62;&#x3d;&#80;O&#83;T&#x26;&#117;s&#x65;&#x72;&#95;&#105;&#x64;&#61;&#99;&#55;b6&#x63;&#98;&#x34;7-&#99;&#x62;&#57;&#54;-&#x34;&#x34;&#52;&#49;&#45;&#x38;&#56;&#48;&#49;&#45;3&#53;&#x62;&#x35;7&#x34;&#53;&#54;&#55;&#x35;&#x33;&#97;&#38;us&#101;&#114;&#95;&#110;&#x61;m&#x65;&#x3d;&#x73;&#117;&#x73;&#97;&#x6e;&#46;u&#x6b;&#x2e;&#50;9&#x40;&#101;&#x78;&#97;&#109;&#x70;&#108;&#x65;&#x2e;&#99;&#x6f;&#109;">&#x30;&#49;&#x2e;&#48;0&#48;Z&#x26;&#108;&#105;&#109;i&#x74;&#x3d;1&#x30;&#48;0&#48;&amp;&#111;&#x66;&#x66;&#115;&#101;&#x74;=&#48;&#38;a&#110;&#111;n&#61;&#102;&#x61;&#108;&#115;&#x65;&amp;&#x61;&#x70;p&#x5f;&#110;&#x61;&#109;&#x65;&#61;&#84;&#x65;a&#116;&#65;&#112;&#x70;&amp;im&#x70;le&#109;e&#110;&#116;ed&#95;&#105;&#110;&#x5f;&#x76;&#x65;&#114;&#x73;&#105;&#111;&#x6e;&#61;&#x76;&#x32;&#x2e;1&#x2e;&#x30;&#x26;&#x76;&#101;&#114;&#98;=P&#x4f;&#x53;&#x54;&amp;&#117;s&#x65;&#x72;_&#105;&#100;=&#99;&#x37;&#x62;&#x36;c&#x62;4&#x37;&#x2d;&#99;&#x62;&#x39;&#54;&#45;&#x34;&#52;&#52;&#49;&#45;8&#x38;0&#49;&#45;&#51;&#x35;&#x62;&#53;745&#x36;&#x37;&#53;&#51;&#97;&#x26;&#x75;&#x73;&#x65;&#x72;&#95;na&#109;&#x65;=&#115;&#x75;&#115;&#97;&#x6e;&#x2e;&#x75;k&#46;&#x32;9&#x40;&#x65;&#120;&#x61;m&#112;l&#101;.&#99;&#x6f;m</a>&amp;consumer_id=78</p><p>Other filters:</p><p>7 consumer_id  (if null ignore)</p><p>8 user_id (if null ignore)</p><p>9 anon (if null ignore) only support two value : true (return where user_id is null.) or false (return where user_id is not null.)</p><p>10 url (if null ignore), note: can not contain '&amp;'.</p><p>11 app_name (if null ignore)</p><p>12 implemented_by_partial_function (if null ignore),</p><p>13 implemented_in_version (if null ignore)</p><p>14 verb (if null ignore)</p><p>15 correlation_id (if null ignore)</p><p>16 duration (if null ignore) non digit chars will be silently omitted</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/metrics",
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

    @cached_property
    def banks(self) -> BanksResourceWithRawResponse:
        return BanksResourceWithRawResponse(self._metrics.banks)

    @cached_property
    def top_apis(self) -> TopAPIsResourceWithRawResponse:
        return TopAPIsResourceWithRawResponse(self._metrics.top_apis)

    @cached_property
    def top_consumers(self) -> TopConsumersResourceWithRawResponse:
        return TopConsumersResourceWithRawResponse(self._metrics.top_consumers)


class AsyncMetricsResourceWithRawResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

        self.list = async_to_custom_raw_response_wrapper(
            metrics.list,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def banks(self) -> AsyncBanksResourceWithRawResponse:
        return AsyncBanksResourceWithRawResponse(self._metrics.banks)

    @cached_property
    def top_apis(self) -> AsyncTopAPIsResourceWithRawResponse:
        return AsyncTopAPIsResourceWithRawResponse(self._metrics.top_apis)

    @cached_property
    def top_consumers(self) -> AsyncTopConsumersResourceWithRawResponse:
        return AsyncTopConsumersResourceWithRawResponse(self._metrics.top_consumers)


class MetricsResourceWithStreamingResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

        self.list = to_custom_streamed_response_wrapper(
            metrics.list,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def banks(self) -> BanksResourceWithStreamingResponse:
        return BanksResourceWithStreamingResponse(self._metrics.banks)

    @cached_property
    def top_apis(self) -> TopAPIsResourceWithStreamingResponse:
        return TopAPIsResourceWithStreamingResponse(self._metrics.top_apis)

    @cached_property
    def top_consumers(self) -> TopConsumersResourceWithStreamingResponse:
        return TopConsumersResourceWithStreamingResponse(self._metrics.top_consumers)


class AsyncMetricsResourceWithStreamingResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

        self.list = async_to_custom_streamed_response_wrapper(
            metrics.list,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def banks(self) -> AsyncBanksResourceWithStreamingResponse:
        return AsyncBanksResourceWithStreamingResponse(self._metrics.banks)

    @cached_property
    def top_apis(self) -> AsyncTopAPIsResourceWithStreamingResponse:
        return AsyncTopAPIsResourceWithStreamingResponse(self._metrics.top_apis)

    @cached_property
    def top_consumers(self) -> AsyncTopConsumersResourceWithStreamingResponse:
        return AsyncTopConsumersResourceWithStreamingResponse(self._metrics.top_consumers)
