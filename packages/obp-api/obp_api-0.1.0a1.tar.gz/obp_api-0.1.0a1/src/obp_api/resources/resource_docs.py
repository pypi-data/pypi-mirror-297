# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["ResourceDocsResource", "AsyncResourceDocsResource"]


class ResourceDocsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ResourceDocsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ResourceDocsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResourceDocsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ResourceDocsResourceWithStreamingResponse(self)

    def list(
        self,
        api_version: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get documentation about the RESTful resources on this server including example bodies for POST and PUT requests.</p><p>This is the native data format used to document OBP endpoints. Each endpoint has a Resource Doc (a Scala case class) defined in the source code.</p><p>This endpoint is used by OBP API Explorer to display and work with the API documentation.</p><p>Most (but not all) fields are also available in swagger format. (The Swagger endpoint is built from Resource Docs.)</p><p>API_VERSION is the version you want documentation about e.g. v3.0.0</p><p>You may filter this endpoint with tags parameter e.g. ?tags=Account,Bank</p><p>You may filter this endpoint with functions parameter e.g. ?functions=enableDisableConsumers,getConnectorMetrics</p><p>For possible function values, see implemented_by.function in the JSON returned by this endpoint or the OBP source code or the footer of the API Explorer which produces a comma separated list of functions that reflect the server or filtering by API Explorer based on tags etc.</p><p>You may filter this endpoint using the 'content' url parameter, e.g. ?content=dynamic<br />if set content=dynamic, only show dynamic endpoints, if content=static, only show the static endpoints. if omit this parameter, we will show all the endpoints.</p><p>You may need some other language resource docs, now we support en_GB and es_ES at the moment.</p><p>You can filter with api-collection-id, but api-collection-id can not be used with others together. If api-collection-id is used in URL, it will ignore all other parameters.</p><p>See the Resource Doc endpoint for more information.</p><p>Note: Dynamic Resource Docs are cached, TTL is 3600 seconds<br />Static Resource Docs are cached, TTL is 3600 seconds</p><p>Following are more examples:<br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp</a><br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?tags=Account,Bank">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?tags=Account,Bank</a><br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?functions=getBanks,bankById">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?functions=getBanks,bankById</a><br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?locale=es_ES">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?locale=es_ES</a><br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?content=static,dynamic,all">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?content=static,dynamic,all</a><br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?api-collection-id=4e866c86-60c3-4268-a221-cb0bbf1ad221">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?api-collection-id=4e866c86-60c3-4268-a221-cb0bbf1ad221</a></p><ul><li> operation_id is concatenation of "v", version and function and should be unique (used for DOM element IDs etc. maybe used to link to source code) </li><li> version references the version that the API call is defined in.</li><li> function is the (scala) partial function that implements this endpoint. It is unique per version of the API.</li><li> request_url is empty for the root call, else the path. It contains the standard prefix (e.g. /obp) and the implemented version (the version where this endpoint was defined) e.g. /obp/v1.2.0/resource</li><li> specified_url (recommended to use) is empty for the root call, else the path. It contains the standard prefix (e.g. /obp) and the version specified in the call e.g. /obp/v3.1.0/resource. In OBP, endpoints are first made available at the request_url, but the same resource (function call) is often made available under later versions (specified_url). To access the latest version of all endpoints use the latest version available on your OBP instance e.g. /obp/v3.1.0 - To get the original version use the request_url. We recommend to use the specified_url since non semantic improvements are more likely to be applied to later implementations of the call.</li><li> summary is a short description inline with the swagger terminology. </li><li> description may contain html markup (generated from markdown on the server).</li></ul><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_version:
            raise ValueError(f"Expected a non-empty value for `api_version` but received {api_version!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/resource-docs/{api_version}/obp",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def swagger(
        self,
        api_version: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Returns documentation about the RESTful resources on this server in Swagger format.</p><p>API_VERSION is the version you want documentation about e.g. v3.0.0</p><p>You may filter this endpoint using the 'tags' url parameter e.g. ?tags=Account,Bank</p><p>(All endpoints are given one or more tags which for used in grouping)</p><p>You may filter this endpoint using the 'functions' url parameter e.g. ?functions=getBanks,bankById</p><p>(Each endpoint is implemented in the OBP Scala code by a 'function')</p><p>See the Resource Doc endpoint for more information.</p><p>Note: Resource Docs are cached, TTL is 3600 seconds</p><p>Following are more examples:<br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger">https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger</a><br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?tags=Account,Bank">https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?tags=Account,Bank</a><br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?functions=getBanks,bankById">https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?functions=getBanks,bankById</a><br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?tags=Account,Bank,PSD2&amp;functions=getBanks,bankById">https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?tags=Account,Bank,PSD2&amp;functions=getBanks,bankById</a></p><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_version:
            raise ValueError(f"Expected a non-empty value for `api_version` but received {api_version!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/resource-docs/{api_version}/swagger",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncResourceDocsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncResourceDocsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncResourceDocsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResourceDocsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncResourceDocsResourceWithStreamingResponse(self)

    async def list(
        self,
        api_version: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get documentation about the RESTful resources on this server including example bodies for POST and PUT requests.</p><p>This is the native data format used to document OBP endpoints. Each endpoint has a Resource Doc (a Scala case class) defined in the source code.</p><p>This endpoint is used by OBP API Explorer to display and work with the API documentation.</p><p>Most (but not all) fields are also available in swagger format. (The Swagger endpoint is built from Resource Docs.)</p><p>API_VERSION is the version you want documentation about e.g. v3.0.0</p><p>You may filter this endpoint with tags parameter e.g. ?tags=Account,Bank</p><p>You may filter this endpoint with functions parameter e.g. ?functions=enableDisableConsumers,getConnectorMetrics</p><p>For possible function values, see implemented_by.function in the JSON returned by this endpoint or the OBP source code or the footer of the API Explorer which produces a comma separated list of functions that reflect the server or filtering by API Explorer based on tags etc.</p><p>You may filter this endpoint using the 'content' url parameter, e.g. ?content=dynamic<br />if set content=dynamic, only show dynamic endpoints, if content=static, only show the static endpoints. if omit this parameter, we will show all the endpoints.</p><p>You may need some other language resource docs, now we support en_GB and es_ES at the moment.</p><p>You can filter with api-collection-id, but api-collection-id can not be used with others together. If api-collection-id is used in URL, it will ignore all other parameters.</p><p>See the Resource Doc endpoint for more information.</p><p>Note: Dynamic Resource Docs are cached, TTL is 3600 seconds<br />Static Resource Docs are cached, TTL is 3600 seconds</p><p>Following are more examples:<br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp</a><br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?tags=Account,Bank">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?tags=Account,Bank</a><br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?functions=getBanks,bankById">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?functions=getBanks,bankById</a><br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?locale=es_ES">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?locale=es_ES</a><br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?content=static,dynamic,all">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?content=static,dynamic,all</a><br /><a href="https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?api-collection-id=4e866c86-60c3-4268-a221-cb0bbf1ad221">https://apisandbox.openbankproject.com/obp/v4.0.0/resource-docs/v4.0.0/obp?api-collection-id=4e866c86-60c3-4268-a221-cb0bbf1ad221</a></p><ul><li> operation_id is concatenation of "v", version and function and should be unique (used for DOM element IDs etc. maybe used to link to source code) </li><li> version references the version that the API call is defined in.</li><li> function is the (scala) partial function that implements this endpoint. It is unique per version of the API.</li><li> request_url is empty for the root call, else the path. It contains the standard prefix (e.g. /obp) and the implemented version (the version where this endpoint was defined) e.g. /obp/v1.2.0/resource</li><li> specified_url (recommended to use) is empty for the root call, else the path. It contains the standard prefix (e.g. /obp) and the version specified in the call e.g. /obp/v3.1.0/resource. In OBP, endpoints are first made available at the request_url, but the same resource (function call) is often made available under later versions (specified_url). To access the latest version of all endpoints use the latest version available on your OBP instance e.g. /obp/v3.1.0 - To get the original version use the request_url. We recommend to use the specified_url since non semantic improvements are more likely to be applied to later implementations of the call.</li><li> summary is a short description inline with the swagger terminology. </li><li> description may contain html markup (generated from markdown on the server).</li></ul><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_version:
            raise ValueError(f"Expected a non-empty value for `api_version` but received {api_version!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/resource-docs/{api_version}/obp",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def swagger(
        self,
        api_version: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Returns documentation about the RESTful resources on this server in Swagger format.</p><p>API_VERSION is the version you want documentation about e.g. v3.0.0</p><p>You may filter this endpoint using the 'tags' url parameter e.g. ?tags=Account,Bank</p><p>(All endpoints are given one or more tags which for used in grouping)</p><p>You may filter this endpoint using the 'functions' url parameter e.g. ?functions=getBanks,bankById</p><p>(Each endpoint is implemented in the OBP Scala code by a 'function')</p><p>See the Resource Doc endpoint for more information.</p><p>Note: Resource Docs are cached, TTL is 3600 seconds</p><p>Following are more examples:<br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger">https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger</a><br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?tags=Account,Bank">https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?tags=Account,Bank</a><br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?functions=getBanks,bankById">https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?functions=getBanks,bankById</a><br /><a href="https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?tags=Account,Bank,PSD2&amp;functions=getBanks,bankById">https://apisandbox.openbankproject.com/obp/v3.1.0/resource-docs/v3.1.0/swagger?tags=Account,Bank,PSD2&amp;functions=getBanks,bankById</a></p><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_version:
            raise ValueError(f"Expected a non-empty value for `api_version` but received {api_version!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/resource-docs/{api_version}/swagger",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ResourceDocsResourceWithRawResponse:
    def __init__(self, resource_docs: ResourceDocsResource) -> None:
        self._resource_docs = resource_docs

        self.list = to_custom_raw_response_wrapper(
            resource_docs.list,
            BinaryAPIResponse,
        )
        self.swagger = to_custom_raw_response_wrapper(
            resource_docs.swagger,
            BinaryAPIResponse,
        )


class AsyncResourceDocsResourceWithRawResponse:
    def __init__(self, resource_docs: AsyncResourceDocsResource) -> None:
        self._resource_docs = resource_docs

        self.list = async_to_custom_raw_response_wrapper(
            resource_docs.list,
            AsyncBinaryAPIResponse,
        )
        self.swagger = async_to_custom_raw_response_wrapper(
            resource_docs.swagger,
            AsyncBinaryAPIResponse,
        )


class ResourceDocsResourceWithStreamingResponse:
    def __init__(self, resource_docs: ResourceDocsResource) -> None:
        self._resource_docs = resource_docs

        self.list = to_custom_streamed_response_wrapper(
            resource_docs.list,
            StreamedBinaryAPIResponse,
        )
        self.swagger = to_custom_streamed_response_wrapper(
            resource_docs.swagger,
            StreamedBinaryAPIResponse,
        )


class AsyncResourceDocsResourceWithStreamingResponse:
    def __init__(self, resource_docs: AsyncResourceDocsResource) -> None:
        self._resource_docs = resource_docs

        self.list = async_to_custom_streamed_response_wrapper(
            resource_docs.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.swagger = async_to_custom_streamed_response_wrapper(
            resource_docs.swagger,
            AsyncStreamedBinaryAPIResponse,
        )
