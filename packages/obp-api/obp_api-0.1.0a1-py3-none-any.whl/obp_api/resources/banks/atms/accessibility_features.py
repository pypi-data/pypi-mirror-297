# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
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
from ....types.banks.atms import accessibility_feature_update_params

__all__ = ["AccessibilityFeaturesResource", "AsyncAccessibilityFeaturesResource"]


class AccessibilityFeaturesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AccessibilityFeaturesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AccessibilityFeaturesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AccessibilityFeaturesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AccessibilityFeaturesResourceWithStreamingResponse(self)

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
        <p>Update ATM Accessibility Features.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/accessibility-features",
            body=maybe_transform(body, accessibility_feature_update_params.AccessibilityFeatureUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAccessibilityFeaturesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAccessibilityFeaturesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAccessibilityFeaturesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAccessibilityFeaturesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAccessibilityFeaturesResourceWithStreamingResponse(self)

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
        <p>Update ATM Accessibility Features.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/atms/{atm_id}/accessibility-features",
            body=await async_maybe_transform(
                body, accessibility_feature_update_params.AccessibilityFeatureUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class AccessibilityFeaturesResourceWithRawResponse:
    def __init__(self, accessibility_features: AccessibilityFeaturesResource) -> None:
        self._accessibility_features = accessibility_features

        self.update = to_custom_raw_response_wrapper(
            accessibility_features.update,
            BinaryAPIResponse,
        )


class AsyncAccessibilityFeaturesResourceWithRawResponse:
    def __init__(self, accessibility_features: AsyncAccessibilityFeaturesResource) -> None:
        self._accessibility_features = accessibility_features

        self.update = async_to_custom_raw_response_wrapper(
            accessibility_features.update,
            AsyncBinaryAPIResponse,
        )


class AccessibilityFeaturesResourceWithStreamingResponse:
    def __init__(self, accessibility_features: AccessibilityFeaturesResource) -> None:
        self._accessibility_features = accessibility_features

        self.update = to_custom_streamed_response_wrapper(
            accessibility_features.update,
            StreamedBinaryAPIResponse,
        )


class AsyncAccessibilityFeaturesResourceWithStreamingResponse:
    def __init__(self, accessibility_features: AsyncAccessibilityFeaturesResource) -> None:
        self._accessibility_features = accessibility_features

        self.update = async_to_custom_streamed_response_wrapper(
            accessibility_features.update,
            AsyncStreamedBinaryAPIResponse,
        )
