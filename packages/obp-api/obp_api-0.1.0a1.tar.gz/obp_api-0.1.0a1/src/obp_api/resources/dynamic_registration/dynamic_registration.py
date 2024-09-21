# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from .consumers import (
    ConsumersResource,
    AsyncConsumersResource,
    ConsumersResourceWithRawResponse,
    AsyncConsumersResourceWithRawResponse,
    ConsumersResourceWithStreamingResponse,
    AsyncConsumersResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["DynamicRegistrationResource", "AsyncDynamicRegistrationResource"]


class DynamicRegistrationResource(SyncAPIResource):
    @cached_property
    def consumers(self) -> ConsumersResource:
        return ConsumersResource(self._client)

    @cached_property
    def with_raw_response(self) -> DynamicRegistrationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return DynamicRegistrationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DynamicRegistrationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return DynamicRegistrationResourceWithStreamingResponse(self)


class AsyncDynamicRegistrationResource(AsyncAPIResource):
    @cached_property
    def consumers(self) -> AsyncConsumersResource:
        return AsyncConsumersResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDynamicRegistrationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDynamicRegistrationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDynamicRegistrationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncDynamicRegistrationResourceWithStreamingResponse(self)


class DynamicRegistrationResourceWithRawResponse:
    def __init__(self, dynamic_registration: DynamicRegistrationResource) -> None:
        self._dynamic_registration = dynamic_registration

    @cached_property
    def consumers(self) -> ConsumersResourceWithRawResponse:
        return ConsumersResourceWithRawResponse(self._dynamic_registration.consumers)


class AsyncDynamicRegistrationResourceWithRawResponse:
    def __init__(self, dynamic_registration: AsyncDynamicRegistrationResource) -> None:
        self._dynamic_registration = dynamic_registration

    @cached_property
    def consumers(self) -> AsyncConsumersResourceWithRawResponse:
        return AsyncConsumersResourceWithRawResponse(self._dynamic_registration.consumers)


class DynamicRegistrationResourceWithStreamingResponse:
    def __init__(self, dynamic_registration: DynamicRegistrationResource) -> None:
        self._dynamic_registration = dynamic_registration

    @cached_property
    def consumers(self) -> ConsumersResourceWithStreamingResponse:
        return ConsumersResourceWithStreamingResponse(self._dynamic_registration.consumers)


class AsyncDynamicRegistrationResourceWithStreamingResponse:
    def __init__(self, dynamic_registration: AsyncDynamicRegistrationResource) -> None:
        self._dynamic_registration = dynamic_registration

    @cached_property
    def consumers(self) -> AsyncConsumersResourceWithStreamingResponse:
        return AsyncConsumersResourceWithStreamingResponse(self._dynamic_registration.consumers)
