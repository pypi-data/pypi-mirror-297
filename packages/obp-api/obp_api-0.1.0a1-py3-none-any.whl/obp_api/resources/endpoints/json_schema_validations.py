# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

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

__all__ = ["JsonSchemaValidationsResource", "AsyncJsonSchemaValidationsResource"]


class JsonSchemaValidationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> JsonSchemaValidationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return JsonSchemaValidationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> JsonSchemaValidationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return JsonSchemaValidationsResourceWithStreamingResponse(self)

    def list(
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
        <p>Get all JSON Schema Validations - public.</p><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/endpoints/json-schema-validations",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncJsonSchemaValidationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncJsonSchemaValidationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncJsonSchemaValidationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncJsonSchemaValidationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncJsonSchemaValidationsResourceWithStreamingResponse(self)

    async def list(
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
        <p>Get all JSON Schema Validations - public.</p><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/endpoints/json-schema-validations",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class JsonSchemaValidationsResourceWithRawResponse:
    def __init__(self, json_schema_validations: JsonSchemaValidationsResource) -> None:
        self._json_schema_validations = json_schema_validations

        self.list = to_custom_raw_response_wrapper(
            json_schema_validations.list,
            BinaryAPIResponse,
        )


class AsyncJsonSchemaValidationsResourceWithRawResponse:
    def __init__(self, json_schema_validations: AsyncJsonSchemaValidationsResource) -> None:
        self._json_schema_validations = json_schema_validations

        self.list = async_to_custom_raw_response_wrapper(
            json_schema_validations.list,
            AsyncBinaryAPIResponse,
        )


class JsonSchemaValidationsResourceWithStreamingResponse:
    def __init__(self, json_schema_validations: JsonSchemaValidationsResource) -> None:
        self._json_schema_validations = json_schema_validations

        self.list = to_custom_streamed_response_wrapper(
            json_schema_validations.list,
            StreamedBinaryAPIResponse,
        )


class AsyncJsonSchemaValidationsResourceWithStreamingResponse:
    def __init__(self, json_schema_validations: AsyncJsonSchemaValidationsResource) -> None:
        self._json_schema_validations = json_schema_validations

        self.list = async_to_custom_streamed_response_wrapper(
            json_schema_validations.list,
            AsyncStreamedBinaryAPIResponse,
        )
