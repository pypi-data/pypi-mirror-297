# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .balances import (
    BalancesResource,
    AsyncBalancesResource,
    BalancesResourceWithRawResponse,
    AsyncBalancesResourceWithRawResponse,
    BalancesResourceWithStreamingResponse,
    AsyncBalancesResourceWithStreamingResponse,
)
from .metadata import (
    MetadataResource,
    AsyncMetadataResource,
    MetadataResourceWithRawResponse,
    AsyncMetadataResourceWithRawResponse,
    MetadataResourceWithStreamingResponse,
    AsyncMetadataResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .credit_cards import (
    CreditCardsResource,
    AsyncCreditCardsResource,
    CreditCardsResourceWithRawResponse,
    AsyncCreditCardsResourceWithRawResponse,
    CreditCardsResourceWithStreamingResponse,
    AsyncCreditCardsResourceWithStreamingResponse,
)
from .target_views import (
    TargetViewsResource,
    AsyncTargetViewsResource,
    TargetViewsResourceWithRawResponse,
    AsyncTargetViewsResourceWithRawResponse,
    TargetViewsResourceWithStreamingResponse,
    AsyncTargetViewsResourceWithStreamingResponse,
)
from .direct_debits import (
    DirectDebitsResource,
    AsyncDirectDebitsResource,
    DirectDebitsResourceWithRawResponse,
    AsyncDirectDebitsResourceWithRawResponse,
    DirectDebitsResourceWithStreamingResponse,
    AsyncDirectDebitsResourceWithStreamingResponse,
)
from .counterparties import (
    CounterpartiesResource,
    AsyncCounterpartiesResource,
    CounterpartiesResourceWithRawResponse,
    AsyncCounterpartiesResourceWithRawResponse,
    CounterpartiesResourceWithStreamingResponse,
    AsyncCounterpartiesResourceWithStreamingResponse,
)
from .funds_available import (
    FundsAvailableResource,
    AsyncFundsAvailableResource,
    FundsAvailableResourceWithRawResponse,
    AsyncFundsAvailableResourceWithRawResponse,
    FundsAvailableResourceWithStreamingResponse,
    AsyncFundsAvailableResourceWithStreamingResponse,
)
from .metadata.metadata import MetadataResource, AsyncMetadataResource
from .user_account_access import (
    UserAccountAccessResource,
    AsyncUserAccountAccessResource,
    UserAccountAccessResourceWithRawResponse,
    AsyncUserAccountAccessResourceWithRawResponse,
    UserAccountAccessResourceWithStreamingResponse,
    AsyncUserAccountAccessResourceWithStreamingResponse,
)
from .credit_cards.credit_cards import CreditCardsResource, AsyncCreditCardsResource
from .counterparties.counterparties import CounterpartiesResource, AsyncCounterpartiesResource

__all__ = ["ViewsResource", "AsyncViewsResource"]


class ViewsResource(SyncAPIResource):
    @cached_property
    def credit_cards(self) -> CreditCardsResource:
        return CreditCardsResource(self._client)

    @cached_property
    def direct_debits(self) -> DirectDebitsResource:
        return DirectDebitsResource(self._client)

    @cached_property
    def funds_available(self) -> FundsAvailableResource:
        return FundsAvailableResource(self._client)

    @cached_property
    def metadata(self) -> MetadataResource:
        return MetadataResource(self._client)

    @cached_property
    def counterparties(self) -> CounterpartiesResource:
        return CounterpartiesResource(self._client)

    @cached_property
    def balances(self) -> BalancesResource:
        return BalancesResource(self._client)

    @cached_property
    def target_views(self) -> TargetViewsResource:
        return TargetViewsResource(self._client)

    @cached_property
    def user_account_access(self) -> UserAccountAccessResource:
        return UserAccountAccessResource(self._client)

    @cached_property
    def with_raw_response(self) -> ViewsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ViewsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ViewsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ViewsResourceWithStreamingResponse(self)


class AsyncViewsResource(AsyncAPIResource):
    @cached_property
    def credit_cards(self) -> AsyncCreditCardsResource:
        return AsyncCreditCardsResource(self._client)

    @cached_property
    def direct_debits(self) -> AsyncDirectDebitsResource:
        return AsyncDirectDebitsResource(self._client)

    @cached_property
    def funds_available(self) -> AsyncFundsAvailableResource:
        return AsyncFundsAvailableResource(self._client)

    @cached_property
    def metadata(self) -> AsyncMetadataResource:
        return AsyncMetadataResource(self._client)

    @cached_property
    def counterparties(self) -> AsyncCounterpartiesResource:
        return AsyncCounterpartiesResource(self._client)

    @cached_property
    def balances(self) -> AsyncBalancesResource:
        return AsyncBalancesResource(self._client)

    @cached_property
    def target_views(self) -> AsyncTargetViewsResource:
        return AsyncTargetViewsResource(self._client)

    @cached_property
    def user_account_access(self) -> AsyncUserAccountAccessResource:
        return AsyncUserAccountAccessResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncViewsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncViewsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncViewsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncViewsResourceWithStreamingResponse(self)


class ViewsResourceWithRawResponse:
    def __init__(self, views: ViewsResource) -> None:
        self._views = views

    @cached_property
    def credit_cards(self) -> CreditCardsResourceWithRawResponse:
        return CreditCardsResourceWithRawResponse(self._views.credit_cards)

    @cached_property
    def direct_debits(self) -> DirectDebitsResourceWithRawResponse:
        return DirectDebitsResourceWithRawResponse(self._views.direct_debits)

    @cached_property
    def funds_available(self) -> FundsAvailableResourceWithRawResponse:
        return FundsAvailableResourceWithRawResponse(self._views.funds_available)

    @cached_property
    def metadata(self) -> MetadataResourceWithRawResponse:
        return MetadataResourceWithRawResponse(self._views.metadata)

    @cached_property
    def counterparties(self) -> CounterpartiesResourceWithRawResponse:
        return CounterpartiesResourceWithRawResponse(self._views.counterparties)

    @cached_property
    def balances(self) -> BalancesResourceWithRawResponse:
        return BalancesResourceWithRawResponse(self._views.balances)

    @cached_property
    def target_views(self) -> TargetViewsResourceWithRawResponse:
        return TargetViewsResourceWithRawResponse(self._views.target_views)

    @cached_property
    def user_account_access(self) -> UserAccountAccessResourceWithRawResponse:
        return UserAccountAccessResourceWithRawResponse(self._views.user_account_access)


class AsyncViewsResourceWithRawResponse:
    def __init__(self, views: AsyncViewsResource) -> None:
        self._views = views

    @cached_property
    def credit_cards(self) -> AsyncCreditCardsResourceWithRawResponse:
        return AsyncCreditCardsResourceWithRawResponse(self._views.credit_cards)

    @cached_property
    def direct_debits(self) -> AsyncDirectDebitsResourceWithRawResponse:
        return AsyncDirectDebitsResourceWithRawResponse(self._views.direct_debits)

    @cached_property
    def funds_available(self) -> AsyncFundsAvailableResourceWithRawResponse:
        return AsyncFundsAvailableResourceWithRawResponse(self._views.funds_available)

    @cached_property
    def metadata(self) -> AsyncMetadataResourceWithRawResponse:
        return AsyncMetadataResourceWithRawResponse(self._views.metadata)

    @cached_property
    def counterparties(self) -> AsyncCounterpartiesResourceWithRawResponse:
        return AsyncCounterpartiesResourceWithRawResponse(self._views.counterparties)

    @cached_property
    def balances(self) -> AsyncBalancesResourceWithRawResponse:
        return AsyncBalancesResourceWithRawResponse(self._views.balances)

    @cached_property
    def target_views(self) -> AsyncTargetViewsResourceWithRawResponse:
        return AsyncTargetViewsResourceWithRawResponse(self._views.target_views)

    @cached_property
    def user_account_access(self) -> AsyncUserAccountAccessResourceWithRawResponse:
        return AsyncUserAccountAccessResourceWithRawResponse(self._views.user_account_access)


class ViewsResourceWithStreamingResponse:
    def __init__(self, views: ViewsResource) -> None:
        self._views = views

    @cached_property
    def credit_cards(self) -> CreditCardsResourceWithStreamingResponse:
        return CreditCardsResourceWithStreamingResponse(self._views.credit_cards)

    @cached_property
    def direct_debits(self) -> DirectDebitsResourceWithStreamingResponse:
        return DirectDebitsResourceWithStreamingResponse(self._views.direct_debits)

    @cached_property
    def funds_available(self) -> FundsAvailableResourceWithStreamingResponse:
        return FundsAvailableResourceWithStreamingResponse(self._views.funds_available)

    @cached_property
    def metadata(self) -> MetadataResourceWithStreamingResponse:
        return MetadataResourceWithStreamingResponse(self._views.metadata)

    @cached_property
    def counterparties(self) -> CounterpartiesResourceWithStreamingResponse:
        return CounterpartiesResourceWithStreamingResponse(self._views.counterparties)

    @cached_property
    def balances(self) -> BalancesResourceWithStreamingResponse:
        return BalancesResourceWithStreamingResponse(self._views.balances)

    @cached_property
    def target_views(self) -> TargetViewsResourceWithStreamingResponse:
        return TargetViewsResourceWithStreamingResponse(self._views.target_views)

    @cached_property
    def user_account_access(self) -> UserAccountAccessResourceWithStreamingResponse:
        return UserAccountAccessResourceWithStreamingResponse(self._views.user_account_access)


class AsyncViewsResourceWithStreamingResponse:
    def __init__(self, views: AsyncViewsResource) -> None:
        self._views = views

    @cached_property
    def credit_cards(self) -> AsyncCreditCardsResourceWithStreamingResponse:
        return AsyncCreditCardsResourceWithStreamingResponse(self._views.credit_cards)

    @cached_property
    def direct_debits(self) -> AsyncDirectDebitsResourceWithStreamingResponse:
        return AsyncDirectDebitsResourceWithStreamingResponse(self._views.direct_debits)

    @cached_property
    def funds_available(self) -> AsyncFundsAvailableResourceWithStreamingResponse:
        return AsyncFundsAvailableResourceWithStreamingResponse(self._views.funds_available)

    @cached_property
    def metadata(self) -> AsyncMetadataResourceWithStreamingResponse:
        return AsyncMetadataResourceWithStreamingResponse(self._views.metadata)

    @cached_property
    def counterparties(self) -> AsyncCounterpartiesResourceWithStreamingResponse:
        return AsyncCounterpartiesResourceWithStreamingResponse(self._views.counterparties)

    @cached_property
    def balances(self) -> AsyncBalancesResourceWithStreamingResponse:
        return AsyncBalancesResourceWithStreamingResponse(self._views.balances)

    @cached_property
    def target_views(self) -> AsyncTargetViewsResourceWithStreamingResponse:
        return AsyncTargetViewsResourceWithStreamingResponse(self._views.target_views)

    @cached_property
    def user_account_access(self) -> AsyncUserAccountAccessResourceWithStreamingResponse:
        return AsyncUserAccountAccessResourceWithStreamingResponse(self._views.user_account_access)
