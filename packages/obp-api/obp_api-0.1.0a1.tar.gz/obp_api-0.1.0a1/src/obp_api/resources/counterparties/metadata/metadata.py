# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .url import (
    URLResource,
    AsyncURLResource,
    URLResourceWithRawResponse,
    AsyncURLResourceWithRawResponse,
    URLResourceWithStreamingResponse,
    AsyncURLResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .physical_location import (
    PhysicalLocationResource,
    AsyncPhysicalLocationResource,
    PhysicalLocationResourceWithRawResponse,
    AsyncPhysicalLocationResourceWithRawResponse,
    PhysicalLocationResourceWithStreamingResponse,
    AsyncPhysicalLocationResourceWithStreamingResponse,
)
from .open_corporates_url import (
    OpenCorporatesURLResource,
    AsyncOpenCorporatesURLResource,
    OpenCorporatesURLResourceWithRawResponse,
    AsyncOpenCorporatesURLResourceWithRawResponse,
    OpenCorporatesURLResourceWithStreamingResponse,
    AsyncOpenCorporatesURLResourceWithStreamingResponse,
)

__all__ = ["MetadataResource", "AsyncMetadataResource"]


class MetadataResource(SyncAPIResource):
    @cached_property
    def open_corporates_url(self) -> OpenCorporatesURLResource:
        return OpenCorporatesURLResource(self._client)

    @cached_property
    def physical_location(self) -> PhysicalLocationResource:
        return PhysicalLocationResource(self._client)

    @cached_property
    def url(self) -> URLResource:
        return URLResource(self._client)

    @cached_property
    def with_raw_response(self) -> MetadataResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return MetadataResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MetadataResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return MetadataResourceWithStreamingResponse(self)


class AsyncMetadataResource(AsyncAPIResource):
    @cached_property
    def open_corporates_url(self) -> AsyncOpenCorporatesURLResource:
        return AsyncOpenCorporatesURLResource(self._client)

    @cached_property
    def physical_location(self) -> AsyncPhysicalLocationResource:
        return AsyncPhysicalLocationResource(self._client)

    @cached_property
    def url(self) -> AsyncURLResource:
        return AsyncURLResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMetadataResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMetadataResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMetadataResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncMetadataResourceWithStreamingResponse(self)


class MetadataResourceWithRawResponse:
    def __init__(self, metadata: MetadataResource) -> None:
        self._metadata = metadata

    @cached_property
    def open_corporates_url(self) -> OpenCorporatesURLResourceWithRawResponse:
        return OpenCorporatesURLResourceWithRawResponse(self._metadata.open_corporates_url)

    @cached_property
    def physical_location(self) -> PhysicalLocationResourceWithRawResponse:
        return PhysicalLocationResourceWithRawResponse(self._metadata.physical_location)

    @cached_property
    def url(self) -> URLResourceWithRawResponse:
        return URLResourceWithRawResponse(self._metadata.url)


class AsyncMetadataResourceWithRawResponse:
    def __init__(self, metadata: AsyncMetadataResource) -> None:
        self._metadata = metadata

    @cached_property
    def open_corporates_url(self) -> AsyncOpenCorporatesURLResourceWithRawResponse:
        return AsyncOpenCorporatesURLResourceWithRawResponse(self._metadata.open_corporates_url)

    @cached_property
    def physical_location(self) -> AsyncPhysicalLocationResourceWithRawResponse:
        return AsyncPhysicalLocationResourceWithRawResponse(self._metadata.physical_location)

    @cached_property
    def url(self) -> AsyncURLResourceWithRawResponse:
        return AsyncURLResourceWithRawResponse(self._metadata.url)


class MetadataResourceWithStreamingResponse:
    def __init__(self, metadata: MetadataResource) -> None:
        self._metadata = metadata

    @cached_property
    def open_corporates_url(self) -> OpenCorporatesURLResourceWithStreamingResponse:
        return OpenCorporatesURLResourceWithStreamingResponse(self._metadata.open_corporates_url)

    @cached_property
    def physical_location(self) -> PhysicalLocationResourceWithStreamingResponse:
        return PhysicalLocationResourceWithStreamingResponse(self._metadata.physical_location)

    @cached_property
    def url(self) -> URLResourceWithStreamingResponse:
        return URLResourceWithStreamingResponse(self._metadata.url)


class AsyncMetadataResourceWithStreamingResponse:
    def __init__(self, metadata: AsyncMetadataResource) -> None:
        self._metadata = metadata

    @cached_property
    def open_corporates_url(self) -> AsyncOpenCorporatesURLResourceWithStreamingResponse:
        return AsyncOpenCorporatesURLResourceWithStreamingResponse(self._metadata.open_corporates_url)

    @cached_property
    def physical_location(self) -> AsyncPhysicalLocationResourceWithStreamingResponse:
        return AsyncPhysicalLocationResourceWithStreamingResponse(self._metadata.physical_location)

    @cached_property
    def url(self) -> AsyncURLResourceWithStreamingResponse:
        return AsyncURLResourceWithStreamingResponse(self._metadata.url)
