# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
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
from ....types.banks.atms import supported_language_update_params

__all__ = ["SupportedLanguagesResource", "AsyncSupportedLanguagesResource"]


class SupportedLanguagesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SupportedLanguagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return SupportedLanguagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SupportedLanguagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return SupportedLanguagesResourceWithStreamingResponse(self)

    def update(
        self,
        atm_id: str,
        *,
        bank_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Update ATM Supported Languages.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/supported-languages",
            body=maybe_transform(body, supported_language_update_params.SupportedLanguageUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncSupportedLanguagesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSupportedLanguagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSupportedLanguagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSupportedLanguagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncSupportedLanguagesResourceWithStreamingResponse(self)

    async def update(
        self,
        atm_id: str,
        *,
        bank_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Update ATM Supported Languages.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/supported-languages",
            body=await async_maybe_transform(body, supported_language_update_params.SupportedLanguageUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class SupportedLanguagesResourceWithRawResponse:
    def __init__(self, supported_languages: SupportedLanguagesResource) -> None:
        self._supported_languages = supported_languages

        self.update = to_custom_raw_response_wrapper(
            supported_languages.update,
            BinaryAPIResponse,
        )


class AsyncSupportedLanguagesResourceWithRawResponse:
    def __init__(self, supported_languages: AsyncSupportedLanguagesResource) -> None:
        self._supported_languages = supported_languages

        self.update = async_to_custom_raw_response_wrapper(
            supported_languages.update,
            AsyncBinaryAPIResponse,
        )


class SupportedLanguagesResourceWithStreamingResponse:
    def __init__(self, supported_languages: SupportedLanguagesResource) -> None:
        self._supported_languages = supported_languages

        self.update = to_custom_streamed_response_wrapper(
            supported_languages.update,
            StreamedBinaryAPIResponse,
        )


class AsyncSupportedLanguagesResourceWithStreamingResponse:
    def __init__(self, supported_languages: AsyncSupportedLanguagesResource) -> None:
        self._supported_languages = supported_languages

        self.update = async_to_custom_streamed_response_wrapper(
            supported_languages.update,
            AsyncStreamedBinaryAPIResponse,
        )
