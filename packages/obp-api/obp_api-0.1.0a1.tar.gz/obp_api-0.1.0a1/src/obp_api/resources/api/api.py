# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .glossary import (
    GlossaryResource,
    AsyncGlossaryResource,
    GlossaryResourceWithRawResponse,
    AsyncGlossaryResourceWithRawResponse,
    GlossaryResourceWithStreamingResponse,
    AsyncGlossaryResourceWithStreamingResponse,
)
from .versions import (
    VersionsResource,
    AsyncVersionsResource,
    VersionsResourceWithRawResponse,
    AsyncVersionsResourceWithRawResponse,
    VersionsResourceWithStreamingResponse,
    AsyncVersionsResourceWithStreamingResponse,
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
from .suggested_session_timeout import (
    SuggestedSessionTimeoutResource,
    AsyncSuggestedSessionTimeoutResource,
    SuggestedSessionTimeoutResourceWithRawResponse,
    AsyncSuggestedSessionTimeoutResourceWithRawResponse,
    SuggestedSessionTimeoutResourceWithStreamingResponse,
    AsyncSuggestedSessionTimeoutResourceWithStreamingResponse,
)

__all__ = ["APIResource", "AsyncAPIResource"]


class APIResource(SyncAPIResource):
    @cached_property
    def glossary(self) -> GlossaryResource:
        return GlossaryResource(self._client)

    @cached_property
    def versions(self) -> VersionsResource:
        return VersionsResource(self._client)

    @cached_property
    def suggested_session_timeout(self) -> SuggestedSessionTimeoutResource:
        return SuggestedSessionTimeoutResource(self._client)

    @cached_property
    def with_raw_response(self) -> APIResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return APIResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> APIResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return APIResourceWithStreamingResponse(self)

    def root(
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
        <p>Returns information about:</p><ul><li>API version</li><li>Hosted by information</li><li>Hosted at information</li><li>Energy source information</li><li>Git Commit</li></ul><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/root",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAPIResource(AsyncAPIResource):
    @cached_property
    def glossary(self) -> AsyncGlossaryResource:
        return AsyncGlossaryResource(self._client)

    @cached_property
    def versions(self) -> AsyncVersionsResource:
        return AsyncVersionsResource(self._client)

    @cached_property
    def suggested_session_timeout(self) -> AsyncSuggestedSessionTimeoutResource:
        return AsyncSuggestedSessionTimeoutResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAPIResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAPIResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAPIResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAPIResourceWithStreamingResponse(self)

    async def root(
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
        <p>Returns information about:</p><ul><li>API version</li><li>Hosted by information</li><li>Hosted at information</li><li>Energy source information</li><li>Git Commit</li></ul><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/root",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class APIResourceWithRawResponse:
    def __init__(self, api: APIResource) -> None:
        self._api = api

        self.root = to_custom_raw_response_wrapper(
            api.root,
            BinaryAPIResponse,
        )

    @cached_property
    def glossary(self) -> GlossaryResourceWithRawResponse:
        return GlossaryResourceWithRawResponse(self._api.glossary)

    @cached_property
    def versions(self) -> VersionsResourceWithRawResponse:
        return VersionsResourceWithRawResponse(self._api.versions)

    @cached_property
    def suggested_session_timeout(self) -> SuggestedSessionTimeoutResourceWithRawResponse:
        return SuggestedSessionTimeoutResourceWithRawResponse(self._api.suggested_session_timeout)


class AsyncAPIResourceWithRawResponse:
    def __init__(self, api: AsyncAPIResource) -> None:
        self._api = api

        self.root = async_to_custom_raw_response_wrapper(
            api.root,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def glossary(self) -> AsyncGlossaryResourceWithRawResponse:
        return AsyncGlossaryResourceWithRawResponse(self._api.glossary)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self._api.versions)

    @cached_property
    def suggested_session_timeout(self) -> AsyncSuggestedSessionTimeoutResourceWithRawResponse:
        return AsyncSuggestedSessionTimeoutResourceWithRawResponse(self._api.suggested_session_timeout)


class APIResourceWithStreamingResponse:
    def __init__(self, api: APIResource) -> None:
        self._api = api

        self.root = to_custom_streamed_response_wrapper(
            api.root,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def glossary(self) -> GlossaryResourceWithStreamingResponse:
        return GlossaryResourceWithStreamingResponse(self._api.glossary)

    @cached_property
    def versions(self) -> VersionsResourceWithStreamingResponse:
        return VersionsResourceWithStreamingResponse(self._api.versions)

    @cached_property
    def suggested_session_timeout(self) -> SuggestedSessionTimeoutResourceWithStreamingResponse:
        return SuggestedSessionTimeoutResourceWithStreamingResponse(self._api.suggested_session_timeout)


class AsyncAPIResourceWithStreamingResponse:
    def __init__(self, api: AsyncAPIResource) -> None:
        self._api = api

        self.root = async_to_custom_streamed_response_wrapper(
            api.root,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def glossary(self) -> AsyncGlossaryResourceWithStreamingResponse:
        return AsyncGlossaryResourceWithStreamingResponse(self._api.glossary)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithStreamingResponse:
        return AsyncVersionsResourceWithStreamingResponse(self._api.versions)

    @cached_property
    def suggested_session_timeout(self) -> AsyncSuggestedSessionTimeoutResourceWithStreamingResponse:
        return AsyncSuggestedSessionTimeoutResourceWithStreamingResponse(self._api.suggested_session_timeout)
