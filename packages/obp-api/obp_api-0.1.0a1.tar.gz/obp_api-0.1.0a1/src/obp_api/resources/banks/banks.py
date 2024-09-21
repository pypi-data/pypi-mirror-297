# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .fx import (
    FxResource,
    AsyncFxResource,
    FxResourceWithRawResponse,
    AsyncFxResourceWithRawResponse,
    FxResourceWithStreamingResponse,
    AsyncFxResourceWithStreamingResponse,
)
from .atms import (
    AtmsResource,
    AsyncAtmsResource,
    AtmsResourceWithRawResponse,
    AsyncAtmsResourceWithRawResponse,
    AtmsResourceWithStreamingResponse,
    AsyncAtmsResourceWithStreamingResponse,
)
from ...types import bank_create_params, bank_update_params
from .adapter import (
    AdapterResource,
    AsyncAdapterResource,
    AdapterResourceWithRawResponse,
    AsyncAdapterResourceWithRawResponse,
    AdapterResourceWithStreamingResponse,
    AsyncAdapterResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .accounts import (
    AccountsResource,
    AsyncAccountsResource,
    AccountsResourceWithRawResponse,
    AsyncAccountsResourceWithRawResponse,
    AccountsResourceWithStreamingResponse,
    AsyncAccountsResourceWithStreamingResponse,
)
from .balances import (
    BalancesResource,
    AsyncBalancesResource,
    BalancesResourceWithRawResponse,
    AsyncBalancesResourceWithRawResponse,
    BalancesResourceWithStreamingResponse,
    AsyncBalancesResourceWithStreamingResponse,
)
from .branches import (
    BranchesResource,
    AsyncBranchesResource,
    BranchesResourceWithRawResponse,
    AsyncBranchesResourceWithRawResponse,
    BranchesResourceWithStreamingResponse,
    AsyncBranchesResourceWithStreamingResponse,
)
from .consents import (
    ConsentsResource,
    AsyncConsentsResource,
    ConsentsResourceWithRawResponse,
    AsyncConsentsResourceWithRawResponse,
    ConsentsResourceWithStreamingResponse,
    AsyncConsentsResourceWithStreamingResponse,
)
from .meetings import (
    MeetingsResource,
    AsyncMeetingsResource,
    MeetingsResourceWithRawResponse,
    AsyncMeetingsResourceWithRawResponse,
    MeetingsResourceWithStreamingResponse,
    AsyncMeetingsResourceWithStreamingResponse,
)
from .webhooks import (
    WebhooksResource,
    AsyncWebhooksResource,
    WebhooksResourceWithRawResponse,
    AsyncWebhooksResourceWithRawResponse,
    WebhooksResourceWithStreamingResponse,
    AsyncWebhooksResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .atms.atms import AtmsResource, AsyncAtmsResource
from .customers import (
    CustomersResource,
    AsyncCustomersResource,
    CustomersResourceWithRawResponse,
    AsyncCustomersResourceWithRawResponse,
    CustomersResourceWithStreamingResponse,
    AsyncCustomersResourceWithStreamingResponse,
)
from .attributes import (
    AttributesResource,
    AsyncAttributesResource,
    AttributesResourceWithRawResponse,
    AsyncAttributesResourceWithRawResponse,
    AttributesResourceWithStreamingResponse,
    AsyncAttributesResourceWithStreamingResponse,
)
from .management import (
    ManagementResource,
    AsyncManagementResource,
    ManagementResourceWithRawResponse,
    AsyncManagementResourceWithRawResponse,
    ManagementResourceWithStreamingResponse,
    AsyncManagementResourceWithStreamingResponse,
)
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
from .my_consents import (
    MyConsentsResource,
    AsyncMyConsentsResource,
    MyConsentsResourceWithRawResponse,
    AsyncMyConsentsResourceWithRawResponse,
    MyConsentsResourceWithStreamingResponse,
    AsyncMyConsentsResourceWithStreamingResponse,
)
from .entitlements import (
    EntitlementsResource,
    AsyncEntitlementsResource,
    EntitlementsResourceWithRawResponse,
    AsyncEntitlementsResourceWithRawResponse,
    EntitlementsResourceWithStreamingResponse,
    AsyncEntitlementsResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from .dynamic_entities import (
    DynamicEntitiesResource,
    AsyncDynamicEntitiesResource,
    DynamicEntitiesResourceWithRawResponse,
    AsyncDynamicEntitiesResourceWithRawResponse,
    DynamicEntitiesResourceWithStreamingResponse,
    AsyncDynamicEntitiesResourceWithStreamingResponse,
)
from .my_consent_infos import (
    MyConsentInfosResource,
    AsyncMyConsentInfosResource,
    MyConsentInfosResourceWithRawResponse,
    AsyncMyConsentInfosResourceWithRawResponse,
    MyConsentInfosResourceWithStreamingResponse,
    AsyncMyConsentInfosResourceWithStreamingResponse,
)
from .account_web_hooks import (
    AccountWebHooksResource,
    AsyncAccountWebHooksResource,
    AccountWebHooksResourceWithRawResponse,
    AsyncAccountWebHooksResourceWithRawResponse,
    AccountWebHooksResourceWithStreamingResponse,
    AsyncAccountWebHooksResourceWithStreamingResponse,
)
from .accounts.accounts import AccountsResource, AsyncAccountsResource
from .dynamic_endpoints import (
    DynamicEndpointsResource,
    AsyncDynamicEndpointsResource,
    DynamicEndpointsResourceWithRawResponse,
    AsyncDynamicEndpointsResourceWithRawResponse,
    DynamicEndpointsResourceWithStreamingResponse,
    AsyncDynamicEndpointsResourceWithStreamingResponse,
)
from .firehose_customers import (
    FirehoseCustomersResource,
    AsyncFirehoseCustomersResource,
    FirehoseCustomersResourceWithRawResponse,
    AsyncFirehoseCustomersResourceWithRawResponse,
    FirehoseCustomersResourceWithStreamingResponse,
    AsyncFirehoseCustomersResourceWithStreamingResponse,
)
from .customers.customers import CustomersResource, AsyncCustomersResource
from .account_applications import (
    AccountApplicationsResource,
    AsyncAccountApplicationsResource,
    AccountApplicationsResourceWithRawResponse,
    AsyncAccountApplicationsResourceWithRawResponse,
    AccountApplicationsResourceWithStreamingResponse,
    AsyncAccountApplicationsResourceWithStreamingResponse,
)
from .dynamic_message_docs import (
    DynamicMessageDocsResource,
    AsyncDynamicMessageDocsResource,
    DynamicMessageDocsResourceWithRawResponse,
    AsyncDynamicMessageDocsResourceWithRawResponse,
    DynamicMessageDocsResourceWithStreamingResponse,
    AsyncDynamicMessageDocsResourceWithStreamingResponse,
)
from .attribute_definitions import (
    AttributeDefinitionsResource,
    AsyncAttributeDefinitionsResource,
    AttributeDefinitionsResourceWithRawResponse,
    AsyncAttributeDefinitionsResourceWithRawResponse,
    AttributeDefinitionsResourceWithStreamingResponse,
    AsyncAttributeDefinitionsResourceWithStreamingResponse,
)
from .management.management import ManagementResource, AsyncManagementResource
from .dynamic_endpoints.dynamic_endpoints import DynamicEndpointsResource, AsyncDynamicEndpointsResource
from .attribute_definitions.attribute_definitions import AttributeDefinitionsResource, AsyncAttributeDefinitionsResource

__all__ = ["BanksResource", "AsyncBanksResource"]


class BanksResource(SyncAPIResource):
    @cached_property
    def customers(self) -> CustomersResource:
        return CustomersResource(self._client)

    @cached_property
    def account_applications(self) -> AccountApplicationsResource:
        return AccountApplicationsResource(self._client)

    @cached_property
    def account_web_hooks(self) -> AccountWebHooksResource:
        return AccountWebHooksResource(self._client)

    @cached_property
    def accounts(self) -> AccountsResource:
        return AccountsResource(self._client)

    @cached_property
    def adapter(self) -> AdapterResource:
        return AdapterResource(self._client)

    @cached_property
    def atms(self) -> AtmsResource:
        return AtmsResource(self._client)

    @cached_property
    def attributes(self) -> AttributesResource:
        return AttributesResource(self._client)

    @cached_property
    def attribute_definitions(self) -> AttributeDefinitionsResource:
        return AttributeDefinitionsResource(self._client)

    @cached_property
    def balances(self) -> BalancesResource:
        return BalancesResource(self._client)

    @cached_property
    def branches(self) -> BranchesResource:
        return BranchesResource(self._client)

    @cached_property
    def consents(self) -> ConsentsResource:
        return ConsentsResource(self._client)

    @cached_property
    def entitlements(self) -> EntitlementsResource:
        return EntitlementsResource(self._client)

    @cached_property
    def firehose_customers(self) -> FirehoseCustomersResource:
        return FirehoseCustomersResource(self._client)

    @cached_property
    def fx(self) -> FxResource:
        return FxResource(self._client)

    @cached_property
    def management(self) -> ManagementResource:
        return ManagementResource(self._client)

    @cached_property
    def meetings(self) -> MeetingsResource:
        return MeetingsResource(self._client)

    @cached_property
    def my_consent_infos(self) -> MyConsentInfosResource:
        return MyConsentInfosResource(self._client)

    @cached_property
    def my_consents(self) -> MyConsentsResource:
        return MyConsentsResource(self._client)

    @cached_property
    def webhooks(self) -> WebhooksResource:
        return WebhooksResource(self._client)

    @cached_property
    def dynamic_endpoints(self) -> DynamicEndpointsResource:
        return DynamicEndpointsResource(self._client)

    @cached_property
    def dynamic_entities(self) -> DynamicEntitiesResource:
        return DynamicEntitiesResource(self._client)

    @cached_property
    def dynamic_message_docs(self) -> DynamicMessageDocsResource:
        return DynamicMessageDocsResource(self._client)

    @cached_property
    def with_raw_response(self) -> BanksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return BanksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BanksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return BanksResourceWithStreamingResponse(self)

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
        <p>Create a new bank (Authenticated access).</p><p>The user creating this will be automatically assigned the Role CanCreateEntitlementAtOneBank.<br />Thus the User can manage the bank they create and assign Roles to other Users.</p><p>Only SANDBOX mode<br />The settlement accounts are created specified by the bank in the POST body.<br />Name and account id are created in accordance to the next rules:<br />- Incoming account (name: Default incoming settlement account, Account ID: OBP_DEFAULT_INCOMING_ACCOUNT_ID, currency: EUR)<br />- Outgoing account (name: Default outgoing settlement account, Account ID: OBP_DEFAULT_OUTGOING_ACCOUNT_ID, currency: EUR)</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/banks",
            body=maybe_transform(body, bank_create_params.BankCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def retrieve(
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
        <p>Get the bank specified by BANK_ID<br />Returns information about a single bank specified by BANK_ID including:</p><ul><li>Bank code and full name of bank</li><li>Logo URL</li><li>Website</li></ul><p>Authentication is Optional</p>

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
            f"/obp/v5.1.0/banks/{bank_id}",
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
        <p>Update an existing bank (Authenticated access).</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/obp/v5.1.0/banks",
            body=maybe_transform(body, bank_update_params.BankUpdateParams),
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
        """
        <p>Get banks on this API instance<br />Returns a list of banks supported on this server:</p><ul><li>ID used as parameter in URLs</li><li>Short and full name of bank</li><li>Logo URL</li><li>Website</li></ul><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/banks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncBanksResource(AsyncAPIResource):
    @cached_property
    def customers(self) -> AsyncCustomersResource:
        return AsyncCustomersResource(self._client)

    @cached_property
    def account_applications(self) -> AsyncAccountApplicationsResource:
        return AsyncAccountApplicationsResource(self._client)

    @cached_property
    def account_web_hooks(self) -> AsyncAccountWebHooksResource:
        return AsyncAccountWebHooksResource(self._client)

    @cached_property
    def accounts(self) -> AsyncAccountsResource:
        return AsyncAccountsResource(self._client)

    @cached_property
    def adapter(self) -> AsyncAdapterResource:
        return AsyncAdapterResource(self._client)

    @cached_property
    def atms(self) -> AsyncAtmsResource:
        return AsyncAtmsResource(self._client)

    @cached_property
    def attributes(self) -> AsyncAttributesResource:
        return AsyncAttributesResource(self._client)

    @cached_property
    def attribute_definitions(self) -> AsyncAttributeDefinitionsResource:
        return AsyncAttributeDefinitionsResource(self._client)

    @cached_property
    def balances(self) -> AsyncBalancesResource:
        return AsyncBalancesResource(self._client)

    @cached_property
    def branches(self) -> AsyncBranchesResource:
        return AsyncBranchesResource(self._client)

    @cached_property
    def consents(self) -> AsyncConsentsResource:
        return AsyncConsentsResource(self._client)

    @cached_property
    def entitlements(self) -> AsyncEntitlementsResource:
        return AsyncEntitlementsResource(self._client)

    @cached_property
    def firehose_customers(self) -> AsyncFirehoseCustomersResource:
        return AsyncFirehoseCustomersResource(self._client)

    @cached_property
    def fx(self) -> AsyncFxResource:
        return AsyncFxResource(self._client)

    @cached_property
    def management(self) -> AsyncManagementResource:
        return AsyncManagementResource(self._client)

    @cached_property
    def meetings(self) -> AsyncMeetingsResource:
        return AsyncMeetingsResource(self._client)

    @cached_property
    def my_consent_infos(self) -> AsyncMyConsentInfosResource:
        return AsyncMyConsentInfosResource(self._client)

    @cached_property
    def my_consents(self) -> AsyncMyConsentsResource:
        return AsyncMyConsentsResource(self._client)

    @cached_property
    def webhooks(self) -> AsyncWebhooksResource:
        return AsyncWebhooksResource(self._client)

    @cached_property
    def dynamic_endpoints(self) -> AsyncDynamicEndpointsResource:
        return AsyncDynamicEndpointsResource(self._client)

    @cached_property
    def dynamic_entities(self) -> AsyncDynamicEntitiesResource:
        return AsyncDynamicEntitiesResource(self._client)

    @cached_property
    def dynamic_message_docs(self) -> AsyncDynamicMessageDocsResource:
        return AsyncDynamicMessageDocsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncBanksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBanksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBanksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncBanksResourceWithStreamingResponse(self)

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
        <p>Create a new bank (Authenticated access).</p><p>The user creating this will be automatically assigned the Role CanCreateEntitlementAtOneBank.<br />Thus the User can manage the bank they create and assign Roles to other Users.</p><p>Only SANDBOX mode<br />The settlement accounts are created specified by the bank in the POST body.<br />Name and account id are created in accordance to the next rules:<br />- Incoming account (name: Default incoming settlement account, Account ID: OBP_DEFAULT_INCOMING_ACCOUNT_ID, currency: EUR)<br />- Outgoing account (name: Default outgoing settlement account, Account ID: OBP_DEFAULT_OUTGOING_ACCOUNT_ID, currency: EUR)</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/banks",
            body=await async_maybe_transform(body, bank_create_params.BankCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def retrieve(
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
        <p>Get the bank specified by BANK_ID<br />Returns information about a single bank specified by BANK_ID including:</p><ul><li>Bank code and full name of bank</li><li>Logo URL</li><li>Website</li></ul><p>Authentication is Optional</p>

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
            f"/obp/v5.1.0/banks/{bank_id}",
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
        <p>Update an existing bank (Authenticated access).</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/obp/v5.1.0/banks",
            body=await async_maybe_transform(body, bank_update_params.BankUpdateParams),
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
        """
        <p>Get banks on this API instance<br />Returns a list of banks supported on this server:</p><ul><li>ID used as parameter in URLs</li><li>Short and full name of bank</li><li>Logo URL</li><li>Website</li></ul><p>Authentication is Optional</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/banks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class BanksResourceWithRawResponse:
    def __init__(self, banks: BanksResource) -> None:
        self._banks = banks

        self.create = to_custom_raw_response_wrapper(
            banks.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            banks.retrieve,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            banks.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            banks.list,
            BinaryAPIResponse,
        )

    @cached_property
    def customers(self) -> CustomersResourceWithRawResponse:
        return CustomersResourceWithRawResponse(self._banks.customers)

    @cached_property
    def account_applications(self) -> AccountApplicationsResourceWithRawResponse:
        return AccountApplicationsResourceWithRawResponse(self._banks.account_applications)

    @cached_property
    def account_web_hooks(self) -> AccountWebHooksResourceWithRawResponse:
        return AccountWebHooksResourceWithRawResponse(self._banks.account_web_hooks)

    @cached_property
    def accounts(self) -> AccountsResourceWithRawResponse:
        return AccountsResourceWithRawResponse(self._banks.accounts)

    @cached_property
    def adapter(self) -> AdapterResourceWithRawResponse:
        return AdapterResourceWithRawResponse(self._banks.adapter)

    @cached_property
    def atms(self) -> AtmsResourceWithRawResponse:
        return AtmsResourceWithRawResponse(self._banks.atms)

    @cached_property
    def attributes(self) -> AttributesResourceWithRawResponse:
        return AttributesResourceWithRawResponse(self._banks.attributes)

    @cached_property
    def attribute_definitions(self) -> AttributeDefinitionsResourceWithRawResponse:
        return AttributeDefinitionsResourceWithRawResponse(self._banks.attribute_definitions)

    @cached_property
    def balances(self) -> BalancesResourceWithRawResponse:
        return BalancesResourceWithRawResponse(self._banks.balances)

    @cached_property
    def branches(self) -> BranchesResourceWithRawResponse:
        return BranchesResourceWithRawResponse(self._banks.branches)

    @cached_property
    def consents(self) -> ConsentsResourceWithRawResponse:
        return ConsentsResourceWithRawResponse(self._banks.consents)

    @cached_property
    def entitlements(self) -> EntitlementsResourceWithRawResponse:
        return EntitlementsResourceWithRawResponse(self._banks.entitlements)

    @cached_property
    def firehose_customers(self) -> FirehoseCustomersResourceWithRawResponse:
        return FirehoseCustomersResourceWithRawResponse(self._banks.firehose_customers)

    @cached_property
    def fx(self) -> FxResourceWithRawResponse:
        return FxResourceWithRawResponse(self._banks.fx)

    @cached_property
    def management(self) -> ManagementResourceWithRawResponse:
        return ManagementResourceWithRawResponse(self._banks.management)

    @cached_property
    def meetings(self) -> MeetingsResourceWithRawResponse:
        return MeetingsResourceWithRawResponse(self._banks.meetings)

    @cached_property
    def my_consent_infos(self) -> MyConsentInfosResourceWithRawResponse:
        return MyConsentInfosResourceWithRawResponse(self._banks.my_consent_infos)

    @cached_property
    def my_consents(self) -> MyConsentsResourceWithRawResponse:
        return MyConsentsResourceWithRawResponse(self._banks.my_consents)

    @cached_property
    def webhooks(self) -> WebhooksResourceWithRawResponse:
        return WebhooksResourceWithRawResponse(self._banks.webhooks)

    @cached_property
    def dynamic_endpoints(self) -> DynamicEndpointsResourceWithRawResponse:
        return DynamicEndpointsResourceWithRawResponse(self._banks.dynamic_endpoints)

    @cached_property
    def dynamic_entities(self) -> DynamicEntitiesResourceWithRawResponse:
        return DynamicEntitiesResourceWithRawResponse(self._banks.dynamic_entities)

    @cached_property
    def dynamic_message_docs(self) -> DynamicMessageDocsResourceWithRawResponse:
        return DynamicMessageDocsResourceWithRawResponse(self._banks.dynamic_message_docs)


class AsyncBanksResourceWithRawResponse:
    def __init__(self, banks: AsyncBanksResource) -> None:
        self._banks = banks

        self.create = async_to_custom_raw_response_wrapper(
            banks.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            banks.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            banks.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            banks.list,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def customers(self) -> AsyncCustomersResourceWithRawResponse:
        return AsyncCustomersResourceWithRawResponse(self._banks.customers)

    @cached_property
    def account_applications(self) -> AsyncAccountApplicationsResourceWithRawResponse:
        return AsyncAccountApplicationsResourceWithRawResponse(self._banks.account_applications)

    @cached_property
    def account_web_hooks(self) -> AsyncAccountWebHooksResourceWithRawResponse:
        return AsyncAccountWebHooksResourceWithRawResponse(self._banks.account_web_hooks)

    @cached_property
    def accounts(self) -> AsyncAccountsResourceWithRawResponse:
        return AsyncAccountsResourceWithRawResponse(self._banks.accounts)

    @cached_property
    def adapter(self) -> AsyncAdapterResourceWithRawResponse:
        return AsyncAdapterResourceWithRawResponse(self._banks.adapter)

    @cached_property
    def atms(self) -> AsyncAtmsResourceWithRawResponse:
        return AsyncAtmsResourceWithRawResponse(self._banks.atms)

    @cached_property
    def attributes(self) -> AsyncAttributesResourceWithRawResponse:
        return AsyncAttributesResourceWithRawResponse(self._banks.attributes)

    @cached_property
    def attribute_definitions(self) -> AsyncAttributeDefinitionsResourceWithRawResponse:
        return AsyncAttributeDefinitionsResourceWithRawResponse(self._banks.attribute_definitions)

    @cached_property
    def balances(self) -> AsyncBalancesResourceWithRawResponse:
        return AsyncBalancesResourceWithRawResponse(self._banks.balances)

    @cached_property
    def branches(self) -> AsyncBranchesResourceWithRawResponse:
        return AsyncBranchesResourceWithRawResponse(self._banks.branches)

    @cached_property
    def consents(self) -> AsyncConsentsResourceWithRawResponse:
        return AsyncConsentsResourceWithRawResponse(self._banks.consents)

    @cached_property
    def entitlements(self) -> AsyncEntitlementsResourceWithRawResponse:
        return AsyncEntitlementsResourceWithRawResponse(self._banks.entitlements)

    @cached_property
    def firehose_customers(self) -> AsyncFirehoseCustomersResourceWithRawResponse:
        return AsyncFirehoseCustomersResourceWithRawResponse(self._banks.firehose_customers)

    @cached_property
    def fx(self) -> AsyncFxResourceWithRawResponse:
        return AsyncFxResourceWithRawResponse(self._banks.fx)

    @cached_property
    def management(self) -> AsyncManagementResourceWithRawResponse:
        return AsyncManagementResourceWithRawResponse(self._banks.management)

    @cached_property
    def meetings(self) -> AsyncMeetingsResourceWithRawResponse:
        return AsyncMeetingsResourceWithRawResponse(self._banks.meetings)

    @cached_property
    def my_consent_infos(self) -> AsyncMyConsentInfosResourceWithRawResponse:
        return AsyncMyConsentInfosResourceWithRawResponse(self._banks.my_consent_infos)

    @cached_property
    def my_consents(self) -> AsyncMyConsentsResourceWithRawResponse:
        return AsyncMyConsentsResourceWithRawResponse(self._banks.my_consents)

    @cached_property
    def webhooks(self) -> AsyncWebhooksResourceWithRawResponse:
        return AsyncWebhooksResourceWithRawResponse(self._banks.webhooks)

    @cached_property
    def dynamic_endpoints(self) -> AsyncDynamicEndpointsResourceWithRawResponse:
        return AsyncDynamicEndpointsResourceWithRawResponse(self._banks.dynamic_endpoints)

    @cached_property
    def dynamic_entities(self) -> AsyncDynamicEntitiesResourceWithRawResponse:
        return AsyncDynamicEntitiesResourceWithRawResponse(self._banks.dynamic_entities)

    @cached_property
    def dynamic_message_docs(self) -> AsyncDynamicMessageDocsResourceWithRawResponse:
        return AsyncDynamicMessageDocsResourceWithRawResponse(self._banks.dynamic_message_docs)


class BanksResourceWithStreamingResponse:
    def __init__(self, banks: BanksResource) -> None:
        self._banks = banks

        self.create = to_custom_streamed_response_wrapper(
            banks.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            banks.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            banks.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            banks.list,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def customers(self) -> CustomersResourceWithStreamingResponse:
        return CustomersResourceWithStreamingResponse(self._banks.customers)

    @cached_property
    def account_applications(self) -> AccountApplicationsResourceWithStreamingResponse:
        return AccountApplicationsResourceWithStreamingResponse(self._banks.account_applications)

    @cached_property
    def account_web_hooks(self) -> AccountWebHooksResourceWithStreamingResponse:
        return AccountWebHooksResourceWithStreamingResponse(self._banks.account_web_hooks)

    @cached_property
    def accounts(self) -> AccountsResourceWithStreamingResponse:
        return AccountsResourceWithStreamingResponse(self._banks.accounts)

    @cached_property
    def adapter(self) -> AdapterResourceWithStreamingResponse:
        return AdapterResourceWithStreamingResponse(self._banks.adapter)

    @cached_property
    def atms(self) -> AtmsResourceWithStreamingResponse:
        return AtmsResourceWithStreamingResponse(self._banks.atms)

    @cached_property
    def attributes(self) -> AttributesResourceWithStreamingResponse:
        return AttributesResourceWithStreamingResponse(self._banks.attributes)

    @cached_property
    def attribute_definitions(self) -> AttributeDefinitionsResourceWithStreamingResponse:
        return AttributeDefinitionsResourceWithStreamingResponse(self._banks.attribute_definitions)

    @cached_property
    def balances(self) -> BalancesResourceWithStreamingResponse:
        return BalancesResourceWithStreamingResponse(self._banks.balances)

    @cached_property
    def branches(self) -> BranchesResourceWithStreamingResponse:
        return BranchesResourceWithStreamingResponse(self._banks.branches)

    @cached_property
    def consents(self) -> ConsentsResourceWithStreamingResponse:
        return ConsentsResourceWithStreamingResponse(self._banks.consents)

    @cached_property
    def entitlements(self) -> EntitlementsResourceWithStreamingResponse:
        return EntitlementsResourceWithStreamingResponse(self._banks.entitlements)

    @cached_property
    def firehose_customers(self) -> FirehoseCustomersResourceWithStreamingResponse:
        return FirehoseCustomersResourceWithStreamingResponse(self._banks.firehose_customers)

    @cached_property
    def fx(self) -> FxResourceWithStreamingResponse:
        return FxResourceWithStreamingResponse(self._banks.fx)

    @cached_property
    def management(self) -> ManagementResourceWithStreamingResponse:
        return ManagementResourceWithStreamingResponse(self._banks.management)

    @cached_property
    def meetings(self) -> MeetingsResourceWithStreamingResponse:
        return MeetingsResourceWithStreamingResponse(self._banks.meetings)

    @cached_property
    def my_consent_infos(self) -> MyConsentInfosResourceWithStreamingResponse:
        return MyConsentInfosResourceWithStreamingResponse(self._banks.my_consent_infos)

    @cached_property
    def my_consents(self) -> MyConsentsResourceWithStreamingResponse:
        return MyConsentsResourceWithStreamingResponse(self._banks.my_consents)

    @cached_property
    def webhooks(self) -> WebhooksResourceWithStreamingResponse:
        return WebhooksResourceWithStreamingResponse(self._banks.webhooks)

    @cached_property
    def dynamic_endpoints(self) -> DynamicEndpointsResourceWithStreamingResponse:
        return DynamicEndpointsResourceWithStreamingResponse(self._banks.dynamic_endpoints)

    @cached_property
    def dynamic_entities(self) -> DynamicEntitiesResourceWithStreamingResponse:
        return DynamicEntitiesResourceWithStreamingResponse(self._banks.dynamic_entities)

    @cached_property
    def dynamic_message_docs(self) -> DynamicMessageDocsResourceWithStreamingResponse:
        return DynamicMessageDocsResourceWithStreamingResponse(self._banks.dynamic_message_docs)


class AsyncBanksResourceWithStreamingResponse:
    def __init__(self, banks: AsyncBanksResource) -> None:
        self._banks = banks

        self.create = async_to_custom_streamed_response_wrapper(
            banks.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            banks.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            banks.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            banks.list,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def customers(self) -> AsyncCustomersResourceWithStreamingResponse:
        return AsyncCustomersResourceWithStreamingResponse(self._banks.customers)

    @cached_property
    def account_applications(self) -> AsyncAccountApplicationsResourceWithStreamingResponse:
        return AsyncAccountApplicationsResourceWithStreamingResponse(self._banks.account_applications)

    @cached_property
    def account_web_hooks(self) -> AsyncAccountWebHooksResourceWithStreamingResponse:
        return AsyncAccountWebHooksResourceWithStreamingResponse(self._banks.account_web_hooks)

    @cached_property
    def accounts(self) -> AsyncAccountsResourceWithStreamingResponse:
        return AsyncAccountsResourceWithStreamingResponse(self._banks.accounts)

    @cached_property
    def adapter(self) -> AsyncAdapterResourceWithStreamingResponse:
        return AsyncAdapterResourceWithStreamingResponse(self._banks.adapter)

    @cached_property
    def atms(self) -> AsyncAtmsResourceWithStreamingResponse:
        return AsyncAtmsResourceWithStreamingResponse(self._banks.atms)

    @cached_property
    def attributes(self) -> AsyncAttributesResourceWithStreamingResponse:
        return AsyncAttributesResourceWithStreamingResponse(self._banks.attributes)

    @cached_property
    def attribute_definitions(self) -> AsyncAttributeDefinitionsResourceWithStreamingResponse:
        return AsyncAttributeDefinitionsResourceWithStreamingResponse(self._banks.attribute_definitions)

    @cached_property
    def balances(self) -> AsyncBalancesResourceWithStreamingResponse:
        return AsyncBalancesResourceWithStreamingResponse(self._banks.balances)

    @cached_property
    def branches(self) -> AsyncBranchesResourceWithStreamingResponse:
        return AsyncBranchesResourceWithStreamingResponse(self._banks.branches)

    @cached_property
    def consents(self) -> AsyncConsentsResourceWithStreamingResponse:
        return AsyncConsentsResourceWithStreamingResponse(self._banks.consents)

    @cached_property
    def entitlements(self) -> AsyncEntitlementsResourceWithStreamingResponse:
        return AsyncEntitlementsResourceWithStreamingResponse(self._banks.entitlements)

    @cached_property
    def firehose_customers(self) -> AsyncFirehoseCustomersResourceWithStreamingResponse:
        return AsyncFirehoseCustomersResourceWithStreamingResponse(self._banks.firehose_customers)

    @cached_property
    def fx(self) -> AsyncFxResourceWithStreamingResponse:
        return AsyncFxResourceWithStreamingResponse(self._banks.fx)

    @cached_property
    def management(self) -> AsyncManagementResourceWithStreamingResponse:
        return AsyncManagementResourceWithStreamingResponse(self._banks.management)

    @cached_property
    def meetings(self) -> AsyncMeetingsResourceWithStreamingResponse:
        return AsyncMeetingsResourceWithStreamingResponse(self._banks.meetings)

    @cached_property
    def my_consent_infos(self) -> AsyncMyConsentInfosResourceWithStreamingResponse:
        return AsyncMyConsentInfosResourceWithStreamingResponse(self._banks.my_consent_infos)

    @cached_property
    def my_consents(self) -> AsyncMyConsentsResourceWithStreamingResponse:
        return AsyncMyConsentsResourceWithStreamingResponse(self._banks.my_consents)

    @cached_property
    def webhooks(self) -> AsyncWebhooksResourceWithStreamingResponse:
        return AsyncWebhooksResourceWithStreamingResponse(self._banks.webhooks)

    @cached_property
    def dynamic_endpoints(self) -> AsyncDynamicEndpointsResourceWithStreamingResponse:
        return AsyncDynamicEndpointsResourceWithStreamingResponse(self._banks.dynamic_endpoints)

    @cached_property
    def dynamic_entities(self) -> AsyncDynamicEntitiesResourceWithStreamingResponse:
        return AsyncDynamicEntitiesResourceWithStreamingResponse(self._banks.dynamic_entities)

    @cached_property
    def dynamic_message_docs(self) -> AsyncDynamicMessageDocsResourceWithStreamingResponse:
        return AsyncDynamicMessageDocsResourceWithStreamingResponse(self._banks.dynamic_message_docs)
