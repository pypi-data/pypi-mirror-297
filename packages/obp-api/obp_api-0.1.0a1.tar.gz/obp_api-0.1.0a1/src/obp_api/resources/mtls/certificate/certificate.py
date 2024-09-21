# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .current import (
    CurrentResource,
    AsyncCurrentResource,
    CurrentResourceWithRawResponse,
    AsyncCurrentResourceWithRawResponse,
    CurrentResourceWithStreamingResponse,
    AsyncCurrentResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["CertificateResource", "AsyncCertificateResource"]


class CertificateResource(SyncAPIResource):
    @cached_property
    def current(self) -> CurrentResource:
        return CurrentResource(self._client)

    @cached_property
    def with_raw_response(self) -> CertificateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CertificateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CertificateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CertificateResourceWithStreamingResponse(self)


class AsyncCertificateResource(AsyncAPIResource):
    @cached_property
    def current(self) -> AsyncCurrentResource:
        return AsyncCurrentResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCertificateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCertificateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCertificateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCertificateResourceWithStreamingResponse(self)


class CertificateResourceWithRawResponse:
    def __init__(self, certificate: CertificateResource) -> None:
        self._certificate = certificate

    @cached_property
    def current(self) -> CurrentResourceWithRawResponse:
        return CurrentResourceWithRawResponse(self._certificate.current)


class AsyncCertificateResourceWithRawResponse:
    def __init__(self, certificate: AsyncCertificateResource) -> None:
        self._certificate = certificate

    @cached_property
    def current(self) -> AsyncCurrentResourceWithRawResponse:
        return AsyncCurrentResourceWithRawResponse(self._certificate.current)


class CertificateResourceWithStreamingResponse:
    def __init__(self, certificate: CertificateResource) -> None:
        self._certificate = certificate

    @cached_property
    def current(self) -> CurrentResourceWithStreamingResponse:
        return CurrentResourceWithStreamingResponse(self._certificate.current)


class AsyncCertificateResourceWithStreamingResponse:
    def __init__(self, certificate: AsyncCertificateResource) -> None:
        self._certificate = certificate

    @cached_property
    def current(self) -> AsyncCurrentResourceWithStreamingResponse:
        return AsyncCurrentResourceWithStreamingResponse(self._certificate.current)
