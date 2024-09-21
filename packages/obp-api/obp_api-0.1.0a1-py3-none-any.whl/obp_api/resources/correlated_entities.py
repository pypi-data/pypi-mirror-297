# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["CorrelatedEntitiesResource", "AsyncCorrelatedEntitiesResource"]


class CorrelatedEntitiesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CorrelatedEntitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CorrelatedEntitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CorrelatedEntitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CorrelatedEntitiesResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Correlated Entities are users and customers linked to the currently authenticated user via User-Customer-Links</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/my/correlated-entities",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncCorrelatedEntitiesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCorrelatedEntitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCorrelatedEntitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCorrelatedEntitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCorrelatedEntitiesResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Correlated Entities are users and customers linked to the currently authenticated user via User-Customer-Links</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/my/correlated-entities",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class CorrelatedEntitiesResourceWithRawResponse:
    def __init__(self, correlated_entities: CorrelatedEntitiesResource) -> None:
        self._correlated_entities = correlated_entities

        self.list = to_custom_raw_response_wrapper(
            correlated_entities.list,
            BinaryAPIResponse,
        )


class AsyncCorrelatedEntitiesResourceWithRawResponse:
    def __init__(self, correlated_entities: AsyncCorrelatedEntitiesResource) -> None:
        self._correlated_entities = correlated_entities

        self.list = async_to_custom_raw_response_wrapper(
            correlated_entities.list,
            AsyncBinaryAPIResponse,
        )


class CorrelatedEntitiesResourceWithStreamingResponse:
    def __init__(self, correlated_entities: CorrelatedEntitiesResource) -> None:
        self._correlated_entities = correlated_entities

        self.list = to_custom_streamed_response_wrapper(
            correlated_entities.list,
            StreamedBinaryAPIResponse,
        )


class AsyncCorrelatedEntitiesResourceWithStreamingResponse:
    def __init__(self, correlated_entities: AsyncCorrelatedEntitiesResource) -> None:
        self._correlated_entities = correlated_entities

        self.list = async_to_custom_streamed_response_wrapper(
            correlated_entities.list,
            AsyncStreamedBinaryAPIResponse,
        )
