# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .message_docs import (
    MessageDocsResource,
    AsyncMessageDocsResource,
    MessageDocsResourceWithRawResponse,
    AsyncMessageDocsResourceWithRawResponse,
    MessageDocsResourceWithStreamingResponse,
    AsyncMessageDocsResourceWithStreamingResponse,
)
from .message_docs.message_docs import MessageDocsResource, AsyncMessageDocsResource

__all__ = ["DocumentationResource", "AsyncDocumentationResource"]


class DocumentationResource(SyncAPIResource):
    @cached_property
    def message_docs(self) -> MessageDocsResource:
        return MessageDocsResource(self._client)

    @cached_property
    def with_raw_response(self) -> DocumentationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return DocumentationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocumentationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return DocumentationResourceWithStreamingResponse(self)


class AsyncDocumentationResource(AsyncAPIResource):
    @cached_property
    def message_docs(self) -> AsyncMessageDocsResource:
        return AsyncMessageDocsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDocumentationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDocumentationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocumentationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncDocumentationResourceWithStreamingResponse(self)


class DocumentationResourceWithRawResponse:
    def __init__(self, documentation: DocumentationResource) -> None:
        self._documentation = documentation

    @cached_property
    def message_docs(self) -> MessageDocsResourceWithRawResponse:
        return MessageDocsResourceWithRawResponse(self._documentation.message_docs)


class AsyncDocumentationResourceWithRawResponse:
    def __init__(self, documentation: AsyncDocumentationResource) -> None:
        self._documentation = documentation

    @cached_property
    def message_docs(self) -> AsyncMessageDocsResourceWithRawResponse:
        return AsyncMessageDocsResourceWithRawResponse(self._documentation.message_docs)


class DocumentationResourceWithStreamingResponse:
    def __init__(self, documentation: DocumentationResource) -> None:
        self._documentation = documentation

    @cached_property
    def message_docs(self) -> MessageDocsResourceWithStreamingResponse:
        return MessageDocsResourceWithStreamingResponse(self._documentation.message_docs)


class AsyncDocumentationResourceWithStreamingResponse:
    def __init__(self, documentation: AsyncDocumentationResource) -> None:
        self._documentation = documentation

    @cached_property
    def message_docs(self) -> AsyncMessageDocsResourceWithStreamingResponse:
        return AsyncMessageDocsResourceWithStreamingResponse(self._documentation.message_docs)
