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
from ...types.consumers import redirect_url_update_params

__all__ = ["RedirectURLResource", "AsyncRedirectURLResource"]


class RedirectURLResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RedirectURLResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return RedirectURLResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RedirectURLResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return RedirectURLResourceWithStreamingResponse(self)

    def update(
        self,
        consumer_id: str,
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
        <p>Update an existing redirectUrl for a Consumer specified by CONSUMER_ID.</p><p>Please note: Your consumer may be disabled as a result of this action.</p><p>CONSUMER_ID can be obtained after you register the application.</p><p>Or use the endpoint 'Get Consumers' to get it</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not consumer_id:
            raise ValueError(f"Expected a non-empty value for `consumer_id` but received {consumer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/management/consumers/{consumer_id}/consumer/redirect_url",
            body=maybe_transform(body, redirect_url_update_params.RedirectURLUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncRedirectURLResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRedirectURLResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRedirectURLResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRedirectURLResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncRedirectURLResourceWithStreamingResponse(self)

    async def update(
        self,
        consumer_id: str,
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
        <p>Update an existing redirectUrl for a Consumer specified by CONSUMER_ID.</p><p>Please note: Your consumer may be disabled as a result of this action.</p><p>CONSUMER_ID can be obtained after you register the application.</p><p>Or use the endpoint 'Get Consumers' to get it</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not consumer_id:
            raise ValueError(f"Expected a non-empty value for `consumer_id` but received {consumer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/management/consumers/{consumer_id}/consumer/redirect_url",
            body=await async_maybe_transform(body, redirect_url_update_params.RedirectURLUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class RedirectURLResourceWithRawResponse:
    def __init__(self, redirect_url: RedirectURLResource) -> None:
        self._redirect_url = redirect_url

        self.update = to_custom_raw_response_wrapper(
            redirect_url.update,
            BinaryAPIResponse,
        )


class AsyncRedirectURLResourceWithRawResponse:
    def __init__(self, redirect_url: AsyncRedirectURLResource) -> None:
        self._redirect_url = redirect_url

        self.update = async_to_custom_raw_response_wrapper(
            redirect_url.update,
            AsyncBinaryAPIResponse,
        )


class RedirectURLResourceWithStreamingResponse:
    def __init__(self, redirect_url: RedirectURLResource) -> None:
        self._redirect_url = redirect_url

        self.update = to_custom_streamed_response_wrapper(
            redirect_url.update,
            StreamedBinaryAPIResponse,
        )


class AsyncRedirectURLResourceWithStreamingResponse:
    def __init__(self, redirect_url: AsyncRedirectURLResource) -> None:
        self._redirect_url = redirect_url

        self.update = async_to_custom_streamed_response_wrapper(
            redirect_url.update,
            AsyncStreamedBinaryAPIResponse,
        )
