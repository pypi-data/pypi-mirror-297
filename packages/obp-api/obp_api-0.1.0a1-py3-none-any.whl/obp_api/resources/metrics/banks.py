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

__all__ = ["BanksResource", "AsyncBanksResource"]


class BanksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BanksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return BanksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BanksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return BanksResourceWithStreamingResponse(self)

    def retrieve(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get the all metrics at the Bank specified by BANK_ID</p><p>require CanReadMetrics role</p><p>Filters Part 1.<em>filtering</em> (no wilde cards etc.) parameters to GET /management/metrics</p><p>Should be able to filter on the following metrics fields</p><p>eg: /management/metrics?from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:01.000Z&amp;limit=50&amp;offset=2</p><p>1 from_date (defaults to one week before current date): eg:from_date=1100-01-01T01:01:01.000Z</p><p>2 to_date (defaults to current date) eg:to_date=1100-01-01T01:01:01.000Z</p><p>3 limit (for pagination: defaults to 50)  eg:limit=200</p><p>4 offset (for pagination: zero index, defaults to 0) eg: offset=10</p><p>5 sort_by (defaults to date field) eg: sort_by=date<br />possible values:<br />&quot;url&quot;,<br />&quot;date&quot;,<br />&quot;user_name&quot;,<br />&quot;app_name&quot;,<br />&quot;developer_email&quot;,<br />&quot;implemented_by_partial_function&quot;,<br />&quot;implemented_in_version&quot;,<br />&quot;consumer_id&quot;,<br />&quot;verb&quot;</p><p>6 direction (defaults to date desc) eg: direction=desc</p><p>eg: /management/metrics?from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:<a href="m&#x61;&#105;&#108;&#x74;&#111;&#58;&#48;&#x31;.&#x30;&#48;0&#x5a;&#x26;&#x6c;&#x69;&#x6d;&#x69;&#116;&#x3d;1&#x30;&#48;&#48;&#x30;&#x26;&#x6f;ff&#115;e&#116;&#x3d;&#48;&#x26;&#x61;&#110;&#x6f;&#110;=&#102;al&#x73;e&#x26;&#x61;&#112;&#x70;_&#110;&#x61;m&#101;&#61;&#x54;e&#x61;&#116;&#65;&#x70;&#x70;&#x26;&#105;&#x6d;&#112;&#108;em&#x65;&#x6e;&#116;&#101;&#x64;&#95;&#105;&#110;&#x5f;&#118;e&#114;s&#105;&#x6f;&#x6e;&#61;v&#x32;.1&#x2e;&#48;&#x26;v&#x65;&#x72;&#98;&#x3d;&#80;&#x4f;&#83;&#84;&#x26;&#x75;&#115;&#x65;&#x72;&#95;id&#x3d;&#x63;&#x37;&#x62;&#x36;cb&#x34;&#x37;&#45;&#99;b&#57;&#54;&#45;4&#x34;&#x34;&#x31;-&#x38;&#56;&#x30;1&#45;&#x33;&#x35;&#x62;&#x35;&#x37;&#x34;&#53;&#54;7&#53;&#x33;&#x61;&#x26;&#x75;&#x73;&#x65;r&#x5f;&#110;&#97;m&#101;&#61;&#115;&#x75;s&#x61;&#x6e;&#x2e;uk&#x2e;2&#x39;&#64;&#x65;&#120;&#97;&#x6d;&#112;&#108;&#x65;&#x2e;&#99;&#x6f;&#x6d;">0&#49;.&#48;&#x30;0Z&#38;&#x6c;&#105;&#x6d;&#105;t=&#x31;&#x30;&#48;&#48;&#x30;&#38;&#111;&#x66;&#102;&#x73;&#101;t=&#48;&#x26;&#97;&#110;&#111;&#110;=&#102;&#97;&#x6c;&#115;&#101;&amp;&#97;&#x70;p_&#110;&#97;&#109;&#x65;&#x3d;T&#x65;&#x61;t&#65;&#112;p&#x26;&#105;&#109;&#112;&#x6c;e&#x6d;&#101;&#110;&#116;&#x65;&#100;&#95;&#105;&#110;_&#118;&#x65;&#x72;&#115;&#105;&#111;&#110;&#x3d;&#118;2&#46;&#x31;&#46;&#48;&amp;&#118;&#101;r&#98;&#x3d;&#80;&#79;&#83;&#x54;&#38;&#117;&#x73;&#x65;r&#x5f;i&#x64;&#61;&#x63;&#x37;&#98;6c&#x62;&#52;&#55;&#x2d;&#99;&#x62;&#57;&#x36;&#x2d;&#52;&#x34;4&#x31;-&#56;&#x38;&#48;&#x31;&#x2d;&#x33;&#x35;&#x62;&#53;&#55;&#x34;5&#54;&#55;&#x35;&#51;&#x61;&#x26;&#117;se&#114;&#x5f;&#110;&#97;m&#101;&#x3d;s&#x75;&#115;&#97;&#x6e;.&#x75;&#107;.&#x32;&#x39;&#64;e&#x78;&#x61;m&#x70;&#x6c;e.&#x63;&#x6f;m</a>&amp;consumer_id=78</p><p>Other filters:</p><p>7 consumer_id  (if null ignore)</p><p>8 user_id (if null ignore)</p><p>9 anon (if null ignore) only support two value : true (return where user_id is null.) or false (return where user_id is not null.)</p><p>10 url (if null ignore), note: can not contain '&amp;'.</p><p>11 app_name (if null ignore)</p><p>12 implemented_by_partial_function (if null ignore),</p><p>13 implemented_in_version (if null ignore)</p><p>14 verb (if null ignore)</p><p>15 correlation_id (if null ignore)</p><p>16 duration (if null ignore) non digit chars will be silently omitted</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/management/metrics/banks/{bank_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncBanksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBanksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBanksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBanksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncBanksResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get the all metrics at the Bank specified by BANK_ID</p><p>require CanReadMetrics role</p><p>Filters Part 1.<em>filtering</em> (no wilde cards etc.) parameters to GET /management/metrics</p><p>Should be able to filter on the following metrics fields</p><p>eg: /management/metrics?from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:01.000Z&amp;limit=50&amp;offset=2</p><p>1 from_date (defaults to one week before current date): eg:from_date=1100-01-01T01:01:01.000Z</p><p>2 to_date (defaults to current date) eg:to_date=1100-01-01T01:01:01.000Z</p><p>3 limit (for pagination: defaults to 50)  eg:limit=200</p><p>4 offset (for pagination: zero index, defaults to 0) eg: offset=10</p><p>5 sort_by (defaults to date field) eg: sort_by=date<br />possible values:<br />&quot;url&quot;,<br />&quot;date&quot;,<br />&quot;user_name&quot;,<br />&quot;app_name&quot;,<br />&quot;developer_email&quot;,<br />&quot;implemented_by_partial_function&quot;,<br />&quot;implemented_in_version&quot;,<br />&quot;consumer_id&quot;,<br />&quot;verb&quot;</p><p>6 direction (defaults to date desc) eg: direction=desc</p><p>eg: /management/metrics?from_date=1100-01-01T01:01:01.000Z&amp;to_date=1100-01-01T01:01:<a href="m&#x61;&#105;&#108;&#x74;&#111;&#58;&#48;&#x31;.&#x30;&#48;0&#x5a;&#x26;&#x6c;&#x69;&#x6d;&#x69;&#116;&#x3d;1&#x30;&#48;&#48;&#x30;&#x26;&#x6f;ff&#115;e&#116;&#x3d;&#48;&#x26;&#x61;&#110;&#x6f;&#110;=&#102;al&#x73;e&#x26;&#x61;&#112;&#x70;_&#110;&#x61;m&#101;&#61;&#x54;e&#x61;&#116;&#65;&#x70;&#x70;&#x26;&#105;&#x6d;&#112;&#108;em&#x65;&#x6e;&#116;&#101;&#x64;&#95;&#105;&#110;&#x5f;&#118;e&#114;s&#105;&#x6f;&#x6e;&#61;v&#x32;.1&#x2e;&#48;&#x26;v&#x65;&#x72;&#98;&#x3d;&#80;&#x4f;&#83;&#84;&#x26;&#x75;&#115;&#x65;&#x72;&#95;id&#x3d;&#x63;&#x37;&#x62;&#x36;cb&#x34;&#x37;&#45;&#99;b&#57;&#54;&#45;4&#x34;&#x34;&#x31;-&#x38;&#56;&#x30;1&#45;&#x33;&#x35;&#x62;&#x35;&#x37;&#x34;&#53;&#54;7&#53;&#x33;&#x61;&#x26;&#x75;&#x73;&#x65;r&#x5f;&#110;&#97;m&#101;&#61;&#115;&#x75;s&#x61;&#x6e;&#x2e;uk&#x2e;2&#x39;&#64;&#x65;&#120;&#97;&#x6d;&#112;&#108;&#x65;&#x2e;&#99;&#x6f;&#x6d;">0&#49;.&#48;&#x30;0Z&#38;&#x6c;&#105;&#x6d;&#105;t=&#x31;&#x30;&#48;&#48;&#x30;&#38;&#111;&#x66;&#102;&#x73;&#101;t=&#48;&#x26;&#97;&#110;&#111;&#110;=&#102;&#97;&#x6c;&#115;&#101;&amp;&#97;&#x70;p_&#110;&#97;&#109;&#x65;&#x3d;T&#x65;&#x61;t&#65;&#112;p&#x26;&#105;&#109;&#112;&#x6c;e&#x6d;&#101;&#110;&#116;&#x65;&#100;&#95;&#105;&#110;_&#118;&#x65;&#x72;&#115;&#105;&#111;&#110;&#x3d;&#118;2&#46;&#x31;&#46;&#48;&amp;&#118;&#101;r&#98;&#x3d;&#80;&#79;&#83;&#x54;&#38;&#117;&#x73;&#x65;r&#x5f;i&#x64;&#61;&#x63;&#x37;&#98;6c&#x62;&#52;&#55;&#x2d;&#99;&#x62;&#57;&#x36;&#x2d;&#52;&#x34;4&#x31;-&#56;&#x38;&#48;&#x31;&#x2d;&#x33;&#x35;&#x62;&#53;&#55;&#x34;5&#54;&#55;&#x35;&#51;&#x61;&#x26;&#117;se&#114;&#x5f;&#110;&#97;m&#101;&#x3d;s&#x75;&#115;&#97;&#x6e;.&#x75;&#107;.&#x32;&#x39;&#64;e&#x78;&#x61;m&#x70;&#x6c;e.&#x63;&#x6f;m</a>&amp;consumer_id=78</p><p>Other filters:</p><p>7 consumer_id  (if null ignore)</p><p>8 user_id (if null ignore)</p><p>9 anon (if null ignore) only support two value : true (return where user_id is null.) or false (return where user_id is not null.)</p><p>10 url (if null ignore), note: can not contain '&amp;'.</p><p>11 app_name (if null ignore)</p><p>12 implemented_by_partial_function (if null ignore),</p><p>13 implemented_in_version (if null ignore)</p><p>14 verb (if null ignore)</p><p>15 correlation_id (if null ignore)</p><p>16 duration (if null ignore) non digit chars will be silently omitted</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/management/metrics/banks/{bank_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class BanksResourceWithRawResponse:
    def __init__(self, banks: BanksResource) -> None:
        self._banks = banks

        self.retrieve = to_custom_raw_response_wrapper(
            banks.retrieve,
            BinaryAPIResponse,
        )


class AsyncBanksResourceWithRawResponse:
    def __init__(self, banks: AsyncBanksResource) -> None:
        self._banks = banks

        self.retrieve = async_to_custom_raw_response_wrapper(
            banks.retrieve,
            AsyncBinaryAPIResponse,
        )


class BanksResourceWithStreamingResponse:
    def __init__(self, banks: BanksResource) -> None:
        self._banks = banks

        self.retrieve = to_custom_streamed_response_wrapper(
            banks.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncBanksResourceWithStreamingResponse:
    def __init__(self, banks: AsyncBanksResource) -> None:
        self._banks = banks

        self.retrieve = async_to_custom_streamed_response_wrapper(
            banks.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
