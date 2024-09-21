# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .card import (
    CardResource,
    AsyncCardResource,
    CardResourceWithRawResponse,
    AsyncCardResourceWithRawResponse,
    CardResourceWithStreamingResponse,
    AsyncCardResourceWithStreamingResponse,
)
from .banks import (
    BanksResource,
    AsyncBanksResource,
    BanksResourceWithRawResponse,
    AsyncBanksResourceWithRawResponse,
    BanksResourceWithStreamingResponse,
    AsyncBanksResourceWithStreamingResponse,
)
from .cards import (
    CardsResource,
    AsyncCardsResource,
    CardsResourceWithRawResponse,
    AsyncCardsResourceWithRawResponse,
    CardsResourceWithStreamingResponse,
    AsyncCardsResourceWithStreamingResponse,
)
from .product import (
    ProductResource,
    AsyncProductResource,
    ProductResourceWithRawResponse,
    AsyncProductResourceWithRawResponse,
    ProductResourceWithStreamingResponse,
    AsyncProductResourceWithStreamingResponse,
)
from .accounts import (
    AccountsResource,
    AsyncAccountsResource,
    AccountsResourceWithRawResponse,
    AsyncAccountsResourceWithRawResponse,
    AccountsResourceWithStreamingResponse,
    AsyncAccountsResourceWithStreamingResponse,
)
from .customer import (
    CustomerResource,
    AsyncCustomerResource,
    CustomerResourceWithRawResponse,
    AsyncCustomerResourceWithRawResponse,
    CustomerResourceWithStreamingResponse,
    AsyncCustomerResourceWithStreamingResponse,
)
from .products import (
    ProductsResource,
    AsyncProductsResource,
    ProductsResourceWithRawResponse,
    AsyncProductsResourceWithRawResponse,
    ProductsResourceWithStreamingResponse,
    AsyncProductsResourceWithStreamingResponse,
)
from .customers import (
    CustomersResource,
    AsyncCustomersResource,
    CustomersResourceWithRawResponse,
    AsyncCustomersResourceWithRawResponse,
    CustomersResourceWithStreamingResponse,
    AsyncCustomersResourceWithStreamingResponse,
)
from ...._compat import cached_property
from .transaction import (
    TransactionResource,
    AsyncTransactionResource,
    TransactionResourceWithRawResponse,
    AsyncTransactionResourceWithRawResponse,
    TransactionResourceWithStreamingResponse,
    AsyncTransactionResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from .transactions import (
    TransactionsResource,
    AsyncTransactionsResource,
    TransactionsResourceWithRawResponse,
    AsyncTransactionsResourceWithRawResponse,
    TransactionsResourceWithStreamingResponse,
    AsyncTransactionsResourceWithStreamingResponse,
)
from .transaction_requests import (
    TransactionRequestsResource,
    AsyncTransactionRequestsResource,
    TransactionRequestsResourceWithRawResponse,
    AsyncTransactionRequestsResourceWithRawResponse,
    TransactionRequestsResourceWithStreamingResponse,
    AsyncTransactionRequestsResourceWithStreamingResponse,
)

__all__ = ["AttributeDefinitionsResource", "AsyncAttributeDefinitionsResource"]


class AttributeDefinitionsResource(SyncAPIResource):
    @cached_property
    def accounts(self) -> AccountsResource:
        return AccountsResource(self._client)

    @cached_property
    def cards(self) -> CardsResource:
        return CardsResource(self._client)

    @cached_property
    def customers(self) -> CustomersResource:
        return CustomersResource(self._client)

    @cached_property
    def products(self) -> ProductsResource:
        return ProductsResource(self._client)

    @cached_property
    def transactions(self) -> TransactionsResource:
        return TransactionsResource(self._client)

    @cached_property
    def transaction_requests(self) -> TransactionRequestsResource:
        return TransactionRequestsResource(self._client)

    @cached_property
    def banks(self) -> BanksResource:
        return BanksResource(self._client)

    @cached_property
    def card(self) -> CardResource:
        return CardResource(self._client)

    @cached_property
    def customer(self) -> CustomerResource:
        return CustomerResource(self._client)

    @cached_property
    def product(self) -> ProductResource:
        return ProductResource(self._client)

    @cached_property
    def transaction(self) -> TransactionResource:
        return TransactionResource(self._client)

    @cached_property
    def with_raw_response(self) -> AttributeDefinitionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AttributeDefinitionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AttributeDefinitionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AttributeDefinitionsResourceWithStreamingResponse(self)


class AsyncAttributeDefinitionsResource(AsyncAPIResource):
    @cached_property
    def accounts(self) -> AsyncAccountsResource:
        return AsyncAccountsResource(self._client)

    @cached_property
    def cards(self) -> AsyncCardsResource:
        return AsyncCardsResource(self._client)

    @cached_property
    def customers(self) -> AsyncCustomersResource:
        return AsyncCustomersResource(self._client)

    @cached_property
    def products(self) -> AsyncProductsResource:
        return AsyncProductsResource(self._client)

    @cached_property
    def transactions(self) -> AsyncTransactionsResource:
        return AsyncTransactionsResource(self._client)

    @cached_property
    def transaction_requests(self) -> AsyncTransactionRequestsResource:
        return AsyncTransactionRequestsResource(self._client)

    @cached_property
    def banks(self) -> AsyncBanksResource:
        return AsyncBanksResource(self._client)

    @cached_property
    def card(self) -> AsyncCardResource:
        return AsyncCardResource(self._client)

    @cached_property
    def customer(self) -> AsyncCustomerResource:
        return AsyncCustomerResource(self._client)

    @cached_property
    def product(self) -> AsyncProductResource:
        return AsyncProductResource(self._client)

    @cached_property
    def transaction(self) -> AsyncTransactionResource:
        return AsyncTransactionResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAttributeDefinitionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAttributeDefinitionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAttributeDefinitionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncAttributeDefinitionsResourceWithStreamingResponse(self)


class AttributeDefinitionsResourceWithRawResponse:
    def __init__(self, attribute_definitions: AttributeDefinitionsResource) -> None:
        self._attribute_definitions = attribute_definitions

    @cached_property
    def accounts(self) -> AccountsResourceWithRawResponse:
        return AccountsResourceWithRawResponse(self._attribute_definitions.accounts)

    @cached_property
    def cards(self) -> CardsResourceWithRawResponse:
        return CardsResourceWithRawResponse(self._attribute_definitions.cards)

    @cached_property
    def customers(self) -> CustomersResourceWithRawResponse:
        return CustomersResourceWithRawResponse(self._attribute_definitions.customers)

    @cached_property
    def products(self) -> ProductsResourceWithRawResponse:
        return ProductsResourceWithRawResponse(self._attribute_definitions.products)

    @cached_property
    def transactions(self) -> TransactionsResourceWithRawResponse:
        return TransactionsResourceWithRawResponse(self._attribute_definitions.transactions)

    @cached_property
    def transaction_requests(self) -> TransactionRequestsResourceWithRawResponse:
        return TransactionRequestsResourceWithRawResponse(self._attribute_definitions.transaction_requests)

    @cached_property
    def banks(self) -> BanksResourceWithRawResponse:
        return BanksResourceWithRawResponse(self._attribute_definitions.banks)

    @cached_property
    def card(self) -> CardResourceWithRawResponse:
        return CardResourceWithRawResponse(self._attribute_definitions.card)

    @cached_property
    def customer(self) -> CustomerResourceWithRawResponse:
        return CustomerResourceWithRawResponse(self._attribute_definitions.customer)

    @cached_property
    def product(self) -> ProductResourceWithRawResponse:
        return ProductResourceWithRawResponse(self._attribute_definitions.product)

    @cached_property
    def transaction(self) -> TransactionResourceWithRawResponse:
        return TransactionResourceWithRawResponse(self._attribute_definitions.transaction)


class AsyncAttributeDefinitionsResourceWithRawResponse:
    def __init__(self, attribute_definitions: AsyncAttributeDefinitionsResource) -> None:
        self._attribute_definitions = attribute_definitions

    @cached_property
    def accounts(self) -> AsyncAccountsResourceWithRawResponse:
        return AsyncAccountsResourceWithRawResponse(self._attribute_definitions.accounts)

    @cached_property
    def cards(self) -> AsyncCardsResourceWithRawResponse:
        return AsyncCardsResourceWithRawResponse(self._attribute_definitions.cards)

    @cached_property
    def customers(self) -> AsyncCustomersResourceWithRawResponse:
        return AsyncCustomersResourceWithRawResponse(self._attribute_definitions.customers)

    @cached_property
    def products(self) -> AsyncProductsResourceWithRawResponse:
        return AsyncProductsResourceWithRawResponse(self._attribute_definitions.products)

    @cached_property
    def transactions(self) -> AsyncTransactionsResourceWithRawResponse:
        return AsyncTransactionsResourceWithRawResponse(self._attribute_definitions.transactions)

    @cached_property
    def transaction_requests(self) -> AsyncTransactionRequestsResourceWithRawResponse:
        return AsyncTransactionRequestsResourceWithRawResponse(self._attribute_definitions.transaction_requests)

    @cached_property
    def banks(self) -> AsyncBanksResourceWithRawResponse:
        return AsyncBanksResourceWithRawResponse(self._attribute_definitions.banks)

    @cached_property
    def card(self) -> AsyncCardResourceWithRawResponse:
        return AsyncCardResourceWithRawResponse(self._attribute_definitions.card)

    @cached_property
    def customer(self) -> AsyncCustomerResourceWithRawResponse:
        return AsyncCustomerResourceWithRawResponse(self._attribute_definitions.customer)

    @cached_property
    def product(self) -> AsyncProductResourceWithRawResponse:
        return AsyncProductResourceWithRawResponse(self._attribute_definitions.product)

    @cached_property
    def transaction(self) -> AsyncTransactionResourceWithRawResponse:
        return AsyncTransactionResourceWithRawResponse(self._attribute_definitions.transaction)


class AttributeDefinitionsResourceWithStreamingResponse:
    def __init__(self, attribute_definitions: AttributeDefinitionsResource) -> None:
        self._attribute_definitions = attribute_definitions

    @cached_property
    def accounts(self) -> AccountsResourceWithStreamingResponse:
        return AccountsResourceWithStreamingResponse(self._attribute_definitions.accounts)

    @cached_property
    def cards(self) -> CardsResourceWithStreamingResponse:
        return CardsResourceWithStreamingResponse(self._attribute_definitions.cards)

    @cached_property
    def customers(self) -> CustomersResourceWithStreamingResponse:
        return CustomersResourceWithStreamingResponse(self._attribute_definitions.customers)

    @cached_property
    def products(self) -> ProductsResourceWithStreamingResponse:
        return ProductsResourceWithStreamingResponse(self._attribute_definitions.products)

    @cached_property
    def transactions(self) -> TransactionsResourceWithStreamingResponse:
        return TransactionsResourceWithStreamingResponse(self._attribute_definitions.transactions)

    @cached_property
    def transaction_requests(self) -> TransactionRequestsResourceWithStreamingResponse:
        return TransactionRequestsResourceWithStreamingResponse(self._attribute_definitions.transaction_requests)

    @cached_property
    def banks(self) -> BanksResourceWithStreamingResponse:
        return BanksResourceWithStreamingResponse(self._attribute_definitions.banks)

    @cached_property
    def card(self) -> CardResourceWithStreamingResponse:
        return CardResourceWithStreamingResponse(self._attribute_definitions.card)

    @cached_property
    def customer(self) -> CustomerResourceWithStreamingResponse:
        return CustomerResourceWithStreamingResponse(self._attribute_definitions.customer)

    @cached_property
    def product(self) -> ProductResourceWithStreamingResponse:
        return ProductResourceWithStreamingResponse(self._attribute_definitions.product)

    @cached_property
    def transaction(self) -> TransactionResourceWithStreamingResponse:
        return TransactionResourceWithStreamingResponse(self._attribute_definitions.transaction)


class AsyncAttributeDefinitionsResourceWithStreamingResponse:
    def __init__(self, attribute_definitions: AsyncAttributeDefinitionsResource) -> None:
        self._attribute_definitions = attribute_definitions

    @cached_property
    def accounts(self) -> AsyncAccountsResourceWithStreamingResponse:
        return AsyncAccountsResourceWithStreamingResponse(self._attribute_definitions.accounts)

    @cached_property
    def cards(self) -> AsyncCardsResourceWithStreamingResponse:
        return AsyncCardsResourceWithStreamingResponse(self._attribute_definitions.cards)

    @cached_property
    def customers(self) -> AsyncCustomersResourceWithStreamingResponse:
        return AsyncCustomersResourceWithStreamingResponse(self._attribute_definitions.customers)

    @cached_property
    def products(self) -> AsyncProductsResourceWithStreamingResponse:
        return AsyncProductsResourceWithStreamingResponse(self._attribute_definitions.products)

    @cached_property
    def transactions(self) -> AsyncTransactionsResourceWithStreamingResponse:
        return AsyncTransactionsResourceWithStreamingResponse(self._attribute_definitions.transactions)

    @cached_property
    def transaction_requests(self) -> AsyncTransactionRequestsResourceWithStreamingResponse:
        return AsyncTransactionRequestsResourceWithStreamingResponse(self._attribute_definitions.transaction_requests)

    @cached_property
    def banks(self) -> AsyncBanksResourceWithStreamingResponse:
        return AsyncBanksResourceWithStreamingResponse(self._attribute_definitions.banks)

    @cached_property
    def card(self) -> AsyncCardResourceWithStreamingResponse:
        return AsyncCardResourceWithStreamingResponse(self._attribute_definitions.card)

    @cached_property
    def customer(self) -> AsyncCustomerResourceWithStreamingResponse:
        return AsyncCustomerResourceWithStreamingResponse(self._attribute_definitions.customer)

    @cached_property
    def product(self) -> AsyncProductResourceWithStreamingResponse:
        return AsyncProductResourceWithStreamingResponse(self._attribute_definitions.product)

    @cached_property
    def transaction(self) -> AsyncTransactionResourceWithStreamingResponse:
        return AsyncTransactionResourceWithStreamingResponse(self._attribute_definitions.transaction)
