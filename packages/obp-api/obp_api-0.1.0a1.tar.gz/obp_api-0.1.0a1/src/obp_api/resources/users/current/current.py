# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .consumers import (
    ConsumersResource,
    AsyncConsumersResource,
    ConsumersResourceWithRawResponse,
    AsyncConsumersResourceWithRawResponse,
    ConsumersResourceWithStreamingResponse,
    AsyncConsumersResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["CurrentResource", "AsyncCurrentResource"]


class CurrentResource(SyncAPIResource):
    @cached_property
    def consumers(self) -> ConsumersResource:
        return ConsumersResource(self._client)

    @cached_property
    def with_raw_response(self) -> CurrentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CurrentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CurrentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CurrentResourceWithStreamingResponse(self)


class AsyncCurrentResource(AsyncAPIResource):
    @cached_property
    def consumers(self) -> AsyncConsumersResource:
        return AsyncConsumersResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCurrentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCurrentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCurrentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCurrentResourceWithStreamingResponse(self)


class CurrentResourceWithRawResponse:
    def __init__(self, current: CurrentResource) -> None:
        self._current = current

    @cached_property
    def consumers(self) -> ConsumersResourceWithRawResponse:
        return ConsumersResourceWithRawResponse(self._current.consumers)


class AsyncCurrentResourceWithRawResponse:
    def __init__(self, current: AsyncCurrentResource) -> None:
        self._current = current

    @cached_property
    def consumers(self) -> AsyncConsumersResourceWithRawResponse:
        return AsyncConsumersResourceWithRawResponse(self._current.consumers)


class CurrentResourceWithStreamingResponse:
    def __init__(self, current: CurrentResource) -> None:
        self._current = current

    @cached_property
    def consumers(self) -> ConsumersResourceWithStreamingResponse:
        return ConsumersResourceWithStreamingResponse(self._current.consumers)


class AsyncCurrentResourceWithStreamingResponse:
    def __init__(self, current: AsyncCurrentResource) -> None:
        self._current = current

    @cached_property
    def consumers(self) -> AsyncConsumersResourceWithStreamingResponse:
        return AsyncConsumersResourceWithStreamingResponse(self._current.consumers)
