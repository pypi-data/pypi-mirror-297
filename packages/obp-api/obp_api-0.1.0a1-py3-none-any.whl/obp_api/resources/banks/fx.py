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
from ...types.banks import fx_update_params
from ..._base_client import make_request_options

__all__ = ["FxResource", "AsyncFxResource"]


class FxResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FxResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return FxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FxResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return FxResourceWithStreamingResponse(self)

    def retrieve(
        self,
        to_currency_code: str,
        *,
        bank_id: str,
        from_currency_code: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Get the latest FX rate specified by BANK_ID, FROM_CURRENCY_CODE and TO_CURRENCY_CODE</p><p>OBP may try different sources of FX rate information depending on the Connector in operation.</p><p>For example we want to convert EUR =&gt; USD:</p><p>OBP will:<br />1st try - Connector (database, core banking system or external FX service)<br />2nd try part 1 - fallbackexchangerates/eur.json<br />2nd try part 2 - fallbackexchangerates/usd.json (the inverse rate is used)<br />3rd try - Hardcoded map of FX rates.</p><p><img src="https://user-images.githubusercontent.com/485218/60005085-1eded600-966e-11e9-96fb-798b102d9ad0.png" alt="FX Flow" /></p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not from_currency_code:
            raise ValueError(f"Expected a non-empty value for `from_currency_code` but received {from_currency_code!r}")
        if not to_currency_code:
            raise ValueError(f"Expected a non-empty value for `to_currency_code` but received {to_currency_code!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/fx/{from_currency_code}/{to_currency_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
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
        <p>Create or Update Fx for the Bank.</p><p>Example:</p><p>“from_currency_code”:“EUR”,<br />“to_currency_code”:“USD”,<br />“conversion_value”: 1.136305,<br />“inverse_conversion_value”: 1 / 1.136305 = 0.8800454103431737,</p><p>Thus 1 Euro = 1.136305 US Dollar<br />and<br />1 US Dollar = 0.8800 Euro</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/fx",
            body=maybe_transform(body, fx_update_params.FxUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncFxResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFxResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFxResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncFxResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        to_currency_code: str,
        *,
        bank_id: str,
        from_currency_code: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Get the latest FX rate specified by BANK_ID, FROM_CURRENCY_CODE and TO_CURRENCY_CODE</p><p>OBP may try different sources of FX rate information depending on the Connector in operation.</p><p>For example we want to convert EUR =&gt; USD:</p><p>OBP will:<br />1st try - Connector (database, core banking system or external FX service)<br />2nd try part 1 - fallbackexchangerates/eur.json<br />2nd try part 2 - fallbackexchangerates/usd.json (the inverse rate is used)<br />3rd try - Hardcoded map of FX rates.</p><p><img src="https://user-images.githubusercontent.com/485218/60005085-1eded600-966e-11e9-96fb-798b102d9ad0.png" alt="FX Flow" /></p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not from_currency_code:
            raise ValueError(f"Expected a non-empty value for `from_currency_code` but received {from_currency_code!r}")
        if not to_currency_code:
            raise ValueError(f"Expected a non-empty value for `to_currency_code` but received {to_currency_code!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/fx/{from_currency_code}/{to_currency_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
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
        <p>Create or Update Fx for the Bank.</p><p>Example:</p><p>“from_currency_code”:“EUR”,<br />“to_currency_code”:“USD”,<br />“conversion_value”: 1.136305,<br />“inverse_conversion_value”: 1 / 1.136305 = 0.8800454103431737,</p><p>Thus 1 Euro = 1.136305 US Dollar<br />and<br />1 US Dollar = 0.8800 Euro</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/fx",
            body=await async_maybe_transform(body, fx_update_params.FxUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class FxResourceWithRawResponse:
    def __init__(self, fx: FxResource) -> None:
        self._fx = fx

        self.retrieve = to_custom_raw_response_wrapper(
            fx.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            fx.update,
            BinaryAPIResponse,
        )


class AsyncFxResourceWithRawResponse:
    def __init__(self, fx: AsyncFxResource) -> None:
        self._fx = fx

        self.retrieve = async_to_custom_raw_response_wrapper(
            fx.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            fx.update,
            AsyncBinaryAPIResponse,
        )


class FxResourceWithStreamingResponse:
    def __init__(self, fx: FxResource) -> None:
        self._fx = fx

        self.retrieve = to_custom_streamed_response_wrapper(
            fx.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            fx.update,
            StreamedBinaryAPIResponse,
        )


class AsyncFxResourceWithStreamingResponse:
    def __init__(self, fx: AsyncFxResource) -> None:
        self._fx = fx

        self.retrieve = async_to_custom_streamed_response_wrapper(
            fx.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            fx.update,
            AsyncStreamedBinaryAPIResponse,
        )
