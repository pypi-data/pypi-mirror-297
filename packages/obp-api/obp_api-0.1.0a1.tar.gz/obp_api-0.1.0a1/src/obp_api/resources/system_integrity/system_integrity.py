# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .banks import (
    BanksResource,
    AsyncBanksResource,
    BanksResourceWithRawResponse,
    AsyncBanksResourceWithRawResponse,
    BanksResourceWithStreamingResponse,
    AsyncBanksResourceWithStreamingResponse,
)
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

__all__ = ["SystemIntegrityResource", "AsyncSystemIntegrityResource"]


class SystemIntegrityResource(SyncAPIResource):
    @cached_property
    def banks(self) -> BanksResource:
        return BanksResource(self._client)

    @cached_property
    def with_raw_response(self) -> SystemIntegrityResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return SystemIntegrityResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SystemIntegrityResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return SystemIntegrityResourceWithStreamingResponse(self)

    def account_access_unique_index_1_check(
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
        <p>Check unique index at account access table.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/system/integrity/account-access-unique-index-1-check",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def custom_view_names_check(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """<p>Check custom view names.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/system/integrity/custom-view-names-check",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def system_view_names_check(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """<p>Check system view names.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/system/integrity/system-view-names-check",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncSystemIntegrityResource(AsyncAPIResource):
    @cached_property
    def banks(self) -> AsyncBanksResource:
        return AsyncBanksResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSystemIntegrityResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSystemIntegrityResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSystemIntegrityResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncSystemIntegrityResourceWithStreamingResponse(self)

    async def account_access_unique_index_1_check(
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
        <p>Check unique index at account access table.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/system/integrity/account-access-unique-index-1-check",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def custom_view_names_check(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """<p>Check custom view names.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/system/integrity/custom-view-names-check",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def system_view_names_check(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """<p>Check system view names.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/system/integrity/system-view-names-check",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class SystemIntegrityResourceWithRawResponse:
    def __init__(self, system_integrity: SystemIntegrityResource) -> None:
        self._system_integrity = system_integrity

        self.account_access_unique_index_1_check = to_custom_raw_response_wrapper(
            system_integrity.account_access_unique_index_1_check,
            BinaryAPIResponse,
        )
        self.custom_view_names_check = to_custom_raw_response_wrapper(
            system_integrity.custom_view_names_check,
            BinaryAPIResponse,
        )
        self.system_view_names_check = to_custom_raw_response_wrapper(
            system_integrity.system_view_names_check,
            BinaryAPIResponse,
        )

    @cached_property
    def banks(self) -> BanksResourceWithRawResponse:
        return BanksResourceWithRawResponse(self._system_integrity.banks)


class AsyncSystemIntegrityResourceWithRawResponse:
    def __init__(self, system_integrity: AsyncSystemIntegrityResource) -> None:
        self._system_integrity = system_integrity

        self.account_access_unique_index_1_check = async_to_custom_raw_response_wrapper(
            system_integrity.account_access_unique_index_1_check,
            AsyncBinaryAPIResponse,
        )
        self.custom_view_names_check = async_to_custom_raw_response_wrapper(
            system_integrity.custom_view_names_check,
            AsyncBinaryAPIResponse,
        )
        self.system_view_names_check = async_to_custom_raw_response_wrapper(
            system_integrity.system_view_names_check,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def banks(self) -> AsyncBanksResourceWithRawResponse:
        return AsyncBanksResourceWithRawResponse(self._system_integrity.banks)


class SystemIntegrityResourceWithStreamingResponse:
    def __init__(self, system_integrity: SystemIntegrityResource) -> None:
        self._system_integrity = system_integrity

        self.account_access_unique_index_1_check = to_custom_streamed_response_wrapper(
            system_integrity.account_access_unique_index_1_check,
            StreamedBinaryAPIResponse,
        )
        self.custom_view_names_check = to_custom_streamed_response_wrapper(
            system_integrity.custom_view_names_check,
            StreamedBinaryAPIResponse,
        )
        self.system_view_names_check = to_custom_streamed_response_wrapper(
            system_integrity.system_view_names_check,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def banks(self) -> BanksResourceWithStreamingResponse:
        return BanksResourceWithStreamingResponse(self._system_integrity.banks)


class AsyncSystemIntegrityResourceWithStreamingResponse:
    def __init__(self, system_integrity: AsyncSystemIntegrityResource) -> None:
        self._system_integrity = system_integrity

        self.account_access_unique_index_1_check = async_to_custom_streamed_response_wrapper(
            system_integrity.account_access_unique_index_1_check,
            AsyncStreamedBinaryAPIResponse,
        )
        self.custom_view_names_check = async_to_custom_streamed_response_wrapper(
            system_integrity.custom_view_names_check,
            AsyncStreamedBinaryAPIResponse,
        )
        self.system_view_names_check = async_to_custom_streamed_response_wrapper(
            system_integrity.system_view_names_check,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def banks(self) -> AsyncBanksResourceWithStreamingResponse:
        return AsyncBanksResourceWithStreamingResponse(self._system_integrity.banks)
