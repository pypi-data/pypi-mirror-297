# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .views import (
    ViewsResource,
    AsyncViewsResource,
    ViewsResourceWithRawResponse,
    AsyncViewsResourceWithRawResponse,
    ViewsResourceWithStreamingResponse,
    AsyncViewsResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .transactions import (
    TransactionsResource,
    AsyncTransactionsResource,
    TransactionsResourceWithRawResponse,
    AsyncTransactionsResourceWithRawResponse,
    TransactionsResourceWithStreamingResponse,
    AsyncTransactionsResourceWithStreamingResponse,
)

__all__ = ["FirehoseResource", "AsyncFirehoseResource"]


class FirehoseResource(SyncAPIResource):
    @cached_property
    def transactions(self) -> TransactionsResource:
        return TransactionsResource(self._client)

    @cached_property
    def views(self) -> ViewsResource:
        return ViewsResource(self._client)

    @cached_property
    def with_raw_response(self) -> FirehoseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return FirehoseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FirehoseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return FirehoseResourceWithStreamingResponse(self)


class AsyncFirehoseResource(AsyncAPIResource):
    @cached_property
    def transactions(self) -> AsyncTransactionsResource:
        return AsyncTransactionsResource(self._client)

    @cached_property
    def views(self) -> AsyncViewsResource:
        return AsyncViewsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFirehoseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFirehoseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFirehoseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncFirehoseResourceWithStreamingResponse(self)


class FirehoseResourceWithRawResponse:
    def __init__(self, firehose: FirehoseResource) -> None:
        self._firehose = firehose

    @cached_property
    def transactions(self) -> TransactionsResourceWithRawResponse:
        return TransactionsResourceWithRawResponse(self._firehose.transactions)

    @cached_property
    def views(self) -> ViewsResourceWithRawResponse:
        return ViewsResourceWithRawResponse(self._firehose.views)


class AsyncFirehoseResourceWithRawResponse:
    def __init__(self, firehose: AsyncFirehoseResource) -> None:
        self._firehose = firehose

    @cached_property
    def transactions(self) -> AsyncTransactionsResourceWithRawResponse:
        return AsyncTransactionsResourceWithRawResponse(self._firehose.transactions)

    @cached_property
    def views(self) -> AsyncViewsResourceWithRawResponse:
        return AsyncViewsResourceWithRawResponse(self._firehose.views)


class FirehoseResourceWithStreamingResponse:
    def __init__(self, firehose: FirehoseResource) -> None:
        self._firehose = firehose

    @cached_property
    def transactions(self) -> TransactionsResourceWithStreamingResponse:
        return TransactionsResourceWithStreamingResponse(self._firehose.transactions)

    @cached_property
    def views(self) -> ViewsResourceWithStreamingResponse:
        return ViewsResourceWithStreamingResponse(self._firehose.views)


class AsyncFirehoseResourceWithStreamingResponse:
    def __init__(self, firehose: AsyncFirehoseResource) -> None:
        self._firehose = firehose

    @cached_property
    def transactions(self) -> AsyncTransactionsResourceWithStreamingResponse:
        return AsyncTransactionsResourceWithStreamingResponse(self._firehose.transactions)

    @cached_property
    def views(self) -> AsyncViewsResourceWithStreamingResponse:
        return AsyncViewsResourceWithStreamingResponse(self._firehose.views)
