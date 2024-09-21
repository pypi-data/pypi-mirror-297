# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .accounts import (
    AccountsResource,
    AsyncAccountsResource,
    AccountsResourceWithRawResponse,
    AsyncAccountsResourceWithRawResponse,
    AccountsResourceWithStreamingResponse,
    AsyncAccountsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .api_collections import (
    APICollectionsResource,
    AsyncAPICollectionsResource,
    APICollectionsResourceWithRawResponse,
    AsyncAPICollectionsResourceWithRawResponse,
    APICollectionsResourceWithStreamingResponse,
    AsyncAPICollectionsResourceWithStreamingResponse,
)
from .aggregate_metrics import (
    AggregateMetricsResource,
    AsyncAggregateMetricsResource,
    AggregateMetricsResourceWithRawResponse,
    AsyncAggregateMetricsResourceWithRawResponse,
    AggregateMetricsResourceWithStreamingResponse,
    AsyncAggregateMetricsResourceWithStreamingResponse,
)
from .authentication_type_validations import (
    AuthenticationTypeValidationsResource,
    AsyncAuthenticationTypeValidationsResource,
    AuthenticationTypeValidationsResourceWithRawResponse,
    AsyncAuthenticationTypeValidationsResourceWithRawResponse,
    AuthenticationTypeValidationsResourceWithStreamingResponse,
    AsyncAuthenticationTypeValidationsResourceWithStreamingResponse,
)

__all__ = ["ManagementResource", "AsyncManagementResource"]


class ManagementResource(SyncAPIResource):
    @cached_property
    def accounts(self) -> AccountsResource:
        return AccountsResource(self._client)

    @cached_property
    def aggregate_metrics(self) -> AggregateMetricsResource:
        return AggregateMetricsResource(self._client)

    @cached_property
    def api_collections(self) -> APICollectionsResource:
        return APICollectionsResource(self._client)

    @cached_property
    def authentication_type_validations(self) -> AuthenticationTypeValidationsResource:
        return AuthenticationTypeValidationsResource(self._client)

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
    def accounts(self) -> AsyncAccountsResource:
        return AsyncAccountsResource(self._client)

    @cached_property
    def aggregate_metrics(self) -> AsyncAggregateMetricsResource:
        return AsyncAggregateMetricsResource(self._client)

    @cached_property
    def api_collections(self) -> AsyncAPICollectionsResource:
        return AsyncAPICollectionsResource(self._client)

    @cached_property
    def authentication_type_validations(self) -> AsyncAuthenticationTypeValidationsResource:
        return AsyncAuthenticationTypeValidationsResource(self._client)

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
    def accounts(self) -> AccountsResourceWithRawResponse:
        return AccountsResourceWithRawResponse(self._management.accounts)

    @cached_property
    def aggregate_metrics(self) -> AggregateMetricsResourceWithRawResponse:
        return AggregateMetricsResourceWithRawResponse(self._management.aggregate_metrics)

    @cached_property
    def api_collections(self) -> APICollectionsResourceWithRawResponse:
        return APICollectionsResourceWithRawResponse(self._management.api_collections)

    @cached_property
    def authentication_type_validations(self) -> AuthenticationTypeValidationsResourceWithRawResponse:
        return AuthenticationTypeValidationsResourceWithRawResponse(self._management.authentication_type_validations)


class AsyncManagementResourceWithRawResponse:
    def __init__(self, management: AsyncManagementResource) -> None:
        self._management = management

    @cached_property
    def accounts(self) -> AsyncAccountsResourceWithRawResponse:
        return AsyncAccountsResourceWithRawResponse(self._management.accounts)

    @cached_property
    def aggregate_metrics(self) -> AsyncAggregateMetricsResourceWithRawResponse:
        return AsyncAggregateMetricsResourceWithRawResponse(self._management.aggregate_metrics)

    @cached_property
    def api_collections(self) -> AsyncAPICollectionsResourceWithRawResponse:
        return AsyncAPICollectionsResourceWithRawResponse(self._management.api_collections)

    @cached_property
    def authentication_type_validations(self) -> AsyncAuthenticationTypeValidationsResourceWithRawResponse:
        return AsyncAuthenticationTypeValidationsResourceWithRawResponse(
            self._management.authentication_type_validations
        )


class ManagementResourceWithStreamingResponse:
    def __init__(self, management: ManagementResource) -> None:
        self._management = management

    @cached_property
    def accounts(self) -> AccountsResourceWithStreamingResponse:
        return AccountsResourceWithStreamingResponse(self._management.accounts)

    @cached_property
    def aggregate_metrics(self) -> AggregateMetricsResourceWithStreamingResponse:
        return AggregateMetricsResourceWithStreamingResponse(self._management.aggregate_metrics)

    @cached_property
    def api_collections(self) -> APICollectionsResourceWithStreamingResponse:
        return APICollectionsResourceWithStreamingResponse(self._management.api_collections)

    @cached_property
    def authentication_type_validations(self) -> AuthenticationTypeValidationsResourceWithStreamingResponse:
        return AuthenticationTypeValidationsResourceWithStreamingResponse(
            self._management.authentication_type_validations
        )


class AsyncManagementResourceWithStreamingResponse:
    def __init__(self, management: AsyncManagementResource) -> None:
        self._management = management

    @cached_property
    def accounts(self) -> AsyncAccountsResourceWithStreamingResponse:
        return AsyncAccountsResourceWithStreamingResponse(self._management.accounts)

    @cached_property
    def aggregate_metrics(self) -> AsyncAggregateMetricsResourceWithStreamingResponse:
        return AsyncAggregateMetricsResourceWithStreamingResponse(self._management.aggregate_metrics)

    @cached_property
    def api_collections(self) -> AsyncAPICollectionsResourceWithStreamingResponse:
        return AsyncAPICollectionsResourceWithStreamingResponse(self._management.api_collections)

    @cached_property
    def authentication_type_validations(self) -> AsyncAuthenticationTypeValidationsResourceWithStreamingResponse:
        return AsyncAuthenticationTypeValidationsResourceWithStreamingResponse(
            self._management.authentication_type_validations
        )
