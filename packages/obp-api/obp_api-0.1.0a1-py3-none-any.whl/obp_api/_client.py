# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Dict, Union, Mapping, cast
from typing_extensions import Self, Literal, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "ENVIRONMENTS",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "ObpAPI",
    "AsyncObpAPI",
    "Client",
    "AsyncClient",
]

ENVIRONMENTS: Dict[str, str] = {
    "production": "http://apisandbox.openbankproject.com/",
    "environment_1": "https://apisandbox.openbankproject.com/",
}


class ObpAPI(SyncAPIClient):
    accounts: resources.AccountsResource
    adapter: resources.AdapterResource
    api_collections: resources.APICollectionsResource
    api: resources.APIResource
    banks: resources.BanksResource
    accounts_held: resources.AccountsHeldResource
    counterparties: resources.CounterpartiesResource
    transactions: resources.TransactionsResource
    customer_account_links: resources.CustomerAccountLinksResource
    permissions: resources.PermissionsResource
    account_products: resources.AccountProductsResource
    transaction_requests: resources.TransactionRequestsResource
    bank_accounts: resources.BankAccountsResource
    consents: resources.ConsentsResource
    crm_events: resources.CRMEventsResource
    currencies: resources.CurrenciesResource
    customers: resources.CustomersResource
    product_collections: resources.ProductCollectionsResource
    product_tree: resources.ProductTreeResource
    products: resources.ProductsResource
    public_accounts: resources.PublicAccountsResource
    user_invitations: resources.UserInvitationsResource
    user_customer_links: resources.UserCustomerLinksResource
    users: resources.UsersResource
    views: resources.ViewsResource
    web_hooks: resources.WebHooksResource
    cards: resources.CardsResource
    certs: resources.CertsResource
    config: resources.ConfigResource
    connector: resources.ConnectorResource
    consumer: resources.ConsumerResource
    consent_requests: resources.ConsentRequestsResource
    consumers: resources.ConsumersResource
    customers_minimal: resources.CustomersMinimalResource
    database: resources.DatabaseResource
    development: resources.DevelopmentResource
    dynamic_registration: resources.DynamicRegistrationResource
    endpoints: resources.EndpointsResource
    entitlement_requests: resources.EntitlementRequestsResource
    entitlements: resources.EntitlementsResource
    jwks_uris: resources.JwksUrisResource
    management: resources.ManagementResource
    authentication_type_validations: resources.AuthenticationTypeValidationsResource
    standing_orders: resources.StandingOrdersResource
    dynamic_endpoints: resources.DynamicEndpointsResource
    dynamic_message_docs: resources.DynamicMessageDocsResource
    dynamic_resource_docs: resources.DynamicResourceDocsResource
    endpoint_mappings: resources.EndpointMappingsResource
    fast_firehose_accounts: resources.FastFirehoseAccountsResource
    cascading_banks: resources.CascadingBanksResource
    connector_methods: resources.ConnectorMethodsResource
    json_schema_validations: resources.JsonSchemaValidationsResource
    method_routings: resources.MethodRoutingsResource
    metrics: resources.MetricsResource
    system_dynamic_entities: resources.SystemDynamicEntitiesResource
    system_integrity: resources.SystemIntegrityResource
    webui_props: resources.WebuiPropsResource
    documentation: resources.DocumentationResource
    consent: resources.ConsentResource
    correlated_entities: resources.CorrelatedEntitiesResource
    dynamic_entities: resources.DynamicEntitiesResource
    mtls: resources.MtlsResource
    spaces: resources.SpacesResource
    user: resources.UserResource
    rate_limits: resources.RateLimitsResource
    regulated_entities: resources.RegulatedEntitiesResource
    resource_docs: resources.ResourceDocsResource
    roles: resources.RolesResource
    sandbox: resources.SandboxResource
    search: resources.SearchResource
    system_views: resources.SystemViewsResource
    user_entitlements: resources.UserEntitlementsResource
    with_raw_response: ObpAPIWithRawResponse
    with_streaming_response: ObpAPIWithStreamedResponse

    # client options

    _environment: Literal["production", "environment_1"] | NotGiven

    def __init__(
        self,
        *,
        environment: Literal["production", "environment_1"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous obp-api client instance."""
        self._environment = environment

        base_url_env = os.environ.get("OBP_API_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `OBP_API_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.accounts = resources.AccountsResource(self)
        self.adapter = resources.AdapterResource(self)
        self.api_collections = resources.APICollectionsResource(self)
        self.api = resources.APIResource(self)
        self.banks = resources.BanksResource(self)
        self.accounts_held = resources.AccountsHeldResource(self)
        self.counterparties = resources.CounterpartiesResource(self)
        self.transactions = resources.TransactionsResource(self)
        self.customer_account_links = resources.CustomerAccountLinksResource(self)
        self.permissions = resources.PermissionsResource(self)
        self.account_products = resources.AccountProductsResource(self)
        self.transaction_requests = resources.TransactionRequestsResource(self)
        self.bank_accounts = resources.BankAccountsResource(self)
        self.consents = resources.ConsentsResource(self)
        self.crm_events = resources.CRMEventsResource(self)
        self.currencies = resources.CurrenciesResource(self)
        self.customers = resources.CustomersResource(self)
        self.product_collections = resources.ProductCollectionsResource(self)
        self.product_tree = resources.ProductTreeResource(self)
        self.products = resources.ProductsResource(self)
        self.public_accounts = resources.PublicAccountsResource(self)
        self.user_invitations = resources.UserInvitationsResource(self)
        self.user_customer_links = resources.UserCustomerLinksResource(self)
        self.users = resources.UsersResource(self)
        self.views = resources.ViewsResource(self)
        self.web_hooks = resources.WebHooksResource(self)
        self.cards = resources.CardsResource(self)
        self.certs = resources.CertsResource(self)
        self.config = resources.ConfigResource(self)
        self.connector = resources.ConnectorResource(self)
        self.consumer = resources.ConsumerResource(self)
        self.consent_requests = resources.ConsentRequestsResource(self)
        self.consumers = resources.ConsumersResource(self)
        self.customers_minimal = resources.CustomersMinimalResource(self)
        self.database = resources.DatabaseResource(self)
        self.development = resources.DevelopmentResource(self)
        self.dynamic_registration = resources.DynamicRegistrationResource(self)
        self.endpoints = resources.EndpointsResource(self)
        self.entitlement_requests = resources.EntitlementRequestsResource(self)
        self.entitlements = resources.EntitlementsResource(self)
        self.jwks_uris = resources.JwksUrisResource(self)
        self.management = resources.ManagementResource(self)
        self.authentication_type_validations = resources.AuthenticationTypeValidationsResource(self)
        self.standing_orders = resources.StandingOrdersResource(self)
        self.dynamic_endpoints = resources.DynamicEndpointsResource(self)
        self.dynamic_message_docs = resources.DynamicMessageDocsResource(self)
        self.dynamic_resource_docs = resources.DynamicResourceDocsResource(self)
        self.endpoint_mappings = resources.EndpointMappingsResource(self)
        self.fast_firehose_accounts = resources.FastFirehoseAccountsResource(self)
        self.cascading_banks = resources.CascadingBanksResource(self)
        self.connector_methods = resources.ConnectorMethodsResource(self)
        self.json_schema_validations = resources.JsonSchemaValidationsResource(self)
        self.method_routings = resources.MethodRoutingsResource(self)
        self.metrics = resources.MetricsResource(self)
        self.system_dynamic_entities = resources.SystemDynamicEntitiesResource(self)
        self.system_integrity = resources.SystemIntegrityResource(self)
        self.webui_props = resources.WebuiPropsResource(self)
        self.documentation = resources.DocumentationResource(self)
        self.consent = resources.ConsentResource(self)
        self.correlated_entities = resources.CorrelatedEntitiesResource(self)
        self.dynamic_entities = resources.DynamicEntitiesResource(self)
        self.mtls = resources.MtlsResource(self)
        self.spaces = resources.SpacesResource(self)
        self.user = resources.UserResource(self)
        self.rate_limits = resources.RateLimitsResource(self)
        self.regulated_entities = resources.RegulatedEntitiesResource(self)
        self.resource_docs = resources.ResourceDocsResource(self)
        self.roles = resources.RolesResource(self)
        self.sandbox = resources.SandboxResource(self)
        self.search = resources.SearchResource(self)
        self.system_views = resources.SystemViewsResource(self)
        self.user_entitlements = resources.UserEntitlementsResource(self)
        self.with_raw_response = ObpAPIWithRawResponse(self)
        self.with_streaming_response = ObpAPIWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        environment: Literal["production", "environment_1"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncObpAPI(AsyncAPIClient):
    accounts: resources.AsyncAccountsResource
    adapter: resources.AsyncAdapterResource
    api_collections: resources.AsyncAPICollectionsResource
    api: resources.AsyncAPIResource
    banks: resources.AsyncBanksResource
    accounts_held: resources.AsyncAccountsHeldResource
    counterparties: resources.AsyncCounterpartiesResource
    transactions: resources.AsyncTransactionsResource
    customer_account_links: resources.AsyncCustomerAccountLinksResource
    permissions: resources.AsyncPermissionsResource
    account_products: resources.AsyncAccountProductsResource
    transaction_requests: resources.AsyncTransactionRequestsResource
    bank_accounts: resources.AsyncBankAccountsResource
    consents: resources.AsyncConsentsResource
    crm_events: resources.AsyncCRMEventsResource
    currencies: resources.AsyncCurrenciesResource
    customers: resources.AsyncCustomersResource
    product_collections: resources.AsyncProductCollectionsResource
    product_tree: resources.AsyncProductTreeResource
    products: resources.AsyncProductsResource
    public_accounts: resources.AsyncPublicAccountsResource
    user_invitations: resources.AsyncUserInvitationsResource
    user_customer_links: resources.AsyncUserCustomerLinksResource
    users: resources.AsyncUsersResource
    views: resources.AsyncViewsResource
    web_hooks: resources.AsyncWebHooksResource
    cards: resources.AsyncCardsResource
    certs: resources.AsyncCertsResource
    config: resources.AsyncConfigResource
    connector: resources.AsyncConnectorResource
    consumer: resources.AsyncConsumerResource
    consent_requests: resources.AsyncConsentRequestsResource
    consumers: resources.AsyncConsumersResource
    customers_minimal: resources.AsyncCustomersMinimalResource
    database: resources.AsyncDatabaseResource
    development: resources.AsyncDevelopmentResource
    dynamic_registration: resources.AsyncDynamicRegistrationResource
    endpoints: resources.AsyncEndpointsResource
    entitlement_requests: resources.AsyncEntitlementRequestsResource
    entitlements: resources.AsyncEntitlementsResource
    jwks_uris: resources.AsyncJwksUrisResource
    management: resources.AsyncManagementResource
    authentication_type_validations: resources.AsyncAuthenticationTypeValidationsResource
    standing_orders: resources.AsyncStandingOrdersResource
    dynamic_endpoints: resources.AsyncDynamicEndpointsResource
    dynamic_message_docs: resources.AsyncDynamicMessageDocsResource
    dynamic_resource_docs: resources.AsyncDynamicResourceDocsResource
    endpoint_mappings: resources.AsyncEndpointMappingsResource
    fast_firehose_accounts: resources.AsyncFastFirehoseAccountsResource
    cascading_banks: resources.AsyncCascadingBanksResource
    connector_methods: resources.AsyncConnectorMethodsResource
    json_schema_validations: resources.AsyncJsonSchemaValidationsResource
    method_routings: resources.AsyncMethodRoutingsResource
    metrics: resources.AsyncMetricsResource
    system_dynamic_entities: resources.AsyncSystemDynamicEntitiesResource
    system_integrity: resources.AsyncSystemIntegrityResource
    webui_props: resources.AsyncWebuiPropsResource
    documentation: resources.AsyncDocumentationResource
    consent: resources.AsyncConsentResource
    correlated_entities: resources.AsyncCorrelatedEntitiesResource
    dynamic_entities: resources.AsyncDynamicEntitiesResource
    mtls: resources.AsyncMtlsResource
    spaces: resources.AsyncSpacesResource
    user: resources.AsyncUserResource
    rate_limits: resources.AsyncRateLimitsResource
    regulated_entities: resources.AsyncRegulatedEntitiesResource
    resource_docs: resources.AsyncResourceDocsResource
    roles: resources.AsyncRolesResource
    sandbox: resources.AsyncSandboxResource
    search: resources.AsyncSearchResource
    system_views: resources.AsyncSystemViewsResource
    user_entitlements: resources.AsyncUserEntitlementsResource
    with_raw_response: AsyncObpAPIWithRawResponse
    with_streaming_response: AsyncObpAPIWithStreamedResponse

    # client options

    _environment: Literal["production", "environment_1"] | NotGiven

    def __init__(
        self,
        *,
        environment: Literal["production", "environment_1"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async obp-api client instance."""
        self._environment = environment

        base_url_env = os.environ.get("OBP_API_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `OBP_API_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.accounts = resources.AsyncAccountsResource(self)
        self.adapter = resources.AsyncAdapterResource(self)
        self.api_collections = resources.AsyncAPICollectionsResource(self)
        self.api = resources.AsyncAPIResource(self)
        self.banks = resources.AsyncBanksResource(self)
        self.accounts_held = resources.AsyncAccountsHeldResource(self)
        self.counterparties = resources.AsyncCounterpartiesResource(self)
        self.transactions = resources.AsyncTransactionsResource(self)
        self.customer_account_links = resources.AsyncCustomerAccountLinksResource(self)
        self.permissions = resources.AsyncPermissionsResource(self)
        self.account_products = resources.AsyncAccountProductsResource(self)
        self.transaction_requests = resources.AsyncTransactionRequestsResource(self)
        self.bank_accounts = resources.AsyncBankAccountsResource(self)
        self.consents = resources.AsyncConsentsResource(self)
        self.crm_events = resources.AsyncCRMEventsResource(self)
        self.currencies = resources.AsyncCurrenciesResource(self)
        self.customers = resources.AsyncCustomersResource(self)
        self.product_collections = resources.AsyncProductCollectionsResource(self)
        self.product_tree = resources.AsyncProductTreeResource(self)
        self.products = resources.AsyncProductsResource(self)
        self.public_accounts = resources.AsyncPublicAccountsResource(self)
        self.user_invitations = resources.AsyncUserInvitationsResource(self)
        self.user_customer_links = resources.AsyncUserCustomerLinksResource(self)
        self.users = resources.AsyncUsersResource(self)
        self.views = resources.AsyncViewsResource(self)
        self.web_hooks = resources.AsyncWebHooksResource(self)
        self.cards = resources.AsyncCardsResource(self)
        self.certs = resources.AsyncCertsResource(self)
        self.config = resources.AsyncConfigResource(self)
        self.connector = resources.AsyncConnectorResource(self)
        self.consumer = resources.AsyncConsumerResource(self)
        self.consent_requests = resources.AsyncConsentRequestsResource(self)
        self.consumers = resources.AsyncConsumersResource(self)
        self.customers_minimal = resources.AsyncCustomersMinimalResource(self)
        self.database = resources.AsyncDatabaseResource(self)
        self.development = resources.AsyncDevelopmentResource(self)
        self.dynamic_registration = resources.AsyncDynamicRegistrationResource(self)
        self.endpoints = resources.AsyncEndpointsResource(self)
        self.entitlement_requests = resources.AsyncEntitlementRequestsResource(self)
        self.entitlements = resources.AsyncEntitlementsResource(self)
        self.jwks_uris = resources.AsyncJwksUrisResource(self)
        self.management = resources.AsyncManagementResource(self)
        self.authentication_type_validations = resources.AsyncAuthenticationTypeValidationsResource(self)
        self.standing_orders = resources.AsyncStandingOrdersResource(self)
        self.dynamic_endpoints = resources.AsyncDynamicEndpointsResource(self)
        self.dynamic_message_docs = resources.AsyncDynamicMessageDocsResource(self)
        self.dynamic_resource_docs = resources.AsyncDynamicResourceDocsResource(self)
        self.endpoint_mappings = resources.AsyncEndpointMappingsResource(self)
        self.fast_firehose_accounts = resources.AsyncFastFirehoseAccountsResource(self)
        self.cascading_banks = resources.AsyncCascadingBanksResource(self)
        self.connector_methods = resources.AsyncConnectorMethodsResource(self)
        self.json_schema_validations = resources.AsyncJsonSchemaValidationsResource(self)
        self.method_routings = resources.AsyncMethodRoutingsResource(self)
        self.metrics = resources.AsyncMetricsResource(self)
        self.system_dynamic_entities = resources.AsyncSystemDynamicEntitiesResource(self)
        self.system_integrity = resources.AsyncSystemIntegrityResource(self)
        self.webui_props = resources.AsyncWebuiPropsResource(self)
        self.documentation = resources.AsyncDocumentationResource(self)
        self.consent = resources.AsyncConsentResource(self)
        self.correlated_entities = resources.AsyncCorrelatedEntitiesResource(self)
        self.dynamic_entities = resources.AsyncDynamicEntitiesResource(self)
        self.mtls = resources.AsyncMtlsResource(self)
        self.spaces = resources.AsyncSpacesResource(self)
        self.user = resources.AsyncUserResource(self)
        self.rate_limits = resources.AsyncRateLimitsResource(self)
        self.regulated_entities = resources.AsyncRegulatedEntitiesResource(self)
        self.resource_docs = resources.AsyncResourceDocsResource(self)
        self.roles = resources.AsyncRolesResource(self)
        self.sandbox = resources.AsyncSandboxResource(self)
        self.search = resources.AsyncSearchResource(self)
        self.system_views = resources.AsyncSystemViewsResource(self)
        self.user_entitlements = resources.AsyncUserEntitlementsResource(self)
        self.with_raw_response = AsyncObpAPIWithRawResponse(self)
        self.with_streaming_response = AsyncObpAPIWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        environment: Literal["production", "environment_1"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class ObpAPIWithRawResponse:
    def __init__(self, client: ObpAPI) -> None:
        self.accounts = resources.AccountsResourceWithRawResponse(client.accounts)
        self.adapter = resources.AdapterResourceWithRawResponse(client.adapter)
        self.api_collections = resources.APICollectionsResourceWithRawResponse(client.api_collections)
        self.api = resources.APIResourceWithRawResponse(client.api)
        self.banks = resources.BanksResourceWithRawResponse(client.banks)
        self.accounts_held = resources.AccountsHeldResourceWithRawResponse(client.accounts_held)
        self.counterparties = resources.CounterpartiesResourceWithRawResponse(client.counterparties)
        self.transactions = resources.TransactionsResourceWithRawResponse(client.transactions)
        self.customer_account_links = resources.CustomerAccountLinksResourceWithRawResponse(
            client.customer_account_links
        )
        self.permissions = resources.PermissionsResourceWithRawResponse(client.permissions)
        self.account_products = resources.AccountProductsResourceWithRawResponse(client.account_products)
        self.transaction_requests = resources.TransactionRequestsResourceWithRawResponse(client.transaction_requests)
        self.bank_accounts = resources.BankAccountsResourceWithRawResponse(client.bank_accounts)
        self.consents = resources.ConsentsResourceWithRawResponse(client.consents)
        self.crm_events = resources.CRMEventsResourceWithRawResponse(client.crm_events)
        self.currencies = resources.CurrenciesResourceWithRawResponse(client.currencies)
        self.customers = resources.CustomersResourceWithRawResponse(client.customers)
        self.product_collections = resources.ProductCollectionsResourceWithRawResponse(client.product_collections)
        self.product_tree = resources.ProductTreeResourceWithRawResponse(client.product_tree)
        self.products = resources.ProductsResourceWithRawResponse(client.products)
        self.public_accounts = resources.PublicAccountsResourceWithRawResponse(client.public_accounts)
        self.user_invitations = resources.UserInvitationsResourceWithRawResponse(client.user_invitations)
        self.user_customer_links = resources.UserCustomerLinksResourceWithRawResponse(client.user_customer_links)
        self.users = resources.UsersResourceWithRawResponse(client.users)
        self.views = resources.ViewsResourceWithRawResponse(client.views)
        self.web_hooks = resources.WebHooksResourceWithRawResponse(client.web_hooks)
        self.cards = resources.CardsResourceWithRawResponse(client.cards)
        self.certs = resources.CertsResourceWithRawResponse(client.certs)
        self.config = resources.ConfigResourceWithRawResponse(client.config)
        self.connector = resources.ConnectorResourceWithRawResponse(client.connector)
        self.consumer = resources.ConsumerResourceWithRawResponse(client.consumer)
        self.consent_requests = resources.ConsentRequestsResourceWithRawResponse(client.consent_requests)
        self.consumers = resources.ConsumersResourceWithRawResponse(client.consumers)
        self.customers_minimal = resources.CustomersMinimalResourceWithRawResponse(client.customers_minimal)
        self.database = resources.DatabaseResourceWithRawResponse(client.database)
        self.development = resources.DevelopmentResourceWithRawResponse(client.development)
        self.dynamic_registration = resources.DynamicRegistrationResourceWithRawResponse(client.dynamic_registration)
        self.endpoints = resources.EndpointsResourceWithRawResponse(client.endpoints)
        self.entitlement_requests = resources.EntitlementRequestsResourceWithRawResponse(client.entitlement_requests)
        self.entitlements = resources.EntitlementsResourceWithRawResponse(client.entitlements)
        self.jwks_uris = resources.JwksUrisResourceWithRawResponse(client.jwks_uris)
        self.management = resources.ManagementResourceWithRawResponse(client.management)
        self.authentication_type_validations = resources.AuthenticationTypeValidationsResourceWithRawResponse(
            client.authentication_type_validations
        )
        self.standing_orders = resources.StandingOrdersResourceWithRawResponse(client.standing_orders)
        self.dynamic_endpoints = resources.DynamicEndpointsResourceWithRawResponse(client.dynamic_endpoints)
        self.dynamic_message_docs = resources.DynamicMessageDocsResourceWithRawResponse(client.dynamic_message_docs)
        self.dynamic_resource_docs = resources.DynamicResourceDocsResourceWithRawResponse(client.dynamic_resource_docs)
        self.endpoint_mappings = resources.EndpointMappingsResourceWithRawResponse(client.endpoint_mappings)
        self.fast_firehose_accounts = resources.FastFirehoseAccountsResourceWithRawResponse(
            client.fast_firehose_accounts
        )
        self.cascading_banks = resources.CascadingBanksResourceWithRawResponse(client.cascading_banks)
        self.connector_methods = resources.ConnectorMethodsResourceWithRawResponse(client.connector_methods)
        self.json_schema_validations = resources.JsonSchemaValidationsResourceWithRawResponse(
            client.json_schema_validations
        )
        self.method_routings = resources.MethodRoutingsResourceWithRawResponse(client.method_routings)
        self.metrics = resources.MetricsResourceWithRawResponse(client.metrics)
        self.system_dynamic_entities = resources.SystemDynamicEntitiesResourceWithRawResponse(
            client.system_dynamic_entities
        )
        self.system_integrity = resources.SystemIntegrityResourceWithRawResponse(client.system_integrity)
        self.webui_props = resources.WebuiPropsResourceWithRawResponse(client.webui_props)
        self.documentation = resources.DocumentationResourceWithRawResponse(client.documentation)
        self.consent = resources.ConsentResourceWithRawResponse(client.consent)
        self.correlated_entities = resources.CorrelatedEntitiesResourceWithRawResponse(client.correlated_entities)
        self.dynamic_entities = resources.DynamicEntitiesResourceWithRawResponse(client.dynamic_entities)
        self.mtls = resources.MtlsResourceWithRawResponse(client.mtls)
        self.spaces = resources.SpacesResourceWithRawResponse(client.spaces)
        self.user = resources.UserResourceWithRawResponse(client.user)
        self.rate_limits = resources.RateLimitsResourceWithRawResponse(client.rate_limits)
        self.regulated_entities = resources.RegulatedEntitiesResourceWithRawResponse(client.regulated_entities)
        self.resource_docs = resources.ResourceDocsResourceWithRawResponse(client.resource_docs)
        self.roles = resources.RolesResourceWithRawResponse(client.roles)
        self.sandbox = resources.SandboxResourceWithRawResponse(client.sandbox)
        self.search = resources.SearchResourceWithRawResponse(client.search)
        self.system_views = resources.SystemViewsResourceWithRawResponse(client.system_views)
        self.user_entitlements = resources.UserEntitlementsResourceWithRawResponse(client.user_entitlements)


class AsyncObpAPIWithRawResponse:
    def __init__(self, client: AsyncObpAPI) -> None:
        self.accounts = resources.AsyncAccountsResourceWithRawResponse(client.accounts)
        self.adapter = resources.AsyncAdapterResourceWithRawResponse(client.adapter)
        self.api_collections = resources.AsyncAPICollectionsResourceWithRawResponse(client.api_collections)
        self.api = resources.AsyncAPIResourceWithRawResponse(client.api)
        self.banks = resources.AsyncBanksResourceWithRawResponse(client.banks)
        self.accounts_held = resources.AsyncAccountsHeldResourceWithRawResponse(client.accounts_held)
        self.counterparties = resources.AsyncCounterpartiesResourceWithRawResponse(client.counterparties)
        self.transactions = resources.AsyncTransactionsResourceWithRawResponse(client.transactions)
        self.customer_account_links = resources.AsyncCustomerAccountLinksResourceWithRawResponse(
            client.customer_account_links
        )
        self.permissions = resources.AsyncPermissionsResourceWithRawResponse(client.permissions)
        self.account_products = resources.AsyncAccountProductsResourceWithRawResponse(client.account_products)
        self.transaction_requests = resources.AsyncTransactionRequestsResourceWithRawResponse(
            client.transaction_requests
        )
        self.bank_accounts = resources.AsyncBankAccountsResourceWithRawResponse(client.bank_accounts)
        self.consents = resources.AsyncConsentsResourceWithRawResponse(client.consents)
        self.crm_events = resources.AsyncCRMEventsResourceWithRawResponse(client.crm_events)
        self.currencies = resources.AsyncCurrenciesResourceWithRawResponse(client.currencies)
        self.customers = resources.AsyncCustomersResourceWithRawResponse(client.customers)
        self.product_collections = resources.AsyncProductCollectionsResourceWithRawResponse(client.product_collections)
        self.product_tree = resources.AsyncProductTreeResourceWithRawResponse(client.product_tree)
        self.products = resources.AsyncProductsResourceWithRawResponse(client.products)
        self.public_accounts = resources.AsyncPublicAccountsResourceWithRawResponse(client.public_accounts)
        self.user_invitations = resources.AsyncUserInvitationsResourceWithRawResponse(client.user_invitations)
        self.user_customer_links = resources.AsyncUserCustomerLinksResourceWithRawResponse(client.user_customer_links)
        self.users = resources.AsyncUsersResourceWithRawResponse(client.users)
        self.views = resources.AsyncViewsResourceWithRawResponse(client.views)
        self.web_hooks = resources.AsyncWebHooksResourceWithRawResponse(client.web_hooks)
        self.cards = resources.AsyncCardsResourceWithRawResponse(client.cards)
        self.certs = resources.AsyncCertsResourceWithRawResponse(client.certs)
        self.config = resources.AsyncConfigResourceWithRawResponse(client.config)
        self.connector = resources.AsyncConnectorResourceWithRawResponse(client.connector)
        self.consumer = resources.AsyncConsumerResourceWithRawResponse(client.consumer)
        self.consent_requests = resources.AsyncConsentRequestsResourceWithRawResponse(client.consent_requests)
        self.consumers = resources.AsyncConsumersResourceWithRawResponse(client.consumers)
        self.customers_minimal = resources.AsyncCustomersMinimalResourceWithRawResponse(client.customers_minimal)
        self.database = resources.AsyncDatabaseResourceWithRawResponse(client.database)
        self.development = resources.AsyncDevelopmentResourceWithRawResponse(client.development)
        self.dynamic_registration = resources.AsyncDynamicRegistrationResourceWithRawResponse(
            client.dynamic_registration
        )
        self.endpoints = resources.AsyncEndpointsResourceWithRawResponse(client.endpoints)
        self.entitlement_requests = resources.AsyncEntitlementRequestsResourceWithRawResponse(
            client.entitlement_requests
        )
        self.entitlements = resources.AsyncEntitlementsResourceWithRawResponse(client.entitlements)
        self.jwks_uris = resources.AsyncJwksUrisResourceWithRawResponse(client.jwks_uris)
        self.management = resources.AsyncManagementResourceWithRawResponse(client.management)
        self.authentication_type_validations = resources.AsyncAuthenticationTypeValidationsResourceWithRawResponse(
            client.authentication_type_validations
        )
        self.standing_orders = resources.AsyncStandingOrdersResourceWithRawResponse(client.standing_orders)
        self.dynamic_endpoints = resources.AsyncDynamicEndpointsResourceWithRawResponse(client.dynamic_endpoints)
        self.dynamic_message_docs = resources.AsyncDynamicMessageDocsResourceWithRawResponse(
            client.dynamic_message_docs
        )
        self.dynamic_resource_docs = resources.AsyncDynamicResourceDocsResourceWithRawResponse(
            client.dynamic_resource_docs
        )
        self.endpoint_mappings = resources.AsyncEndpointMappingsResourceWithRawResponse(client.endpoint_mappings)
        self.fast_firehose_accounts = resources.AsyncFastFirehoseAccountsResourceWithRawResponse(
            client.fast_firehose_accounts
        )
        self.cascading_banks = resources.AsyncCascadingBanksResourceWithRawResponse(client.cascading_banks)
        self.connector_methods = resources.AsyncConnectorMethodsResourceWithRawResponse(client.connector_methods)
        self.json_schema_validations = resources.AsyncJsonSchemaValidationsResourceWithRawResponse(
            client.json_schema_validations
        )
        self.method_routings = resources.AsyncMethodRoutingsResourceWithRawResponse(client.method_routings)
        self.metrics = resources.AsyncMetricsResourceWithRawResponse(client.metrics)
        self.system_dynamic_entities = resources.AsyncSystemDynamicEntitiesResourceWithRawResponse(
            client.system_dynamic_entities
        )
        self.system_integrity = resources.AsyncSystemIntegrityResourceWithRawResponse(client.system_integrity)
        self.webui_props = resources.AsyncWebuiPropsResourceWithRawResponse(client.webui_props)
        self.documentation = resources.AsyncDocumentationResourceWithRawResponse(client.documentation)
        self.consent = resources.AsyncConsentResourceWithRawResponse(client.consent)
        self.correlated_entities = resources.AsyncCorrelatedEntitiesResourceWithRawResponse(client.correlated_entities)
        self.dynamic_entities = resources.AsyncDynamicEntitiesResourceWithRawResponse(client.dynamic_entities)
        self.mtls = resources.AsyncMtlsResourceWithRawResponse(client.mtls)
        self.spaces = resources.AsyncSpacesResourceWithRawResponse(client.spaces)
        self.user = resources.AsyncUserResourceWithRawResponse(client.user)
        self.rate_limits = resources.AsyncRateLimitsResourceWithRawResponse(client.rate_limits)
        self.regulated_entities = resources.AsyncRegulatedEntitiesResourceWithRawResponse(client.regulated_entities)
        self.resource_docs = resources.AsyncResourceDocsResourceWithRawResponse(client.resource_docs)
        self.roles = resources.AsyncRolesResourceWithRawResponse(client.roles)
        self.sandbox = resources.AsyncSandboxResourceWithRawResponse(client.sandbox)
        self.search = resources.AsyncSearchResourceWithRawResponse(client.search)
        self.system_views = resources.AsyncSystemViewsResourceWithRawResponse(client.system_views)
        self.user_entitlements = resources.AsyncUserEntitlementsResourceWithRawResponse(client.user_entitlements)


class ObpAPIWithStreamedResponse:
    def __init__(self, client: ObpAPI) -> None:
        self.accounts = resources.AccountsResourceWithStreamingResponse(client.accounts)
        self.adapter = resources.AdapterResourceWithStreamingResponse(client.adapter)
        self.api_collections = resources.APICollectionsResourceWithStreamingResponse(client.api_collections)
        self.api = resources.APIResourceWithStreamingResponse(client.api)
        self.banks = resources.BanksResourceWithStreamingResponse(client.banks)
        self.accounts_held = resources.AccountsHeldResourceWithStreamingResponse(client.accounts_held)
        self.counterparties = resources.CounterpartiesResourceWithStreamingResponse(client.counterparties)
        self.transactions = resources.TransactionsResourceWithStreamingResponse(client.transactions)
        self.customer_account_links = resources.CustomerAccountLinksResourceWithStreamingResponse(
            client.customer_account_links
        )
        self.permissions = resources.PermissionsResourceWithStreamingResponse(client.permissions)
        self.account_products = resources.AccountProductsResourceWithStreamingResponse(client.account_products)
        self.transaction_requests = resources.TransactionRequestsResourceWithStreamingResponse(
            client.transaction_requests
        )
        self.bank_accounts = resources.BankAccountsResourceWithStreamingResponse(client.bank_accounts)
        self.consents = resources.ConsentsResourceWithStreamingResponse(client.consents)
        self.crm_events = resources.CRMEventsResourceWithStreamingResponse(client.crm_events)
        self.currencies = resources.CurrenciesResourceWithStreamingResponse(client.currencies)
        self.customers = resources.CustomersResourceWithStreamingResponse(client.customers)
        self.product_collections = resources.ProductCollectionsResourceWithStreamingResponse(client.product_collections)
        self.product_tree = resources.ProductTreeResourceWithStreamingResponse(client.product_tree)
        self.products = resources.ProductsResourceWithStreamingResponse(client.products)
        self.public_accounts = resources.PublicAccountsResourceWithStreamingResponse(client.public_accounts)
        self.user_invitations = resources.UserInvitationsResourceWithStreamingResponse(client.user_invitations)
        self.user_customer_links = resources.UserCustomerLinksResourceWithStreamingResponse(client.user_customer_links)
        self.users = resources.UsersResourceWithStreamingResponse(client.users)
        self.views = resources.ViewsResourceWithStreamingResponse(client.views)
        self.web_hooks = resources.WebHooksResourceWithStreamingResponse(client.web_hooks)
        self.cards = resources.CardsResourceWithStreamingResponse(client.cards)
        self.certs = resources.CertsResourceWithStreamingResponse(client.certs)
        self.config = resources.ConfigResourceWithStreamingResponse(client.config)
        self.connector = resources.ConnectorResourceWithStreamingResponse(client.connector)
        self.consumer = resources.ConsumerResourceWithStreamingResponse(client.consumer)
        self.consent_requests = resources.ConsentRequestsResourceWithStreamingResponse(client.consent_requests)
        self.consumers = resources.ConsumersResourceWithStreamingResponse(client.consumers)
        self.customers_minimal = resources.CustomersMinimalResourceWithStreamingResponse(client.customers_minimal)
        self.database = resources.DatabaseResourceWithStreamingResponse(client.database)
        self.development = resources.DevelopmentResourceWithStreamingResponse(client.development)
        self.dynamic_registration = resources.DynamicRegistrationResourceWithStreamingResponse(
            client.dynamic_registration
        )
        self.endpoints = resources.EndpointsResourceWithStreamingResponse(client.endpoints)
        self.entitlement_requests = resources.EntitlementRequestsResourceWithStreamingResponse(
            client.entitlement_requests
        )
        self.entitlements = resources.EntitlementsResourceWithStreamingResponse(client.entitlements)
        self.jwks_uris = resources.JwksUrisResourceWithStreamingResponse(client.jwks_uris)
        self.management = resources.ManagementResourceWithStreamingResponse(client.management)
        self.authentication_type_validations = resources.AuthenticationTypeValidationsResourceWithStreamingResponse(
            client.authentication_type_validations
        )
        self.standing_orders = resources.StandingOrdersResourceWithStreamingResponse(client.standing_orders)
        self.dynamic_endpoints = resources.DynamicEndpointsResourceWithStreamingResponse(client.dynamic_endpoints)
        self.dynamic_message_docs = resources.DynamicMessageDocsResourceWithStreamingResponse(
            client.dynamic_message_docs
        )
        self.dynamic_resource_docs = resources.DynamicResourceDocsResourceWithStreamingResponse(
            client.dynamic_resource_docs
        )
        self.endpoint_mappings = resources.EndpointMappingsResourceWithStreamingResponse(client.endpoint_mappings)
        self.fast_firehose_accounts = resources.FastFirehoseAccountsResourceWithStreamingResponse(
            client.fast_firehose_accounts
        )
        self.cascading_banks = resources.CascadingBanksResourceWithStreamingResponse(client.cascading_banks)
        self.connector_methods = resources.ConnectorMethodsResourceWithStreamingResponse(client.connector_methods)
        self.json_schema_validations = resources.JsonSchemaValidationsResourceWithStreamingResponse(
            client.json_schema_validations
        )
        self.method_routings = resources.MethodRoutingsResourceWithStreamingResponse(client.method_routings)
        self.metrics = resources.MetricsResourceWithStreamingResponse(client.metrics)
        self.system_dynamic_entities = resources.SystemDynamicEntitiesResourceWithStreamingResponse(
            client.system_dynamic_entities
        )
        self.system_integrity = resources.SystemIntegrityResourceWithStreamingResponse(client.system_integrity)
        self.webui_props = resources.WebuiPropsResourceWithStreamingResponse(client.webui_props)
        self.documentation = resources.DocumentationResourceWithStreamingResponse(client.documentation)
        self.consent = resources.ConsentResourceWithStreamingResponse(client.consent)
        self.correlated_entities = resources.CorrelatedEntitiesResourceWithStreamingResponse(client.correlated_entities)
        self.dynamic_entities = resources.DynamicEntitiesResourceWithStreamingResponse(client.dynamic_entities)
        self.mtls = resources.MtlsResourceWithStreamingResponse(client.mtls)
        self.spaces = resources.SpacesResourceWithStreamingResponse(client.spaces)
        self.user = resources.UserResourceWithStreamingResponse(client.user)
        self.rate_limits = resources.RateLimitsResourceWithStreamingResponse(client.rate_limits)
        self.regulated_entities = resources.RegulatedEntitiesResourceWithStreamingResponse(client.regulated_entities)
        self.resource_docs = resources.ResourceDocsResourceWithStreamingResponse(client.resource_docs)
        self.roles = resources.RolesResourceWithStreamingResponse(client.roles)
        self.sandbox = resources.SandboxResourceWithStreamingResponse(client.sandbox)
        self.search = resources.SearchResourceWithStreamingResponse(client.search)
        self.system_views = resources.SystemViewsResourceWithStreamingResponse(client.system_views)
        self.user_entitlements = resources.UserEntitlementsResourceWithStreamingResponse(client.user_entitlements)


class AsyncObpAPIWithStreamedResponse:
    def __init__(self, client: AsyncObpAPI) -> None:
        self.accounts = resources.AsyncAccountsResourceWithStreamingResponse(client.accounts)
        self.adapter = resources.AsyncAdapterResourceWithStreamingResponse(client.adapter)
        self.api_collections = resources.AsyncAPICollectionsResourceWithStreamingResponse(client.api_collections)
        self.api = resources.AsyncAPIResourceWithStreamingResponse(client.api)
        self.banks = resources.AsyncBanksResourceWithStreamingResponse(client.banks)
        self.accounts_held = resources.AsyncAccountsHeldResourceWithStreamingResponse(client.accounts_held)
        self.counterparties = resources.AsyncCounterpartiesResourceWithStreamingResponse(client.counterparties)
        self.transactions = resources.AsyncTransactionsResourceWithStreamingResponse(client.transactions)
        self.customer_account_links = resources.AsyncCustomerAccountLinksResourceWithStreamingResponse(
            client.customer_account_links
        )
        self.permissions = resources.AsyncPermissionsResourceWithStreamingResponse(client.permissions)
        self.account_products = resources.AsyncAccountProductsResourceWithStreamingResponse(client.account_products)
        self.transaction_requests = resources.AsyncTransactionRequestsResourceWithStreamingResponse(
            client.transaction_requests
        )
        self.bank_accounts = resources.AsyncBankAccountsResourceWithStreamingResponse(client.bank_accounts)
        self.consents = resources.AsyncConsentsResourceWithStreamingResponse(client.consents)
        self.crm_events = resources.AsyncCRMEventsResourceWithStreamingResponse(client.crm_events)
        self.currencies = resources.AsyncCurrenciesResourceWithStreamingResponse(client.currencies)
        self.customers = resources.AsyncCustomersResourceWithStreamingResponse(client.customers)
        self.product_collections = resources.AsyncProductCollectionsResourceWithStreamingResponse(
            client.product_collections
        )
        self.product_tree = resources.AsyncProductTreeResourceWithStreamingResponse(client.product_tree)
        self.products = resources.AsyncProductsResourceWithStreamingResponse(client.products)
        self.public_accounts = resources.AsyncPublicAccountsResourceWithStreamingResponse(client.public_accounts)
        self.user_invitations = resources.AsyncUserInvitationsResourceWithStreamingResponse(client.user_invitations)
        self.user_customer_links = resources.AsyncUserCustomerLinksResourceWithStreamingResponse(
            client.user_customer_links
        )
        self.users = resources.AsyncUsersResourceWithStreamingResponse(client.users)
        self.views = resources.AsyncViewsResourceWithStreamingResponse(client.views)
        self.web_hooks = resources.AsyncWebHooksResourceWithStreamingResponse(client.web_hooks)
        self.cards = resources.AsyncCardsResourceWithStreamingResponse(client.cards)
        self.certs = resources.AsyncCertsResourceWithStreamingResponse(client.certs)
        self.config = resources.AsyncConfigResourceWithStreamingResponse(client.config)
        self.connector = resources.AsyncConnectorResourceWithStreamingResponse(client.connector)
        self.consumer = resources.AsyncConsumerResourceWithStreamingResponse(client.consumer)
        self.consent_requests = resources.AsyncConsentRequestsResourceWithStreamingResponse(client.consent_requests)
        self.consumers = resources.AsyncConsumersResourceWithStreamingResponse(client.consumers)
        self.customers_minimal = resources.AsyncCustomersMinimalResourceWithStreamingResponse(client.customers_minimal)
        self.database = resources.AsyncDatabaseResourceWithStreamingResponse(client.database)
        self.development = resources.AsyncDevelopmentResourceWithStreamingResponse(client.development)
        self.dynamic_registration = resources.AsyncDynamicRegistrationResourceWithStreamingResponse(
            client.dynamic_registration
        )
        self.endpoints = resources.AsyncEndpointsResourceWithStreamingResponse(client.endpoints)
        self.entitlement_requests = resources.AsyncEntitlementRequestsResourceWithStreamingResponse(
            client.entitlement_requests
        )
        self.entitlements = resources.AsyncEntitlementsResourceWithStreamingResponse(client.entitlements)
        self.jwks_uris = resources.AsyncJwksUrisResourceWithStreamingResponse(client.jwks_uris)
        self.management = resources.AsyncManagementResourceWithStreamingResponse(client.management)
        self.authentication_type_validations = (
            resources.AsyncAuthenticationTypeValidationsResourceWithStreamingResponse(
                client.authentication_type_validations
            )
        )
        self.standing_orders = resources.AsyncStandingOrdersResourceWithStreamingResponse(client.standing_orders)
        self.dynamic_endpoints = resources.AsyncDynamicEndpointsResourceWithStreamingResponse(client.dynamic_endpoints)
        self.dynamic_message_docs = resources.AsyncDynamicMessageDocsResourceWithStreamingResponse(
            client.dynamic_message_docs
        )
        self.dynamic_resource_docs = resources.AsyncDynamicResourceDocsResourceWithStreamingResponse(
            client.dynamic_resource_docs
        )
        self.endpoint_mappings = resources.AsyncEndpointMappingsResourceWithStreamingResponse(client.endpoint_mappings)
        self.fast_firehose_accounts = resources.AsyncFastFirehoseAccountsResourceWithStreamingResponse(
            client.fast_firehose_accounts
        )
        self.cascading_banks = resources.AsyncCascadingBanksResourceWithStreamingResponse(client.cascading_banks)
        self.connector_methods = resources.AsyncConnectorMethodsResourceWithStreamingResponse(client.connector_methods)
        self.json_schema_validations = resources.AsyncJsonSchemaValidationsResourceWithStreamingResponse(
            client.json_schema_validations
        )
        self.method_routings = resources.AsyncMethodRoutingsResourceWithStreamingResponse(client.method_routings)
        self.metrics = resources.AsyncMetricsResourceWithStreamingResponse(client.metrics)
        self.system_dynamic_entities = resources.AsyncSystemDynamicEntitiesResourceWithStreamingResponse(
            client.system_dynamic_entities
        )
        self.system_integrity = resources.AsyncSystemIntegrityResourceWithStreamingResponse(client.system_integrity)
        self.webui_props = resources.AsyncWebuiPropsResourceWithStreamingResponse(client.webui_props)
        self.documentation = resources.AsyncDocumentationResourceWithStreamingResponse(client.documentation)
        self.consent = resources.AsyncConsentResourceWithStreamingResponse(client.consent)
        self.correlated_entities = resources.AsyncCorrelatedEntitiesResourceWithStreamingResponse(
            client.correlated_entities
        )
        self.dynamic_entities = resources.AsyncDynamicEntitiesResourceWithStreamingResponse(client.dynamic_entities)
        self.mtls = resources.AsyncMtlsResourceWithStreamingResponse(client.mtls)
        self.spaces = resources.AsyncSpacesResourceWithStreamingResponse(client.spaces)
        self.user = resources.AsyncUserResourceWithStreamingResponse(client.user)
        self.rate_limits = resources.AsyncRateLimitsResourceWithStreamingResponse(client.rate_limits)
        self.regulated_entities = resources.AsyncRegulatedEntitiesResourceWithStreamingResponse(
            client.regulated_entities
        )
        self.resource_docs = resources.AsyncResourceDocsResourceWithStreamingResponse(client.resource_docs)
        self.roles = resources.AsyncRolesResourceWithStreamingResponse(client.roles)
        self.sandbox = resources.AsyncSandboxResourceWithStreamingResponse(client.sandbox)
        self.search = resources.AsyncSearchResourceWithStreamingResponse(client.search)
        self.system_views = resources.AsyncSystemViewsResourceWithStreamingResponse(client.system_views)
        self.user_entitlements = resources.AsyncUserEntitlementsResourceWithStreamingResponse(client.user_entitlements)


Client = ObpAPI

AsyncClient = AsyncObpAPI
