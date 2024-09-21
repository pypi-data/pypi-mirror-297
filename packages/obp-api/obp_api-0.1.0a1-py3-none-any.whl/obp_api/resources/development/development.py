# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .echo import (
    EchoResource,
    AsyncEchoResource,
    EchoResourceWithRawResponse,
    AsyncEchoResourceWithRawResponse,
    EchoResourceWithStreamingResponse,
    AsyncEchoResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .call_context import (
    CallContextResource,
    AsyncCallContextResource,
    CallContextResourceWithRawResponse,
    AsyncCallContextResourceWithRawResponse,
    CallContextResourceWithStreamingResponse,
    AsyncCallContextResourceWithStreamingResponse,
)

__all__ = ["DevelopmentResource", "AsyncDevelopmentResource"]


class DevelopmentResource(SyncAPIResource):
    @cached_property
    def call_context(self) -> CallContextResource:
        return CallContextResource(self._client)

    @cached_property
    def echo(self) -> EchoResource:
        return EchoResource(self._client)

    @cached_property
    def with_raw_response(self) -> DevelopmentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return DevelopmentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DevelopmentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return DevelopmentResourceWithStreamingResponse(self)


class AsyncDevelopmentResource(AsyncAPIResource):
    @cached_property
    def call_context(self) -> AsyncCallContextResource:
        return AsyncCallContextResource(self._client)

    @cached_property
    def echo(self) -> AsyncEchoResource:
        return AsyncEchoResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDevelopmentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDevelopmentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDevelopmentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncDevelopmentResourceWithStreamingResponse(self)


class DevelopmentResourceWithRawResponse:
    def __init__(self, development: DevelopmentResource) -> None:
        self._development = development

    @cached_property
    def call_context(self) -> CallContextResourceWithRawResponse:
        return CallContextResourceWithRawResponse(self._development.call_context)

    @cached_property
    def echo(self) -> EchoResourceWithRawResponse:
        return EchoResourceWithRawResponse(self._development.echo)


class AsyncDevelopmentResourceWithRawResponse:
    def __init__(self, development: AsyncDevelopmentResource) -> None:
        self._development = development

    @cached_property
    def call_context(self) -> AsyncCallContextResourceWithRawResponse:
        return AsyncCallContextResourceWithRawResponse(self._development.call_context)

    @cached_property
    def echo(self) -> AsyncEchoResourceWithRawResponse:
        return AsyncEchoResourceWithRawResponse(self._development.echo)


class DevelopmentResourceWithStreamingResponse:
    def __init__(self, development: DevelopmentResource) -> None:
        self._development = development

    @cached_property
    def call_context(self) -> CallContextResourceWithStreamingResponse:
        return CallContextResourceWithStreamingResponse(self._development.call_context)

    @cached_property
    def echo(self) -> EchoResourceWithStreamingResponse:
        return EchoResourceWithStreamingResponse(self._development.echo)


class AsyncDevelopmentResourceWithStreamingResponse:
    def __init__(self, development: AsyncDevelopmentResource) -> None:
        self._development = development

    @cached_property
    def call_context(self) -> AsyncCallContextResourceWithStreamingResponse:
        return AsyncCallContextResourceWithStreamingResponse(self._development.call_context)

    @cached_property
    def echo(self) -> AsyncEchoResourceWithStreamingResponse:
        return AsyncEchoResourceWithStreamingResponse(self._development.echo)
