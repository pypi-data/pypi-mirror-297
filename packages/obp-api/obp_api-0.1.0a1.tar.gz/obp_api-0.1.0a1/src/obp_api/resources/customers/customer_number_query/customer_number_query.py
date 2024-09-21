# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .overview import (
    OverviewResource,
    AsyncOverviewResource,
    OverviewResourceWithRawResponse,
    AsyncOverviewResourceWithRawResponse,
    OverviewResourceWithStreamingResponse,
    AsyncOverviewResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .overview_flat import (
    OverviewFlatResource,
    AsyncOverviewFlatResource,
    OverviewFlatResourceWithRawResponse,
    AsyncOverviewFlatResourceWithRawResponse,
    OverviewFlatResourceWithStreamingResponse,
    AsyncOverviewFlatResourceWithStreamingResponse,
)

__all__ = ["CustomerNumberQueryResource", "AsyncCustomerNumberQueryResource"]


class CustomerNumberQueryResource(SyncAPIResource):
    @cached_property
    def overview(self) -> OverviewResource:
        return OverviewResource(self._client)

    @cached_property
    def overview_flat(self) -> OverviewFlatResource:
        return OverviewFlatResource(self._client)

    @cached_property
    def with_raw_response(self) -> CustomerNumberQueryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CustomerNumberQueryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CustomerNumberQueryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CustomerNumberQueryResourceWithStreamingResponse(self)


class AsyncCustomerNumberQueryResource(AsyncAPIResource):
    @cached_property
    def overview(self) -> AsyncOverviewResource:
        return AsyncOverviewResource(self._client)

    @cached_property
    def overview_flat(self) -> AsyncOverviewFlatResource:
        return AsyncOverviewFlatResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCustomerNumberQueryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCustomerNumberQueryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCustomerNumberQueryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCustomerNumberQueryResourceWithStreamingResponse(self)


class CustomerNumberQueryResourceWithRawResponse:
    def __init__(self, customer_number_query: CustomerNumberQueryResource) -> None:
        self._customer_number_query = customer_number_query

    @cached_property
    def overview(self) -> OverviewResourceWithRawResponse:
        return OverviewResourceWithRawResponse(self._customer_number_query.overview)

    @cached_property
    def overview_flat(self) -> OverviewFlatResourceWithRawResponse:
        return OverviewFlatResourceWithRawResponse(self._customer_number_query.overview_flat)


class AsyncCustomerNumberQueryResourceWithRawResponse:
    def __init__(self, customer_number_query: AsyncCustomerNumberQueryResource) -> None:
        self._customer_number_query = customer_number_query

    @cached_property
    def overview(self) -> AsyncOverviewResourceWithRawResponse:
        return AsyncOverviewResourceWithRawResponse(self._customer_number_query.overview)

    @cached_property
    def overview_flat(self) -> AsyncOverviewFlatResourceWithRawResponse:
        return AsyncOverviewFlatResourceWithRawResponse(self._customer_number_query.overview_flat)


class CustomerNumberQueryResourceWithStreamingResponse:
    def __init__(self, customer_number_query: CustomerNumberQueryResource) -> None:
        self._customer_number_query = customer_number_query

    @cached_property
    def overview(self) -> OverviewResourceWithStreamingResponse:
        return OverviewResourceWithStreamingResponse(self._customer_number_query.overview)

    @cached_property
    def overview_flat(self) -> OverviewFlatResourceWithStreamingResponse:
        return OverviewFlatResourceWithStreamingResponse(self._customer_number_query.overview_flat)


class AsyncCustomerNumberQueryResourceWithStreamingResponse:
    def __init__(self, customer_number_query: AsyncCustomerNumberQueryResource) -> None:
        self._customer_number_query = customer_number_query

    @cached_property
    def overview(self) -> AsyncOverviewResourceWithStreamingResponse:
        return AsyncOverviewResourceWithStreamingResponse(self._customer_number_query.overview)

    @cached_property
    def overview_flat(self) -> AsyncOverviewFlatResourceWithStreamingResponse:
        return AsyncOverviewFlatResourceWithStreamingResponse(self._customer_number_query.overview_flat)
