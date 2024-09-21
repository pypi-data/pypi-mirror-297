# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .notes import (
    NotesResource,
    AsyncNotesResource,
    NotesResourceWithRawResponse,
    AsyncNotesResourceWithRawResponse,
    NotesResourceWithStreamingResponse,
    AsyncNotesResourceWithStreamingResponse,
)
from .services import (
    ServicesResource,
    AsyncServicesResource,
    ServicesResourceWithRawResponse,
    AsyncServicesResourceWithRawResponse,
    ServicesResourceWithStreamingResponse,
    AsyncServicesResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from .attributes import (
    AttributesResource,
    AsyncAttributesResource,
    AttributesResourceWithRawResponse,
    AsyncAttributesResourceWithRawResponse,
    AttributesResourceWithStreamingResponse,
    AsyncAttributesResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ....types.banks import atm_create_params, atm_update_params
from ...._base_client import make_request_options
from .location_categories import (
    LocationCategoriesResource,
    AsyncLocationCategoriesResource,
    LocationCategoriesResourceWithRawResponse,
    AsyncLocationCategoriesResourceWithRawResponse,
    LocationCategoriesResourceWithStreamingResponse,
    AsyncLocationCategoriesResourceWithStreamingResponse,
)
from .supported_languages import (
    SupportedLanguagesResource,
    AsyncSupportedLanguagesResource,
    SupportedLanguagesResourceWithRawResponse,
    AsyncSupportedLanguagesResourceWithRawResponse,
    SupportedLanguagesResourceWithStreamingResponse,
    AsyncSupportedLanguagesResourceWithStreamingResponse,
)
from .supported_currencies import (
    SupportedCurrenciesResource,
    AsyncSupportedCurrenciesResource,
    SupportedCurrenciesResourceWithRawResponse,
    AsyncSupportedCurrenciesResourceWithRawResponse,
    SupportedCurrenciesResourceWithStreamingResponse,
    AsyncSupportedCurrenciesResourceWithStreamingResponse,
)
from .accessibility_features import (
    AccessibilityFeaturesResource,
    AsyncAccessibilityFeaturesResource,
    AccessibilityFeaturesResourceWithRawResponse,
    AsyncAccessibilityFeaturesResourceWithRawResponse,
    AccessibilityFeaturesResourceWithStreamingResponse,
    AsyncAccessibilityFeaturesResourceWithStreamingResponse,
)

__all__ = ["AtmsResource", "AsyncAtmsResource"]


class AtmsResource(SyncAPIResource):
    @cached_property
    def accessibility_features(self) -> AccessibilityFeaturesResource:
        return AccessibilityFeaturesResource(self._client)

    @cached_property
    def attributes(self) -> AttributesResource:
        return AttributesResource(self._client)

    @cached_property
    def location_categories(self) -> LocationCategoriesResource:
        return LocationCategoriesResource(self._client)

    @cached_property
    def notes(self) -> NotesResource:
        return NotesResource(self._client)

    @cached_property
    def services(self) -> ServicesResource:
        return ServicesResource(self._client)

    @cached_property
    def supported_currencies(self) -> SupportedCurrenciesResource:
        return SupportedCurrenciesResource(self._client)

    @cached_property
    def supported_languages(self) -> SupportedLanguagesResource:
        return SupportedLanguagesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AtmsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AtmsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AtmsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AtmsResourceWithStreamingResponse(self)

    def create(
        self,
        bank_id: str,
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
        <p>Create ATM.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/atms",
            body=maybe_transform(body, atm_create_params.AtmCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def retrieve(
        self,
        atm_id: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Returns information about ATM for a single bank specified by BANK_ID and ATM_ID including:</p><ul><li>Address</li><li>Geo Location</li><li>License the data under this endpoint is released under</li><li>ATM Attributes</li></ul><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        atm_id: str,
        *,
        bank_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Update ATM.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}",
            body=maybe_transform(body, atm_update_params.AtmUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Returns information about ATMs for a single bank specified by BANK_ID including:</p><ul><li>Address</li><li>Geo Location</li><li>License the data under this endpoint is released under</li></ul><p>Pagination:</p><p>By default, 100 records are returned.</p><p>You can use the url query parameters <em>limit</em> and <em>offset</em> for pagination</p><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/atms",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        atm_id: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete ATM.</p><p>This will also delete all its attributes.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncAtmsResource(AsyncAPIResource):
    @cached_property
    def accessibility_features(self) -> AsyncAccessibilityFeaturesResource:
        return AsyncAccessibilityFeaturesResource(self._client)

    @cached_property
    def attributes(self) -> AsyncAttributesResource:
        return AsyncAttributesResource(self._client)

    @cached_property
    def location_categories(self) -> AsyncLocationCategoriesResource:
        return AsyncLocationCategoriesResource(self._client)

    @cached_property
    def notes(self) -> AsyncNotesResource:
        return AsyncNotesResource(self._client)

    @cached_property
    def services(self) -> AsyncServicesResource:
        return AsyncServicesResource(self._client)

    @cached_property
    def supported_currencies(self) -> AsyncSupportedCurrenciesResource:
        return AsyncSupportedCurrenciesResource(self._client)

    @cached_property
    def supported_languages(self) -> AsyncSupportedLanguagesResource:
        return AsyncSupportedLanguagesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAtmsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAtmsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAtmsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAtmsResourceWithStreamingResponse(self)

    async def create(
        self,
        bank_id: str,
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
        <p>Create ATM.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/atms",
            body=await async_maybe_transform(body, atm_create_params.AtmCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def retrieve(
        self,
        atm_id: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Returns information about ATM for a single bank specified by BANK_ID and ATM_ID including:</p><ul><li>Address</li><li>Geo Location</li><li>License the data under this endpoint is released under</li><li>ATM Attributes</li></ul><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        atm_id: str,
        *,
        bank_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Update ATM.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}",
            body=await async_maybe_transform(body, atm_update_params.AtmUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Returns information about ATMs for a single bank specified by BANK_ID including:</p><ul><li>Address</li><li>Geo Location</li><li>License the data under this endpoint is released under</li></ul><p>Pagination:</p><p>By default, 100 records are returned.</p><p>You can use the url query parameters <em>limit</em> and <em>offset</em> for pagination</p><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/atms",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        atm_id: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete ATM.</p><p>This will also delete all its attributes.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not atm_id:
            raise ValueError(f"Expected a non-empty value for `atm_id` but received {atm_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AtmsResourceWithRawResponse:
    def __init__(self, atms: AtmsResource) -> None:
        self._atms = atms

        self.create = to_custom_raw_response_wrapper(
            atms.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            atms.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            atms.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            atms.list,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            atms.delete,
        )

    @cached_property
    def accessibility_features(self) -> AccessibilityFeaturesResourceWithRawResponse:
        return AccessibilityFeaturesResourceWithRawResponse(self._atms.accessibility_features)

    @cached_property
    def attributes(self) -> AttributesResourceWithRawResponse:
        return AttributesResourceWithRawResponse(self._atms.attributes)

    @cached_property
    def location_categories(self) -> LocationCategoriesResourceWithRawResponse:
        return LocationCategoriesResourceWithRawResponse(self._atms.location_categories)

    @cached_property
    def notes(self) -> NotesResourceWithRawResponse:
        return NotesResourceWithRawResponse(self._atms.notes)

    @cached_property
    def services(self) -> ServicesResourceWithRawResponse:
        return ServicesResourceWithRawResponse(self._atms.services)

    @cached_property
    def supported_currencies(self) -> SupportedCurrenciesResourceWithRawResponse:
        return SupportedCurrenciesResourceWithRawResponse(self._atms.supported_currencies)

    @cached_property
    def supported_languages(self) -> SupportedLanguagesResourceWithRawResponse:
        return SupportedLanguagesResourceWithRawResponse(self._atms.supported_languages)


class AsyncAtmsResourceWithRawResponse:
    def __init__(self, atms: AsyncAtmsResource) -> None:
        self._atms = atms

        self.create = async_to_custom_raw_response_wrapper(
            atms.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            atms.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            atms.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            atms.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            atms.delete,
        )

    @cached_property
    def accessibility_features(self) -> AsyncAccessibilityFeaturesResourceWithRawResponse:
        return AsyncAccessibilityFeaturesResourceWithRawResponse(self._atms.accessibility_features)

    @cached_property
    def attributes(self) -> AsyncAttributesResourceWithRawResponse:
        return AsyncAttributesResourceWithRawResponse(self._atms.attributes)

    @cached_property
    def location_categories(self) -> AsyncLocationCategoriesResourceWithRawResponse:
        return AsyncLocationCategoriesResourceWithRawResponse(self._atms.location_categories)

    @cached_property
    def notes(self) -> AsyncNotesResourceWithRawResponse:
        return AsyncNotesResourceWithRawResponse(self._atms.notes)

    @cached_property
    def services(self) -> AsyncServicesResourceWithRawResponse:
        return AsyncServicesResourceWithRawResponse(self._atms.services)

    @cached_property
    def supported_currencies(self) -> AsyncSupportedCurrenciesResourceWithRawResponse:
        return AsyncSupportedCurrenciesResourceWithRawResponse(self._atms.supported_currencies)

    @cached_property
    def supported_languages(self) -> AsyncSupportedLanguagesResourceWithRawResponse:
        return AsyncSupportedLanguagesResourceWithRawResponse(self._atms.supported_languages)


class AtmsResourceWithStreamingResponse:
    def __init__(self, atms: AtmsResource) -> None:
        self._atms = atms

        self.create = to_custom_streamed_response_wrapper(
            atms.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            atms.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            atms.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            atms.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            atms.delete,
        )

    @cached_property
    def accessibility_features(self) -> AccessibilityFeaturesResourceWithStreamingResponse:
        return AccessibilityFeaturesResourceWithStreamingResponse(self._atms.accessibility_features)

    @cached_property
    def attributes(self) -> AttributesResourceWithStreamingResponse:
        return AttributesResourceWithStreamingResponse(self._atms.attributes)

    @cached_property
    def location_categories(self) -> LocationCategoriesResourceWithStreamingResponse:
        return LocationCategoriesResourceWithStreamingResponse(self._atms.location_categories)

    @cached_property
    def notes(self) -> NotesResourceWithStreamingResponse:
        return NotesResourceWithStreamingResponse(self._atms.notes)

    @cached_property
    def services(self) -> ServicesResourceWithStreamingResponse:
        return ServicesResourceWithStreamingResponse(self._atms.services)

    @cached_property
    def supported_currencies(self) -> SupportedCurrenciesResourceWithStreamingResponse:
        return SupportedCurrenciesResourceWithStreamingResponse(self._atms.supported_currencies)

    @cached_property
    def supported_languages(self) -> SupportedLanguagesResourceWithStreamingResponse:
        return SupportedLanguagesResourceWithStreamingResponse(self._atms.supported_languages)


class AsyncAtmsResourceWithStreamingResponse:
    def __init__(self, atms: AsyncAtmsResource) -> None:
        self._atms = atms

        self.create = async_to_custom_streamed_response_wrapper(
            atms.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            atms.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            atms.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            atms.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            atms.delete,
        )

    @cached_property
    def accessibility_features(self) -> AsyncAccessibilityFeaturesResourceWithStreamingResponse:
        return AsyncAccessibilityFeaturesResourceWithStreamingResponse(self._atms.accessibility_features)

    @cached_property
    def attributes(self) -> AsyncAttributesResourceWithStreamingResponse:
        return AsyncAttributesResourceWithStreamingResponse(self._atms.attributes)

    @cached_property
    def location_categories(self) -> AsyncLocationCategoriesResourceWithStreamingResponse:
        return AsyncLocationCategoriesResourceWithStreamingResponse(self._atms.location_categories)

    @cached_property
    def notes(self) -> AsyncNotesResourceWithStreamingResponse:
        return AsyncNotesResourceWithStreamingResponse(self._atms.notes)

    @cached_property
    def services(self) -> AsyncServicesResourceWithStreamingResponse:
        return AsyncServicesResourceWithStreamingResponse(self._atms.services)

    @cached_property
    def supported_currencies(self) -> AsyncSupportedCurrenciesResourceWithStreamingResponse:
        return AsyncSupportedCurrenciesResourceWithStreamingResponse(self._atms.supported_currencies)

    @cached_property
    def supported_languages(self) -> AsyncSupportedLanguagesResourceWithStreamingResponse:
        return AsyncSupportedLanguagesResourceWithStreamingResponse(self._atms.supported_languages)
