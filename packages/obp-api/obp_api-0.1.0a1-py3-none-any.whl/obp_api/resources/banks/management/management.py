# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ...._compat import cached_property
from .historical import (
    HistoricalResource,
    AsyncHistoricalResource,
    HistoricalResourceWithRawResponse,
    AsyncHistoricalResourceWithRawResponse,
    HistoricalResourceWithStreamingResponse,
    AsyncHistoricalResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from .historical.historical import HistoricalResource, AsyncHistoricalResource

__all__ = ["ManagementResource", "AsyncManagementResource"]


class ManagementResource(SyncAPIResource):
    @cached_property
    def historical(self) -> HistoricalResource:
        return HistoricalResource(self._client)

    @cached_property
    def with_raw_response(self) -> ManagementResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ManagementResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ManagementResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ManagementResourceWithStreamingResponse(self)


class AsyncManagementResource(AsyncAPIResource):
    @cached_property
    def historical(self) -> AsyncHistoricalResource:
        return AsyncHistoricalResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncManagementResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncManagementResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncManagementResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncManagementResourceWithStreamingResponse(self)


class ManagementResourceWithRawResponse:
    def __init__(self, management: ManagementResource) -> None:
        self._management = management

    @cached_property
    def historical(self) -> HistoricalResourceWithRawResponse:
        return HistoricalResourceWithRawResponse(self._management.historical)


class AsyncManagementResourceWithRawResponse:
    def __init__(self, management: AsyncManagementResource) -> None:
        self._management = management

    @cached_property
    def historical(self) -> AsyncHistoricalResourceWithRawResponse:
        return AsyncHistoricalResourceWithRawResponse(self._management.historical)


class ManagementResourceWithStreamingResponse:
    def __init__(self, management: ManagementResource) -> None:
        self._management = management

    @cached_property
    def historical(self) -> HistoricalResourceWithStreamingResponse:
        return HistoricalResourceWithStreamingResponse(self._management.historical)


class AsyncManagementResourceWithStreamingResponse:
    def __init__(self, management: AsyncManagementResource) -> None:
        self._management = management

    @cached_property
    def historical(self) -> AsyncHistoricalResourceWithStreamingResponse:
        return AsyncHistoricalResourceWithStreamingResponse(self._management.historical)
