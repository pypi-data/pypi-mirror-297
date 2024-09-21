# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ....._compat import cached_property
from .transactions import (
    TransactionsResource,
    AsyncTransactionsResource,
    TransactionsResourceWithRawResponse,
    AsyncTransactionsResourceWithRawResponse,
    TransactionsResourceWithStreamingResponse,
    AsyncTransactionsResourceWithStreamingResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["HistoricalResource", "AsyncHistoricalResource"]


class HistoricalResource(SyncAPIResource):
    @cached_property
    def transactions(self) -> TransactionsResource:
        return TransactionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> HistoricalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return HistoricalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> HistoricalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return HistoricalResourceWithStreamingResponse(self)


class AsyncHistoricalResource(AsyncAPIResource):
    @cached_property
    def transactions(self) -> AsyncTransactionsResource:
        return AsyncTransactionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncHistoricalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncHistoricalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHistoricalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncHistoricalResourceWithStreamingResponse(self)


class HistoricalResourceWithRawResponse:
    def __init__(self, historical: HistoricalResource) -> None:
        self._historical = historical

    @cached_property
    def transactions(self) -> TransactionsResourceWithRawResponse:
        return TransactionsResourceWithRawResponse(self._historical.transactions)


class AsyncHistoricalResourceWithRawResponse:
    def __init__(self, historical: AsyncHistoricalResource) -> None:
        self._historical = historical

    @cached_property
    def transactions(self) -> AsyncTransactionsResourceWithRawResponse:
        return AsyncTransactionsResourceWithRawResponse(self._historical.transactions)


class HistoricalResourceWithStreamingResponse:
    def __init__(self, historical: HistoricalResource) -> None:
        self._historical = historical

    @cached_property
    def transactions(self) -> TransactionsResourceWithStreamingResponse:
        return TransactionsResourceWithStreamingResponse(self._historical.transactions)


class AsyncHistoricalResourceWithStreamingResponse:
    def __init__(self, historical: AsyncHistoricalResource) -> None:
        self._historical = historical

    @cached_property
    def transactions(self) -> AsyncTransactionsResourceWithStreamingResponse:
        return AsyncTransactionsResourceWithStreamingResponse(self._historical.transactions)
