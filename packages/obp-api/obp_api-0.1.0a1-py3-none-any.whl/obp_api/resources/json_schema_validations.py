# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import json_schema_validation_create_params, json_schema_validation_update_params
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
        <p>Create a JSON Schema Validation.</p><p>Introduction:</p>  <p>JSON Schema is &quot;a vocabulary that allows you to annotate and validate JSON documents&quot;.</p><p>By applying JSON Schema Validation to your OBP endpoints you can constrain POST and PUT request bodies. For example, you can set minimum / maximum lengths of fields and constrain values to certain lists or regular expressions.</p><p>See <a href="https://json-schema.org/">JSONSchema.org</a> for more information about the JSON Schema standard.</p><p>To create a JSON Schema from an any JSON Request body you can use <a href="https://jsonschema.net/app/schemas/0">JSON Schema Net</a></p><p>(The video link below shows how to use that)</p><p>Note: OBP Dynamic Entities also use JSON Schema Validation so you don't need to additionally wrap the resulting endpoints with extra JSON Schema Validation but you could do.</p><p>You can apply JSON schema validations to any OBP endpoint's request body using the POST and PUT endpoints listed in the link below.</p><p>PLEASE SEE the following video explanation: <a href="https://vimeo.com/485287014">JSON schema validation of request for Static and Dynamic Endpoints and Entities</a></p><p>To use this endpoint, please supply a valid json-schema in the request body.</p><p>Note: It might take a few minutes for the newly created JSON Schema to take effect!</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/management/json-schema-validations/OPERATION_ID",
            body=maybe_transform(body, json_schema_validation_create_params.JsonSchemaValidationCreateParams),
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
        """
        <p>Get a JSON Schema Validation by operation_id.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/json-schema-validations/OPERATION_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
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
        <p>Update a JSON Schema Validation.</p><p>Introduction:</p>  <p>JSON Schema is &quot;a vocabulary that allows you to annotate and validate JSON documents&quot;.</p><p>By applying JSON Schema Validation to your OBP endpoints you can constrain POST and PUT request bodies. For example, you can set minimum / maximum lengths of fields and constrain values to certain lists or regular expressions.</p><p>See <a href="https://json-schema.org/">JSONSchema.org</a> for more information about the JSON Schema standard.</p><p>To create a JSON Schema from an any JSON Request body you can use <a href="https://jsonschema.net/app/schemas/0">JSON Schema Net</a></p><p>(The video link below shows how to use that)</p><p>Note: OBP Dynamic Entities also use JSON Schema Validation so you don't need to additionally wrap the resulting endpoints with extra JSON Schema Validation but you could do.</p><p>You can apply JSON schema validations to any OBP endpoint's request body using the POST and PUT endpoints listed in the link below.</p><p>PLEASE SEE the following video explanation: <a href="https://vimeo.com/485287014">JSON schema validation of request for Static and Dynamic Endpoints and Entities</a></p><p>To use this endpoint, please supply a valid json-schema in the request body.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/obp/v5.1.0/management/json-schema-validations/OPERATION_ID",
            body=maybe_transform(body, json_schema_validation_update_params.JsonSchemaValidationUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

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
        """<p>Get all JSON Schema Validations.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/json-schema-validations",
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
        <p>Delete a JSON Schema Validation by operation_id.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            "/obp/v5.1.0/management/json-schema-validations/OPERATION_ID",
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
        <p>Create a JSON Schema Validation.</p><p>Introduction:</p>  <p>JSON Schema is &quot;a vocabulary that allows you to annotate and validate JSON documents&quot;.</p><p>By applying JSON Schema Validation to your OBP endpoints you can constrain POST and PUT request bodies. For example, you can set minimum / maximum lengths of fields and constrain values to certain lists or regular expressions.</p><p>See <a href="https://json-schema.org/">JSONSchema.org</a> for more information about the JSON Schema standard.</p><p>To create a JSON Schema from an any JSON Request body you can use <a href="https://jsonschema.net/app/schemas/0">JSON Schema Net</a></p><p>(The video link below shows how to use that)</p><p>Note: OBP Dynamic Entities also use JSON Schema Validation so you don't need to additionally wrap the resulting endpoints with extra JSON Schema Validation but you could do.</p><p>You can apply JSON schema validations to any OBP endpoint's request body using the POST and PUT endpoints listed in the link below.</p><p>PLEASE SEE the following video explanation: <a href="https://vimeo.com/485287014">JSON schema validation of request for Static and Dynamic Endpoints and Entities</a></p><p>To use this endpoint, please supply a valid json-schema in the request body.</p><p>Note: It might take a few minutes for the newly created JSON Schema to take effect!</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/management/json-schema-validations/OPERATION_ID",
            body=await async_maybe_transform(
                body, json_schema_validation_create_params.JsonSchemaValidationCreateParams
            ),
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
        """
        <p>Get a JSON Schema Validation by operation_id.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/json-schema-validations/OPERATION_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
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
        <p>Update a JSON Schema Validation.</p><p>Introduction:</p>  <p>JSON Schema is &quot;a vocabulary that allows you to annotate and validate JSON documents&quot;.</p><p>By applying JSON Schema Validation to your OBP endpoints you can constrain POST and PUT request bodies. For example, you can set minimum / maximum lengths of fields and constrain values to certain lists or regular expressions.</p><p>See <a href="https://json-schema.org/">JSONSchema.org</a> for more information about the JSON Schema standard.</p><p>To create a JSON Schema from an any JSON Request body you can use <a href="https://jsonschema.net/app/schemas/0">JSON Schema Net</a></p><p>(The video link below shows how to use that)</p><p>Note: OBP Dynamic Entities also use JSON Schema Validation so you don't need to additionally wrap the resulting endpoints with extra JSON Schema Validation but you could do.</p><p>You can apply JSON schema validations to any OBP endpoint's request body using the POST and PUT endpoints listed in the link below.</p><p>PLEASE SEE the following video explanation: <a href="https://vimeo.com/485287014">JSON schema validation of request for Static and Dynamic Endpoints and Entities</a></p><p>To use this endpoint, please supply a valid json-schema in the request body.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/obp/v5.1.0/management/json-schema-validations/OPERATION_ID",
            body=await async_maybe_transform(
                body, json_schema_validation_update_params.JsonSchemaValidationUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

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
        """<p>Get all JSON Schema Validations.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/json-schema-validations",
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
        <p>Delete a JSON Schema Validation by operation_id.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            "/obp/v5.1.0/management/json-schema-validations/OPERATION_ID",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class JsonSchemaValidationsResourceWithRawResponse:
    def __init__(self, json_schema_validations: JsonSchemaValidationsResource) -> None:
        self._json_schema_validations = json_schema_validations

        self.create = to_custom_raw_response_wrapper(
            json_schema_validations.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            json_schema_validations.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            json_schema_validations.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            json_schema_validations.list,
            BinaryAPIResponse,
        )
        self.delete = to_custom_raw_response_wrapper(
            json_schema_validations.delete,
            BinaryAPIResponse,
        )


class AsyncJsonSchemaValidationsResourceWithRawResponse:
    def __init__(self, json_schema_validations: AsyncJsonSchemaValidationsResource) -> None:
        self._json_schema_validations = json_schema_validations

        self.create = async_to_custom_raw_response_wrapper(
            json_schema_validations.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            json_schema_validations.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            json_schema_validations.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            json_schema_validations.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_custom_raw_response_wrapper(
            json_schema_validations.delete,
            AsyncBinaryAPIResponse,
        )


class JsonSchemaValidationsResourceWithStreamingResponse:
    def __init__(self, json_schema_validations: JsonSchemaValidationsResource) -> None:
        self._json_schema_validations = json_schema_validations

        self.create = to_custom_streamed_response_wrapper(
            json_schema_validations.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            json_schema_validations.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            json_schema_validations.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            json_schema_validations.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_custom_streamed_response_wrapper(
            json_schema_validations.delete,
            StreamedBinaryAPIResponse,
        )


class AsyncJsonSchemaValidationsResourceWithStreamingResponse:
    def __init__(self, json_schema_validations: AsyncJsonSchemaValidationsResource) -> None:
        self._json_schema_validations = json_schema_validations

        self.create = async_to_custom_streamed_response_wrapper(
            json_schema_validations.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            json_schema_validations.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            json_schema_validations.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            json_schema_validations.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_custom_streamed_response_wrapper(
            json_schema_validations.delete,
            AsyncStreamedBinaryAPIResponse,
        )
