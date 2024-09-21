# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import authentication_type_validation_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
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

__all__ = ["AuthenticationTypeValidationsResource", "AsyncAuthenticationTypeValidationsResource"]


class AuthenticationTypeValidationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AuthenticationTypeValidationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AuthenticationTypeValidationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AuthenticationTypeValidationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AuthenticationTypeValidationsResourceWithStreamingResponse(self)

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
        <p>Create an Authentication Type Validation.</p><p>Please supply allowed authentication types.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID",
            body=maybe_transform(
                body, authentication_type_validation_create_params.AuthenticationTypeValidationCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
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
        <p>Delete an Authentication Type Validation by operation_id.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            "/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAuthenticationTypeValidationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAuthenticationTypeValidationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAuthenticationTypeValidationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAuthenticationTypeValidationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAuthenticationTypeValidationsResourceWithStreamingResponse(self)

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
        <p>Create an Authentication Type Validation.</p><p>Please supply allowed authentication types.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID",
            body=await async_maybe_transform(
                body, authentication_type_validation_create_params.AuthenticationTypeValidationCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
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
        <p>Delete an Authentication Type Validation by operation_id.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            "/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class AuthenticationTypeValidationsResourceWithRawResponse:
    def __init__(self, authentication_type_validations: AuthenticationTypeValidationsResource) -> None:
        self._authentication_type_validations = authentication_type_validations

        self.create = to_custom_raw_response_wrapper(
            authentication_type_validations.create,
            BinaryAPIResponse,
        )
        self.delete = to_custom_raw_response_wrapper(
            authentication_type_validations.delete,
            BinaryAPIResponse,
        )


class AsyncAuthenticationTypeValidationsResourceWithRawResponse:
    def __init__(self, authentication_type_validations: AsyncAuthenticationTypeValidationsResource) -> None:
        self._authentication_type_validations = authentication_type_validations

        self.create = async_to_custom_raw_response_wrapper(
            authentication_type_validations.create,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_custom_raw_response_wrapper(
            authentication_type_validations.delete,
            AsyncBinaryAPIResponse,
        )


class AuthenticationTypeValidationsResourceWithStreamingResponse:
    def __init__(self, authentication_type_validations: AuthenticationTypeValidationsResource) -> None:
        self._authentication_type_validations = authentication_type_validations

        self.create = to_custom_streamed_response_wrapper(
            authentication_type_validations.create,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_custom_streamed_response_wrapper(
            authentication_type_validations.delete,
            StreamedBinaryAPIResponse,
        )


class AsyncAuthenticationTypeValidationsResourceWithStreamingResponse:
    def __init__(self, authentication_type_validations: AsyncAuthenticationTypeValidationsResource) -> None:
        self._authentication_type_validations = authentication_type_validations

        self.create = async_to_custom_streamed_response_wrapper(
            authentication_type_validations.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_custom_streamed_response_wrapper(
            authentication_type_validations.delete,
            AsyncStreamedBinaryAPIResponse,
        )
