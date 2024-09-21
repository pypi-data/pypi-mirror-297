# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...._base_client import make_request_options

__all__ = ["CurrentResource", "AsyncCurrentResource"]


class CurrentResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CurrentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CurrentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CurrentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CurrentResourceWithStreamingResponse(self)

    def retrieve(
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
        <p>Provide client's certificate info of a current call specified by PSD2-CERT value at Request Header</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/my/mtls/certificate/current",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncCurrentResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCurrentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCurrentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCurrentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCurrentResourceWithStreamingResponse(self)

    async def retrieve(
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
        <p>Provide client's certificate info of a current call specified by PSD2-CERT value at Request Header</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/my/mtls/certificate/current",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class CurrentResourceWithRawResponse:
    def __init__(self, current: CurrentResource) -> None:
        self._current = current

        self.retrieve = to_custom_raw_response_wrapper(
            current.retrieve,
            BinaryAPIResponse,
        )


class AsyncCurrentResourceWithRawResponse:
    def __init__(self, current: AsyncCurrentResource) -> None:
        self._current = current

        self.retrieve = async_to_custom_raw_response_wrapper(
            current.retrieve,
            AsyncBinaryAPIResponse,
        )


class CurrentResourceWithStreamingResponse:
    def __init__(self, current: CurrentResource) -> None:
        self._current = current

        self.retrieve = to_custom_streamed_response_wrapper(
            current.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncCurrentResourceWithStreamingResponse:
    def __init__(self, current: AsyncCurrentResource) -> None:
        self._current = current

        self.retrieve = async_to_custom_streamed_response_wrapper(
            current.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
