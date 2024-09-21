# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
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
from ...types.customers import kyc_document_update_params

__all__ = ["KYCDocumentsResource", "AsyncKYCDocumentsResource"]


class KYCDocumentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> KYCDocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return KYCDocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> KYCDocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return KYCDocumentsResourceWithStreamingResponse(self)

    def update(
        self,
        kyc_document_id: str,
        *,
        bank_id: str,
        customer_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """<p>Add a KYC document for the customer specified by CUSTOMER_ID.

        KYC Documents contain the document type (e.g. passport), place of issue, expiry etc.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        if not kyc_document_id:
            raise ValueError(f"Expected a non-empty value for `kyc_document_id` but received {kyc_document_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}/kyc_documents/{kyc_document_id}",
            body=maybe_transform(body, kyc_document_update_params.KYCDocumentUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
        self,
        customer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get KYC (know your customer) documents for a customer specified by CUSTOMER_ID<br />Get a list of documents that affirm the identity of the customer<br />Passport, driving licence etc.<br />Authentication is Optional</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/customers/{customer_id}/kyc_documents",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncKYCDocumentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncKYCDocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncKYCDocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncKYCDocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncKYCDocumentsResourceWithStreamingResponse(self)

    async def update(
        self,
        kyc_document_id: str,
        *,
        bank_id: str,
        customer_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """<p>Add a KYC document for the customer specified by CUSTOMER_ID.

        KYC Documents contain the document type (e.g. passport), place of issue, expiry etc.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        if not kyc_document_id:
            raise ValueError(f"Expected a non-empty value for `kyc_document_id` but received {kyc_document_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}/kyc_documents/{kyc_document_id}",
            body=await async_maybe_transform(body, kyc_document_update_params.KYCDocumentUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
        self,
        customer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get KYC (know your customer) documents for a customer specified by CUSTOMER_ID<br />Get a list of documents that affirm the identity of the customer<br />Passport, driving licence etc.<br />Authentication is Optional</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/customers/{customer_id}/kyc_documents",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class KYCDocumentsResourceWithRawResponse:
    def __init__(self, kyc_documents: KYCDocumentsResource) -> None:
        self._kyc_documents = kyc_documents

        self.update = to_custom_raw_response_wrapper(
            kyc_documents.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            kyc_documents.list,
            BinaryAPIResponse,
        )


class AsyncKYCDocumentsResourceWithRawResponse:
    def __init__(self, kyc_documents: AsyncKYCDocumentsResource) -> None:
        self._kyc_documents = kyc_documents

        self.update = async_to_custom_raw_response_wrapper(
            kyc_documents.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            kyc_documents.list,
            AsyncBinaryAPIResponse,
        )


class KYCDocumentsResourceWithStreamingResponse:
    def __init__(self, kyc_documents: KYCDocumentsResource) -> None:
        self._kyc_documents = kyc_documents

        self.update = to_custom_streamed_response_wrapper(
            kyc_documents.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            kyc_documents.list,
            StreamedBinaryAPIResponse,
        )


class AsyncKYCDocumentsResourceWithStreamingResponse:
    def __init__(self, kyc_documents: AsyncKYCDocumentsResource) -> None:
        self._kyc_documents = kyc_documents

        self.update = async_to_custom_streamed_response_wrapper(
            kyc_documents.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            kyc_documents.list,
            AsyncStreamedBinaryAPIResponse,
        )
