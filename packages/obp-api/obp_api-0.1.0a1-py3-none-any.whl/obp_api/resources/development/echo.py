# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["EchoResource", "AsyncEchoResource"]


class EchoResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EchoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return EchoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EchoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return EchoResourceWithStreamingResponse(self)

    def jws_verified_request_jws_signed_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Verify Request and Sign Response of a current call.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/development/echo/jws-verified-request-jws-signed-response",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncEchoResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEchoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEchoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEchoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncEchoResourceWithStreamingResponse(self)

    async def jws_verified_request_jws_signed_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Verify Request and Sign Response of a current call.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/development/echo/jws-verified-request-jws-signed-response",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class EchoResourceWithRawResponse:
    def __init__(self, echo: EchoResource) -> None:
        self._echo = echo

        self.jws_verified_request_jws_signed_response = to_raw_response_wrapper(
            echo.jws_verified_request_jws_signed_response,
        )


class AsyncEchoResourceWithRawResponse:
    def __init__(self, echo: AsyncEchoResource) -> None:
        self._echo = echo

        self.jws_verified_request_jws_signed_response = async_to_raw_response_wrapper(
            echo.jws_verified_request_jws_signed_response,
        )


class EchoResourceWithStreamingResponse:
    def __init__(self, echo: EchoResource) -> None:
        self._echo = echo

        self.jws_verified_request_jws_signed_response = to_streamed_response_wrapper(
            echo.jws_verified_request_jws_signed_response,
        )


class AsyncEchoResourceWithStreamingResponse:
    def __init__(self, echo: AsyncEchoResource) -> None:
        self._echo = echo

        self.jws_verified_request_jws_signed_response = async_to_streamed_response_wrapper(
            echo.jws_verified_request_jws_signed_response,
        )
