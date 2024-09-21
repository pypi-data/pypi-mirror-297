# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import webui_prop_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
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
from .._base_client import make_request_options

__all__ = ["WebuiPropsResource", "AsyncWebuiPropsResource"]


class WebuiPropsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WebuiPropsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return WebuiPropsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebuiPropsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return WebuiPropsResourceWithStreamingResponse(self)

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
        <p>Create a WebUiProps.</p><p>Authentication is Mandatory</p><p>Explaination of Fields:</p><ul><li>name is required String value</li><li>value is required String value</li></ul><p>The line break and double quotations should do escape, example:</p><pre><code>{&quot;name&quot;: &quot;webui_some&quot;, &quot;value&quot;: &quot;this valuehave &quot;line break&quot; and double quotations.&quot;}</code></pre><p>should do escape like this:</p><pre><code>{&quot;name&quot;: &quot;webui_some&quot;, &quot;value&quot;: &quot;this value\nhave \\&&quot;line break\\&&quot; and double quotations.&quot;}</code></pre><p>Insert image examples:</p><pre><code>// set width=100 and height=50{&quot;name&quot;: &quot;webui_some_pic&quot;, &quot;value&quot;: &quot;here is a picture &lt;img alt=&quot;hello&quot; src=&quot;http://somedomain.com/images/pic.png&quot; width=&quot;100&quot; height=&quot;50&quot; /&gt;&quot;}// only set height=50{&quot;name&quot;: &quot;webui_some_pic&quot;, &quot;value&quot;: &quot;here is a picture &lt;img alt=&quot;hello&quot; src=&quot;http://somedomain.com/images/pic.png&quot; width=&quot;&quot; height=&quot;50&quot; /&gt;&quot;}// only width=20%{&quot;name&quot;: &quot;webui_some_pic&quot;, &quot;value&quot;: &quot;here is a picture &lt;img alt=&quot;hello&quot; src=&quot;http://somedomain.com/images/pic.png&quot; width=&quot;20%&quot; height=&quot;&quot; /&gt;&quot;}</code></pre>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/management/webui_props",
            body=maybe_transform(body, webui_prop_create_params.WebuiPropCreateParams),
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
        <p>Get the all WebUiProps key values, those props key with &quot;webui_&quot; can be stored in DB, this endpoint get all from DB.</p><p>url query parameter:<br />active: It must be a boolean string. and If active = true, it will show<br />combination of explicit (inserted) + implicit (default)  method_routings.</p><p>eg:<br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/management/webui_props">https://apisandbox.openbankproject.com/obp/v3.1.0/management/webui_props</a><br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/management/webui_props?active=true">https://apisandbox.openbankproject.com/obp/v3.1.0/management/webui_props?active=true</a></p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/webui_props",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        web_ui_props_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete a WebUiProps specified by WEB_UI_PROPS_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not web_ui_props_id:
            raise ValueError(f"Expected a non-empty value for `web_ui_props_id` but received {web_ui_props_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/management/webui_props/{web_ui_props_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncWebuiPropsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWebuiPropsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWebuiPropsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebuiPropsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncWebuiPropsResourceWithStreamingResponse(self)

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
        <p>Create a WebUiProps.</p><p>Authentication is Mandatory</p><p>Explaination of Fields:</p><ul><li>name is required String value</li><li>value is required String value</li></ul><p>The line break and double quotations should do escape, example:</p><pre><code>{&quot;name&quot;: &quot;webui_some&quot;, &quot;value&quot;: &quot;this valuehave &quot;line break&quot; and double quotations.&quot;}</code></pre><p>should do escape like this:</p><pre><code>{&quot;name&quot;: &quot;webui_some&quot;, &quot;value&quot;: &quot;this value\nhave \\&&quot;line break\\&&quot; and double quotations.&quot;}</code></pre><p>Insert image examples:</p><pre><code>// set width=100 and height=50{&quot;name&quot;: &quot;webui_some_pic&quot;, &quot;value&quot;: &quot;here is a picture &lt;img alt=&quot;hello&quot; src=&quot;http://somedomain.com/images/pic.png&quot; width=&quot;100&quot; height=&quot;50&quot; /&gt;&quot;}// only set height=50{&quot;name&quot;: &quot;webui_some_pic&quot;, &quot;value&quot;: &quot;here is a picture &lt;img alt=&quot;hello&quot; src=&quot;http://somedomain.com/images/pic.png&quot; width=&quot;&quot; height=&quot;50&quot; /&gt;&quot;}// only width=20%{&quot;name&quot;: &quot;webui_some_pic&quot;, &quot;value&quot;: &quot;here is a picture &lt;img alt=&quot;hello&quot; src=&quot;http://somedomain.com/images/pic.png&quot; width=&quot;20%&quot; height=&quot;&quot; /&gt;&quot;}</code></pre>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/management/webui_props",
            body=await async_maybe_transform(body, webui_prop_create_params.WebuiPropCreateParams),
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
        <p>Get the all WebUiProps key values, those props key with &quot;webui_&quot; can be stored in DB, this endpoint get all from DB.</p><p>url query parameter:<br />active: It must be a boolean string. and If active = true, it will show<br />combination of explicit (inserted) + implicit (default)  method_routings.</p><p>eg:<br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/management/webui_props">https://apisandbox.openbankproject.com/obp/v3.1.0/management/webui_props</a><br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/management/webui_props?active=true">https://apisandbox.openbankproject.com/obp/v3.1.0/management/webui_props?active=true</a></p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/webui_props",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        web_ui_props_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete a WebUiProps specified by WEB_UI_PROPS_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not web_ui_props_id:
            raise ValueError(f"Expected a non-empty value for `web_ui_props_id` but received {web_ui_props_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/management/webui_props/{web_ui_props_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class WebuiPropsResourceWithRawResponse:
    def __init__(self, webui_props: WebuiPropsResource) -> None:
        self._webui_props = webui_props

        self.create = to_custom_raw_response_wrapper(
            webui_props.create,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            webui_props.list,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            webui_props.delete,
        )


class AsyncWebuiPropsResourceWithRawResponse:
    def __init__(self, webui_props: AsyncWebuiPropsResource) -> None:
        self._webui_props = webui_props

        self.create = async_to_custom_raw_response_wrapper(
            webui_props.create,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            webui_props.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            webui_props.delete,
        )


class WebuiPropsResourceWithStreamingResponse:
    def __init__(self, webui_props: WebuiPropsResource) -> None:
        self._webui_props = webui_props

        self.create = to_custom_streamed_response_wrapper(
            webui_props.create,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            webui_props.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            webui_props.delete,
        )


class AsyncWebuiPropsResourceWithStreamingResponse:
    def __init__(self, webui_props: AsyncWebuiPropsResource) -> None:
        self._webui_props = webui_props

        self.create = async_to_custom_streamed_response_wrapper(
            webui_props.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            webui_props.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            webui_props.delete,
        )
