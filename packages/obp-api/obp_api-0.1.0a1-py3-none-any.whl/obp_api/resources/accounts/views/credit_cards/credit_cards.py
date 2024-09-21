# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .orders import (
    OrdersResource,
    AsyncOrdersResource,
    OrdersResourceWithRawResponse,
    AsyncOrdersResourceWithRawResponse,
    OrdersResourceWithStreamingResponse,
    AsyncOrdersResourceWithStreamingResponse,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["CreditCardsResource", "AsyncCreditCardsResource"]


class CreditCardsResource(SyncAPIResource):
    @cached_property
    def orders(self) -> OrdersResource:
        return OrdersResource(self._client)

    @cached_property
    def with_raw_response(self) -> CreditCardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CreditCardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CreditCardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CreditCardsResourceWithStreamingResponse(self)


class AsyncCreditCardsResource(AsyncAPIResource):
    @cached_property
    def orders(self) -> AsyncOrdersResource:
        return AsyncOrdersResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCreditCardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCreditCardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCreditCardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCreditCardsResourceWithStreamingResponse(self)


class CreditCardsResourceWithRawResponse:
    def __init__(self, credit_cards: CreditCardsResource) -> None:
        self._credit_cards = credit_cards

    @cached_property
    def orders(self) -> OrdersResourceWithRawResponse:
        return OrdersResourceWithRawResponse(self._credit_cards.orders)


class AsyncCreditCardsResourceWithRawResponse:
    def __init__(self, credit_cards: AsyncCreditCardsResource) -> None:
        self._credit_cards = credit_cards

    @cached_property
    def orders(self) -> AsyncOrdersResourceWithRawResponse:
        return AsyncOrdersResourceWithRawResponse(self._credit_cards.orders)


class CreditCardsResourceWithStreamingResponse:
    def __init__(self, credit_cards: CreditCardsResource) -> None:
        self._credit_cards = credit_cards

    @cached_property
    def orders(self) -> OrdersResourceWithStreamingResponse:
        return OrdersResourceWithStreamingResponse(self._credit_cards.orders)


class AsyncCreditCardsResourceWithStreamingResponse:
    def __init__(self, credit_cards: AsyncCreditCardsResource) -> None:
        self._credit_cards = credit_cards

    @cached_property
    def orders(self) -> AsyncOrdersResourceWithStreamingResponse:
        return AsyncOrdersResourceWithStreamingResponse(self._credit_cards.orders)
