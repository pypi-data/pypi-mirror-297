# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .metadata import (
    MetadataResource,
    AsyncMetadataResource,
    MetadataResourceWithRawResponse,
    AsyncMetadataResourceWithRawResponse,
    MetadataResourceWithStreamingResponse,
    AsyncMetadataResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .private_alias import (
    PrivateAliasResource,
    AsyncPrivateAliasResource,
    PrivateAliasResourceWithRawResponse,
    AsyncPrivateAliasResourceWithRawResponse,
    PrivateAliasResourceWithStreamingResponse,
    AsyncPrivateAliasResourceWithStreamingResponse,
)
from .metadata.metadata import MetadataResource, AsyncMetadataResource

__all__ = ["CounterpartiesResource", "AsyncCounterpartiesResource"]


class CounterpartiesResource(SyncAPIResource):
    @cached_property
    def metadata(self) -> MetadataResource:
        return MetadataResource(self._client)

    @cached_property
    def private_alias(self) -> PrivateAliasResource:
        return PrivateAliasResource(self._client)

    @cached_property
    def with_raw_response(self) -> CounterpartiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CounterpartiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CounterpartiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CounterpartiesResourceWithStreamingResponse(self)


class AsyncCounterpartiesResource(AsyncAPIResource):
    @cached_property
    def metadata(self) -> AsyncMetadataResource:
        return AsyncMetadataResource(self._client)

    @cached_property
    def private_alias(self) -> AsyncPrivateAliasResource:
        return AsyncPrivateAliasResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCounterpartiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCounterpartiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCounterpartiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCounterpartiesResourceWithStreamingResponse(self)


class CounterpartiesResourceWithRawResponse:
    def __init__(self, counterparties: CounterpartiesResource) -> None:
        self._counterparties = counterparties

    @cached_property
    def metadata(self) -> MetadataResourceWithRawResponse:
        return MetadataResourceWithRawResponse(self._counterparties.metadata)

    @cached_property
    def private_alias(self) -> PrivateAliasResourceWithRawResponse:
        return PrivateAliasResourceWithRawResponse(self._counterparties.private_alias)


class AsyncCounterpartiesResourceWithRawResponse:
    def __init__(self, counterparties: AsyncCounterpartiesResource) -> None:
        self._counterparties = counterparties

    @cached_property
    def metadata(self) -> AsyncMetadataResourceWithRawResponse:
        return AsyncMetadataResourceWithRawResponse(self._counterparties.metadata)

    @cached_property
    def private_alias(self) -> AsyncPrivateAliasResourceWithRawResponse:
        return AsyncPrivateAliasResourceWithRawResponse(self._counterparties.private_alias)


class CounterpartiesResourceWithStreamingResponse:
    def __init__(self, counterparties: CounterpartiesResource) -> None:
        self._counterparties = counterparties

    @cached_property
    def metadata(self) -> MetadataResourceWithStreamingResponse:
        return MetadataResourceWithStreamingResponse(self._counterparties.metadata)

    @cached_property
    def private_alias(self) -> PrivateAliasResourceWithStreamingResponse:
        return PrivateAliasResourceWithStreamingResponse(self._counterparties.private_alias)


class AsyncCounterpartiesResourceWithStreamingResponse:
    def __init__(self, counterparties: AsyncCounterpartiesResource) -> None:
        self._counterparties = counterparties

    @cached_property
    def metadata(self) -> AsyncMetadataResourceWithStreamingResponse:
        return AsyncMetadataResourceWithStreamingResponse(self._counterparties.metadata)

    @cached_property
    def private_alias(self) -> AsyncPrivateAliasResourceWithStreamingResponse:
        return AsyncPrivateAliasResourceWithStreamingResponse(self._counterparties.private_alias)
