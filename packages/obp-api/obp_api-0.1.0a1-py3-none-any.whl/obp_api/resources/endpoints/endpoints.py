# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .tags import (
    TagsResource,
    AsyncTagsResource,
    TagsResourceWithRawResponse,
    AsyncTagsResourceWithRawResponse,
    TagsResourceWithStreamingResponse,
    AsyncTagsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .json_schema_validations import (
    JsonSchemaValidationsResource,
    AsyncJsonSchemaValidationsResource,
    JsonSchemaValidationsResourceWithRawResponse,
    AsyncJsonSchemaValidationsResourceWithRawResponse,
    JsonSchemaValidationsResourceWithStreamingResponse,
    AsyncJsonSchemaValidationsResourceWithStreamingResponse,
)
from .authentication_type_validations import (
    AuthenticationTypeValidationsResource,
    AsyncAuthenticationTypeValidationsResource,
    AuthenticationTypeValidationsResourceWithRawResponse,
    AsyncAuthenticationTypeValidationsResourceWithRawResponse,
    AuthenticationTypeValidationsResourceWithStreamingResponse,
    AsyncAuthenticationTypeValidationsResourceWithStreamingResponse,
)

__all__ = ["EndpointsResource", "AsyncEndpointsResource"]


class EndpointsResource(SyncAPIResource):
    @cached_property
    def authentication_type_validations(self) -> AuthenticationTypeValidationsResource:
        return AuthenticationTypeValidationsResource(self._client)

    @cached_property
    def json_schema_validations(self) -> JsonSchemaValidationsResource:
        return JsonSchemaValidationsResource(self._client)

    @cached_property
    def tags(self) -> TagsResource:
        return TagsResource(self._client)

    @cached_property
    def with_raw_response(self) -> EndpointsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return EndpointsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EndpointsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return EndpointsResourceWithStreamingResponse(self)


class AsyncEndpointsResource(AsyncAPIResource):
    @cached_property
    def authentication_type_validations(self) -> AsyncAuthenticationTypeValidationsResource:
        return AsyncAuthenticationTypeValidationsResource(self._client)

    @cached_property
    def json_schema_validations(self) -> AsyncJsonSchemaValidationsResource:
        return AsyncJsonSchemaValidationsResource(self._client)

    @cached_property
    def tags(self) -> AsyncTagsResource:
        return AsyncTagsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEndpointsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEndpointsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEndpointsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncEndpointsResourceWithStreamingResponse(self)


class EndpointsResourceWithRawResponse:
    def __init__(self, endpoints: EndpointsResource) -> None:
        self._endpoints = endpoints

    @cached_property
    def authentication_type_validations(self) -> AuthenticationTypeValidationsResourceWithRawResponse:
        return AuthenticationTypeValidationsResourceWithRawResponse(self._endpoints.authentication_type_validations)

    @cached_property
    def json_schema_validations(self) -> JsonSchemaValidationsResourceWithRawResponse:
        return JsonSchemaValidationsResourceWithRawResponse(self._endpoints.json_schema_validations)

    @cached_property
    def tags(self) -> TagsResourceWithRawResponse:
        return TagsResourceWithRawResponse(self._endpoints.tags)


class AsyncEndpointsResourceWithRawResponse:
    def __init__(self, endpoints: AsyncEndpointsResource) -> None:
        self._endpoints = endpoints

    @cached_property
    def authentication_type_validations(self) -> AsyncAuthenticationTypeValidationsResourceWithRawResponse:
        return AsyncAuthenticationTypeValidationsResourceWithRawResponse(
            self._endpoints.authentication_type_validations
        )

    @cached_property
    def json_schema_validations(self) -> AsyncJsonSchemaValidationsResourceWithRawResponse:
        return AsyncJsonSchemaValidationsResourceWithRawResponse(self._endpoints.json_schema_validations)

    @cached_property
    def tags(self) -> AsyncTagsResourceWithRawResponse:
        return AsyncTagsResourceWithRawResponse(self._endpoints.tags)


class EndpointsResourceWithStreamingResponse:
    def __init__(self, endpoints: EndpointsResource) -> None:
        self._endpoints = endpoints

    @cached_property
    def authentication_type_validations(self) -> AuthenticationTypeValidationsResourceWithStreamingResponse:
        return AuthenticationTypeValidationsResourceWithStreamingResponse(
            self._endpoints.authentication_type_validations
        )

    @cached_property
    def json_schema_validations(self) -> JsonSchemaValidationsResourceWithStreamingResponse:
        return JsonSchemaValidationsResourceWithStreamingResponse(self._endpoints.json_schema_validations)

    @cached_property
    def tags(self) -> TagsResourceWithStreamingResponse:
        return TagsResourceWithStreamingResponse(self._endpoints.tags)


class AsyncEndpointsResourceWithStreamingResponse:
    def __init__(self, endpoints: AsyncEndpointsResource) -> None:
        self._endpoints = endpoints

    @cached_property
    def authentication_type_validations(self) -> AsyncAuthenticationTypeValidationsResourceWithStreamingResponse:
        return AsyncAuthenticationTypeValidationsResourceWithStreamingResponse(
            self._endpoints.authentication_type_validations
        )

    @cached_property
    def json_schema_validations(self) -> AsyncJsonSchemaValidationsResourceWithStreamingResponse:
        return AsyncJsonSchemaValidationsResourceWithStreamingResponse(self._endpoints.json_schema_validations)

    @cached_property
    def tags(self) -> AsyncTagsResourceWithStreamingResponse:
        return AsyncTagsResourceWithStreamingResponse(self._endpoints.tags)
