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

__all__ = ["ConsentResource", "AsyncConsentResource"]


class ConsentResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConsentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ConsentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConsentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ConsentResourceWithStreamingResponse(self)

    def revoke(
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
        <p>Revoke Consent specified by Consent-Id at Request Header</p><p>There are a few reasons you might need to revoke an application’s access to a user’s account:<br />- The user explicitly wishes to revoke the application’s access<br />- You as the service provider have determined an application is compromised or malicious, and want to disable it<br />- etc.</p><p>OBP as a resource server stores access tokens in a database, then it is relatively easy to revoke some token that belongs to a particular user.<br />The status of the token is changed to &quot;REVOKED&quot; so the next time the revoked client makes a request, their token will fail to validate.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            "/obp/v5.1.0/my/consent/current",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncConsentResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConsentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConsentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConsentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncConsentResourceWithStreamingResponse(self)

    async def revoke(
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
        <p>Revoke Consent specified by Consent-Id at Request Header</p><p>There are a few reasons you might need to revoke an application’s access to a user’s account:<br />- The user explicitly wishes to revoke the application’s access<br />- You as the service provider have determined an application is compromised or malicious, and want to disable it<br />- etc.</p><p>OBP as a resource server stores access tokens in a database, then it is relatively easy to revoke some token that belongs to a particular user.<br />The status of the token is changed to &quot;REVOKED&quot; so the next time the revoked client makes a request, their token will fail to validate.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            "/obp/v5.1.0/my/consent/current",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ConsentResourceWithRawResponse:
    def __init__(self, consent: ConsentResource) -> None:
        self._consent = consent

        self.revoke = to_custom_raw_response_wrapper(
            consent.revoke,
            BinaryAPIResponse,
        )


class AsyncConsentResourceWithRawResponse:
    def __init__(self, consent: AsyncConsentResource) -> None:
        self._consent = consent

        self.revoke = async_to_custom_raw_response_wrapper(
            consent.revoke,
            AsyncBinaryAPIResponse,
        )


class ConsentResourceWithStreamingResponse:
    def __init__(self, consent: ConsentResource) -> None:
        self._consent = consent

        self.revoke = to_custom_streamed_response_wrapper(
            consent.revoke,
            StreamedBinaryAPIResponse,
        )


class AsyncConsentResourceWithStreamingResponse:
    def __init__(self, consent: AsyncConsentResource) -> None:
        self._consent = consent

        self.revoke = async_to_custom_streamed_response_wrapper(
            consent.revoke,
            AsyncStreamedBinaryAPIResponse,
        )
