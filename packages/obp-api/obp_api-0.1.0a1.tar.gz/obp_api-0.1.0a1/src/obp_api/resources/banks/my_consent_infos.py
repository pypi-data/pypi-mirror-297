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

__all__ = ["MyConsentInfosResource", "AsyncMyConsentInfosResource"]


class MyConsentInfosResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MyConsentInfosResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return MyConsentInfosResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MyConsentInfosResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return MyConsentInfosResourceWithStreamingResponse(self)

    def list(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>This endpoint gets the Consents that the current User created.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/my/consent-infos",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncMyConsentInfosResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMyConsentInfosResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMyConsentInfosResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMyConsentInfosResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncMyConsentInfosResourceWithStreamingResponse(self)

    async def list(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>This endpoint gets the Consents that the current User created.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/my/consent-infos",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class MyConsentInfosResourceWithRawResponse:
    def __init__(self, my_consent_infos: MyConsentInfosResource) -> None:
        self._my_consent_infos = my_consent_infos

        self.list = to_custom_raw_response_wrapper(
            my_consent_infos.list,
            BinaryAPIResponse,
        )


class AsyncMyConsentInfosResourceWithRawResponse:
    def __init__(self, my_consent_infos: AsyncMyConsentInfosResource) -> None:
        self._my_consent_infos = my_consent_infos

        self.list = async_to_custom_raw_response_wrapper(
            my_consent_infos.list,
            AsyncBinaryAPIResponse,
        )


class MyConsentInfosResourceWithStreamingResponse:
    def __init__(self, my_consent_infos: MyConsentInfosResource) -> None:
        self._my_consent_infos = my_consent_infos

        self.list = to_custom_streamed_response_wrapper(
            my_consent_infos.list,
            StreamedBinaryAPIResponse,
        )


class AsyncMyConsentInfosResourceWithStreamingResponse:
    def __init__(self, my_consent_infos: AsyncMyConsentInfosResource) -> None:
        self._my_consent_infos = my_consent_infos

        self.list = async_to_custom_streamed_response_wrapper(
            my_consent_infos.list,
            AsyncStreamedBinaryAPIResponse,
        )
