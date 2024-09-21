# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .consents import (
    ConsentsResource,
    AsyncConsentsResource,
    ConsentsResourceWithRawResponse,
    AsyncConsentsResourceWithRawResponse,
    ConsentsResourceWithStreamingResponse,
    AsyncConsentsResourceWithStreamingResponse,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["ImplicitResource", "AsyncImplicitResource"]


class ImplicitResource(SyncAPIResource):
    @cached_property
    def consents(self) -> ConsentsResource:
        return ConsentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ImplicitResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ImplicitResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ImplicitResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ImplicitResourceWithStreamingResponse(self)


class AsyncImplicitResource(AsyncAPIResource):
    @cached_property
    def consents(self) -> AsyncConsentsResource:
        return AsyncConsentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncImplicitResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncImplicitResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncImplicitResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncImplicitResourceWithStreamingResponse(self)


class ImplicitResourceWithRawResponse:
    def __init__(self, implicit: ImplicitResource) -> None:
        self._implicit = implicit

    @cached_property
    def consents(self) -> ConsentsResourceWithRawResponse:
        return ConsentsResourceWithRawResponse(self._implicit.consents)


class AsyncImplicitResourceWithRawResponse:
    def __init__(self, implicit: AsyncImplicitResource) -> None:
        self._implicit = implicit

    @cached_property
    def consents(self) -> AsyncConsentsResourceWithRawResponse:
        return AsyncConsentsResourceWithRawResponse(self._implicit.consents)


class ImplicitResourceWithStreamingResponse:
    def __init__(self, implicit: ImplicitResource) -> None:
        self._implicit = implicit

    @cached_property
    def consents(self) -> ConsentsResourceWithStreamingResponse:
        return ConsentsResourceWithStreamingResponse(self._implicit.consents)


class AsyncImplicitResourceWithStreamingResponse:
    def __init__(self, implicit: AsyncImplicitResource) -> None:
        self._implicit = implicit

    @cached_property
    def consents(self) -> AsyncConsentsResourceWithStreamingResponse:
        return AsyncConsentsResourceWithStreamingResponse(self._implicit.consents)
