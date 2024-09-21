# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .certificate import (
    CertificateResource,
    AsyncCertificateResource,
    CertificateResourceWithRawResponse,
    AsyncCertificateResourceWithRawResponse,
    CertificateResourceWithStreamingResponse,
    AsyncCertificateResourceWithStreamingResponse,
)
from .certificate.certificate import CertificateResource, AsyncCertificateResource

__all__ = ["MtlsResource", "AsyncMtlsResource"]


class MtlsResource(SyncAPIResource):
    @cached_property
    def certificate(self) -> CertificateResource:
        return CertificateResource(self._client)

    @cached_property
    def with_raw_response(self) -> MtlsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return MtlsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MtlsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return MtlsResourceWithStreamingResponse(self)


class AsyncMtlsResource(AsyncAPIResource):
    @cached_property
    def certificate(self) -> AsyncCertificateResource:
        return AsyncCertificateResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMtlsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMtlsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMtlsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncMtlsResourceWithStreamingResponse(self)


class MtlsResourceWithRawResponse:
    def __init__(self, mtls: MtlsResource) -> None:
        self._mtls = mtls

    @cached_property
    def certificate(self) -> CertificateResourceWithRawResponse:
        return CertificateResourceWithRawResponse(self._mtls.certificate)


class AsyncMtlsResourceWithRawResponse:
    def __init__(self, mtls: AsyncMtlsResource) -> None:
        self._mtls = mtls

    @cached_property
    def certificate(self) -> AsyncCertificateResourceWithRawResponse:
        return AsyncCertificateResourceWithRawResponse(self._mtls.certificate)


class MtlsResourceWithStreamingResponse:
    def __init__(self, mtls: MtlsResource) -> None:
        self._mtls = mtls

    @cached_property
    def certificate(self) -> CertificateResourceWithStreamingResponse:
        return CertificateResourceWithStreamingResponse(self._mtls.certificate)


class AsyncMtlsResourceWithStreamingResponse:
    def __init__(self, mtls: AsyncMtlsResource) -> None:
        self._mtls = mtls

    @cached_property
    def certificate(self) -> AsyncCertificateResourceWithStreamingResponse:
        return AsyncCertificateResourceWithStreamingResponse(self._mtls.certificate)
