# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .sms import (
    SMSResource,
    AsyncSMSResource,
    SMSResourceWithRawResponse,
    AsyncSMSResourceWithRawResponse,
    SMSResourceWithStreamingResponse,
    AsyncSMSResourceWithStreamingResponse,
)
from .email import (
    EmailResource,
    AsyncEmailResource,
    EmailResourceWithRawResponse,
    AsyncEmailResourceWithRawResponse,
    EmailResourceWithStreamingResponse,
    AsyncEmailResourceWithStreamingResponse,
)
from .sms.sms import SMSResource, AsyncSMSResource
from .consents import (
    ConsentsResource,
    AsyncConsentsResource,
    ConsentsResourceWithRawResponse,
    AsyncConsentsResourceWithRawResponse,
    ConsentsResourceWithStreamingResponse,
    AsyncConsentsResourceWithStreamingResponse,
)
from .implicit import (
    ImplicitResource,
    AsyncImplicitResource,
    ImplicitResourceWithRawResponse,
    AsyncImplicitResourceWithRawResponse,
    ImplicitResourceWithStreamingResponse,
    AsyncImplicitResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from .email.email import EmailResource, AsyncEmailResource
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
from ....types.consumer import consent_request_create_params
from .implicit.implicit import ImplicitResource, AsyncImplicitResource

__all__ = ["ConsentRequestsResource", "AsyncConsentRequestsResource"]


class ConsentRequestsResource(SyncAPIResource):
    @cached_property
    def email(self) -> EmailResource:
        return EmailResource(self._client)

    @cached_property
    def implicit(self) -> ImplicitResource:
        return ImplicitResource(self._client)

    @cached_property
    def sms(self) -> SMSResource:
        return SMSResource(self._client)

    @cached_property
    def consents(self) -> ConsentsResource:
        return ConsentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ConsentRequestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ConsentRequestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConsentRequestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ConsentRequestsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Client Authentication (mandatory)</p><p>It is used when applications request an access token to access their own resources, not on behalf of a user.</p><p>The client needs to authenticate themselves for this request.<br />In case of public client we use client_id and private kew to obtain access token, otherwise we use client_id and client_secret.<br />The obtained access token is used in the HTTP Bearer auth header of our request.</p><p>Example:<br />Authorization: Bearer eXtneO-THbQtn3zvK_kQtXXfvOZyZFdBCItlPDbR2Bk.dOWqtXCtFX-tqGTVR0YrIjvAolPIVg7GZ-jz83y6nA0</p><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/consumer/consent-requests",
            body=maybe_transform(body, consent_request_create_params.ConsentRequestCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

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
        """<p>Authentication is Optional</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncConsentRequestsResource(AsyncAPIResource):
    @cached_property
    def email(self) -> AsyncEmailResource:
        return AsyncEmailResource(self._client)

    @cached_property
    def implicit(self) -> AsyncImplicitResource:
        return AsyncImplicitResource(self._client)

    @cached_property
    def sms(self) -> AsyncSMSResource:
        return AsyncSMSResource(self._client)

    @cached_property
    def consents(self) -> AsyncConsentsResource:
        return AsyncConsentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncConsentRequestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConsentRequestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConsentRequestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncConsentRequestsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Client Authentication (mandatory)</p><p>It is used when applications request an access token to access their own resources, not on behalf of a user.</p><p>The client needs to authenticate themselves for this request.<br />In case of public client we use client_id and private kew to obtain access token, otherwise we use client_id and client_secret.<br />The obtained access token is used in the HTTP Bearer auth header of our request.</p><p>Example:<br />Authorization: Bearer eXtneO-THbQtn3zvK_kQtXXfvOZyZFdBCItlPDbR2Bk.dOWqtXCtFX-tqGTVR0YrIjvAolPIVg7GZ-jz83y6nA0</p><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/consumer/consent-requests",
            body=await async_maybe_transform(body, consent_request_create_params.ConsentRequestCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

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
        """<p>Authentication is Optional</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ConsentRequestsResourceWithRawResponse:
    def __init__(self, consent_requests: ConsentRequestsResource) -> None:
        self._consent_requests = consent_requests

        self.create = to_custom_raw_response_wrapper(
            consent_requests.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            consent_requests.retrieve,
            BinaryAPIResponse,
        )

    @cached_property
    def email(self) -> EmailResourceWithRawResponse:
        return EmailResourceWithRawResponse(self._consent_requests.email)

    @cached_property
    def implicit(self) -> ImplicitResourceWithRawResponse:
        return ImplicitResourceWithRawResponse(self._consent_requests.implicit)

    @cached_property
    def sms(self) -> SMSResourceWithRawResponse:
        return SMSResourceWithRawResponse(self._consent_requests.sms)

    @cached_property
    def consents(self) -> ConsentsResourceWithRawResponse:
        return ConsentsResourceWithRawResponse(self._consent_requests.consents)


class AsyncConsentRequestsResourceWithRawResponse:
    def __init__(self, consent_requests: AsyncConsentRequestsResource) -> None:
        self._consent_requests = consent_requests

        self.create = async_to_custom_raw_response_wrapper(
            consent_requests.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            consent_requests.retrieve,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def email(self) -> AsyncEmailResourceWithRawResponse:
        return AsyncEmailResourceWithRawResponse(self._consent_requests.email)

    @cached_property
    def implicit(self) -> AsyncImplicitResourceWithRawResponse:
        return AsyncImplicitResourceWithRawResponse(self._consent_requests.implicit)

    @cached_property
    def sms(self) -> AsyncSMSResourceWithRawResponse:
        return AsyncSMSResourceWithRawResponse(self._consent_requests.sms)

    @cached_property
    def consents(self) -> AsyncConsentsResourceWithRawResponse:
        return AsyncConsentsResourceWithRawResponse(self._consent_requests.consents)


class ConsentRequestsResourceWithStreamingResponse:
    def __init__(self, consent_requests: ConsentRequestsResource) -> None:
        self._consent_requests = consent_requests

        self.create = to_custom_streamed_response_wrapper(
            consent_requests.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            consent_requests.retrieve,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def email(self) -> EmailResourceWithStreamingResponse:
        return EmailResourceWithStreamingResponse(self._consent_requests.email)

    @cached_property
    def implicit(self) -> ImplicitResourceWithStreamingResponse:
        return ImplicitResourceWithStreamingResponse(self._consent_requests.implicit)

    @cached_property
    def sms(self) -> SMSResourceWithStreamingResponse:
        return SMSResourceWithStreamingResponse(self._consent_requests.sms)

    @cached_property
    def consents(self) -> ConsentsResourceWithStreamingResponse:
        return ConsentsResourceWithStreamingResponse(self._consent_requests.consents)


class AsyncConsentRequestsResourceWithStreamingResponse:
    def __init__(self, consent_requests: AsyncConsentRequestsResource) -> None:
        self._consent_requests = consent_requests

        self.create = async_to_custom_streamed_response_wrapper(
            consent_requests.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            consent_requests.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def email(self) -> AsyncEmailResourceWithStreamingResponse:
        return AsyncEmailResourceWithStreamingResponse(self._consent_requests.email)

    @cached_property
    def implicit(self) -> AsyncImplicitResourceWithStreamingResponse:
        return AsyncImplicitResourceWithStreamingResponse(self._consent_requests.implicit)

    @cached_property
    def sms(self) -> AsyncSMSResourceWithStreamingResponse:
        return AsyncSMSResourceWithStreamingResponse(self._consent_requests.sms)

    @cached_property
    def consents(self) -> AsyncConsentsResourceWithStreamingResponse:
        return AsyncConsentsResourceWithStreamingResponse(self._consent_requests.consents)
