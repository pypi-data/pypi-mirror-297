# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["ConsentsResource", "AsyncConsentsResource"]


class ConsentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConsentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ConsentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConsentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ConsentsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        consent_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>This endpoint gets the Consent By consent id.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not consent_id:
            raise ValueError(f"Expected a non-empty value for `consent_id` but received {consent_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/user/current/consents/{consent_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncConsentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConsentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConsentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConsentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncConsentsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        consent_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>This endpoint gets the Consent By consent id.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not consent_id:
            raise ValueError(f"Expected a non-empty value for `consent_id` but received {consent_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/user/current/consents/{consent_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ConsentsResourceWithRawResponse:
    def __init__(self, consents: ConsentsResource) -> None:
        self._consents = consents

        self.retrieve = to_custom_raw_response_wrapper(
            consents.retrieve,
            BinaryAPIResponse,
        )


class AsyncConsentsResourceWithRawResponse:
    def __init__(self, consents: AsyncConsentsResource) -> None:
        self._consents = consents

        self.retrieve = async_to_custom_raw_response_wrapper(
            consents.retrieve,
            AsyncBinaryAPIResponse,
        )


class ConsentsResourceWithStreamingResponse:
    def __init__(self, consents: ConsentsResource) -> None:
        self._consents = consents

        self.retrieve = to_custom_streamed_response_wrapper(
            consents.retrieve,
            StreamedBinaryAPIResponse,
        )


class AsyncConsentsResourceWithStreamingResponse:
    def __init__(self, consents: AsyncConsentsResource) -> None:
        self._consents = consents

        self.retrieve = async_to_custom_streamed_response_wrapper(
            consents.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
