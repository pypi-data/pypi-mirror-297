# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .consents import (
    ConsentsResource,
    AsyncConsentsResource,
    ConsentsResourceWithRawResponse,
    AsyncConsentsResourceWithRawResponse,
    ConsentsResourceWithStreamingResponse,
    AsyncConsentsResourceWithStreamingResponse,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["SMSResource", "AsyncSMSResource"]


class SMSResource(SyncAPIResource):
    @cached_property
    def consents(self) -> ConsentsResource:
        return ConsentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> SMSResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return SMSResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SMSResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return SMSResourceWithStreamingResponse(self)


class AsyncSMSResource(AsyncAPIResource):
    @cached_property
    def consents(self) -> AsyncConsentsResource:
        return AsyncConsentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSMSResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSMSResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSMSResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncSMSResourceWithStreamingResponse(self)


class SMSResourceWithRawResponse:
    def __init__(self, sms: SMSResource) -> None:
        self._sms = sms

    @cached_property
    def consents(self) -> ConsentsResourceWithRawResponse:
        return ConsentsResourceWithRawResponse(self._sms.consents)


class AsyncSMSResourceWithRawResponse:
    def __init__(self, sms: AsyncSMSResource) -> None:
        self._sms = sms

    @cached_property
    def consents(self) -> AsyncConsentsResourceWithRawResponse:
        return AsyncConsentsResourceWithRawResponse(self._sms.consents)


class SMSResourceWithStreamingResponse:
    def __init__(self, sms: SMSResource) -> None:
        self._sms = sms

    @cached_property
    def consents(self) -> ConsentsResourceWithStreamingResponse:
        return ConsentsResourceWithStreamingResponse(self._sms.consents)


class AsyncSMSResourceWithStreamingResponse:
    def __init__(self, sms: AsyncSMSResource) -> None:
        self._sms = sms

    @cached_property
    def consents(self) -> AsyncConsentsResourceWithStreamingResponse:
        return AsyncConsentsResourceWithStreamingResponse(self._sms.consents)
