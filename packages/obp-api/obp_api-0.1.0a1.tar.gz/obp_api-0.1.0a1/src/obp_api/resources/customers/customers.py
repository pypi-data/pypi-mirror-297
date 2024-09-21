# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .data import (
    DataResource,
    AsyncDataResource,
    DataResourceWithRawResponse,
    AsyncDataResourceWithRawResponse,
    DataResourceWithStreamingResponse,
    AsyncDataResourceWithStreamingResponse,
)
from .email import (
    EmailResource,
    AsyncEmailResource,
    EmailResourceWithRawResponse,
    AsyncEmailResourceWithRawResponse,
    EmailResourceWithStreamingResponse,
    AsyncEmailResourceWithStreamingResponse,
)
from .branch import (
    BranchResource,
    AsyncBranchResource,
    BranchResourceWithRawResponse,
    AsyncBranchResourceWithRawResponse,
    BranchResourceWithStreamingResponse,
    AsyncBranchResourceWithStreamingResponse,
)
from .number import (
    NumberResource,
    AsyncNumberResource,
    NumberResourceWithRawResponse,
    AsyncNumberResourceWithRawResponse,
    NumberResourceWithStreamingResponse,
    AsyncNumberResourceWithStreamingResponse,
)
from ...types import customer_create_params
from .cascade import (
    CascadeResource,
    AsyncCascadeResource,
    CascadeResourceWithRawResponse,
    AsyncCascadeResourceWithRawResponse,
    CascadeResourceWithStreamingResponse,
    AsyncCascadeResourceWithStreamingResponse,
)
from .minimal import (
    MinimalResource,
    AsyncMinimalResource,
    MinimalResourceWithRawResponse,
    AsyncMinimalResourceWithRawResponse,
    MinimalResourceWithStreamingResponse,
    AsyncMinimalResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .identity import (
    IdentityResource,
    AsyncIdentityResource,
    IdentityResourceWithRawResponse,
    AsyncIdentityResourceWithRawResponse,
    IdentityResourceWithStreamingResponse,
    AsyncIdentityResourceWithStreamingResponse,
)
from .messages import (
    MessagesResource,
    AsyncMessagesResource,
    MessagesResourceWithRawResponse,
    AsyncMessagesResourceWithRawResponse,
    MessagesResourceWithStreamingResponse,
    AsyncMessagesResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .addresses import (
    AddressesResource,
    AsyncAddressesResource,
    AddressesResourceWithRawResponse,
    AsyncAddressesResourceWithRawResponse,
    AddressesResourceWithStreamingResponse,
    AsyncAddressesResourceWithStreamingResponse,
)
from .attribute import (
    AttributeResource,
    AsyncAttributeResource,
    AttributeResourceWithRawResponse,
    AsyncAttributeResourceWithRawResponse,
    AttributeResourceWithStreamingResponse,
    AsyncAttributeResourceWithStreamingResponse,
)
from .kyc_media import (
    KYCMediaResource,
    AsyncKYCMediaResource,
    KYCMediaResourceWithRawResponse,
    AsyncKYCMediaResourceWithRawResponse,
    KYCMediaResourceWithStreamingResponse,
    AsyncKYCMediaResourceWithStreamingResponse,
)
from .attributes import (
    AttributesResource,
    AsyncAttributesResource,
    AttributesResourceWithRawResponse,
    AsyncAttributesResourceWithRawResponse,
    AttributesResourceWithStreamingResponse,
    AsyncAttributesResourceWithStreamingResponse,
)
from .kyc_checks import (
    KYCChecksResource,
    AsyncKYCChecksResource,
    KYCChecksResourceWithRawResponse,
    AsyncKYCChecksResourceWithRawResponse,
    KYCChecksResourceWithStreamingResponse,
    AsyncKYCChecksResourceWithStreamingResponse,
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
from .credit_limit import (
    CreditLimitResource,
    AsyncCreditLimitResource,
    CreditLimitResourceWithRawResponse,
    AsyncCreditLimitResourceWithRawResponse,
    CreditLimitResourceWithStreamingResponse,
    AsyncCreditLimitResourceWithStreamingResponse,
)
from .kyc_statuses import (
    KYCStatusesResource,
    AsyncKYCStatusesResource,
    KYCStatusesResourceWithRawResponse,
    AsyncKYCStatusesResourceWithRawResponse,
    KYCStatusesResourceWithStreamingResponse,
    AsyncKYCStatusesResourceWithStreamingResponse,
)
from .kyc_documents import (
    KYCDocumentsResource,
    AsyncKYCDocumentsResource,
    KYCDocumentsResourceWithRawResponse,
    AsyncKYCDocumentsResourceWithRawResponse,
    KYCDocumentsResourceWithStreamingResponse,
    AsyncKYCDocumentsResourceWithStreamingResponse,
)
from .mobile_number import (
    MobileNumberResource,
    AsyncMobileNumberResource,
    MobileNumberResourceWithRawResponse,
    AsyncMobileNumberResourceWithRawResponse,
    MobileNumberResourceWithStreamingResponse,
    AsyncMobileNumberResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from .tax_residences import (
    TaxResidencesResource,
    AsyncTaxResidencesResource,
    TaxResidencesResourceWithRawResponse,
    AsyncTaxResidencesResourceWithRawResponse,
    TaxResidencesResourceWithStreamingResponse,
    AsyncTaxResidencesResourceWithStreamingResponse,
)
from .customer_number import (
    CustomerNumberResource,
    AsyncCustomerNumberResource,
    CustomerNumberResourceWithRawResponse,
    AsyncCustomerNumberResourceWithRawResponse,
    CustomerNumberResourceWithStreamingResponse,
    AsyncCustomerNumberResourceWithStreamingResponse,
)
from .accounts_minimal import (
    AccountsMinimalResource,
    AsyncAccountsMinimalResource,
    AccountsMinimalResourceWithRawResponse,
    AsyncAccountsMinimalResourceWithRawResponse,
    AccountsMinimalResourceWithStreamingResponse,
    AsyncAccountsMinimalResourceWithStreamingResponse,
)
from .correlated_users import (
    CorrelatedUsersResource,
    AsyncCorrelatedUsersResource,
    CorrelatedUsersResourceWithRawResponse,
    AsyncCorrelatedUsersResourceWithRawResponse,
    CorrelatedUsersResourceWithStreamingResponse,
    AsyncCorrelatedUsersResourceWithStreamingResponse,
)
from .social_media_handles import (
    SocialMediaHandlesResource,
    AsyncSocialMediaHandlesResource,
    SocialMediaHandlesResourceWithRawResponse,
    AsyncSocialMediaHandlesResourceWithRawResponse,
    SocialMediaHandlesResourceWithStreamingResponse,
    AsyncSocialMediaHandlesResourceWithStreamingResponse,
)
from .customer_number_query import (
    CustomerNumberQueryResource,
    AsyncCustomerNumberQueryResource,
    CustomerNumberQueryResourceWithRawResponse,
    AsyncCustomerNumberQueryResourceWithRawResponse,
    CustomerNumberQueryResourceWithStreamingResponse,
    AsyncCustomerNumberQueryResourceWithStreamingResponse,
)
from .customer_account_links import (
    CustomerAccountLinksResource,
    AsyncCustomerAccountLinksResource,
    CustomerAccountLinksResourceWithRawResponse,
    AsyncCustomerAccountLinksResourceWithRawResponse,
    CustomerAccountLinksResourceWithStreamingResponse,
    AsyncCustomerAccountLinksResourceWithStreamingResponse,
)
from .credit_rating_and_source import (
    CreditRatingAndSourceResource,
    AsyncCreditRatingAndSourceResource,
    CreditRatingAndSourceResourceWithRawResponse,
    AsyncCreditRatingAndSourceResourceWithRawResponse,
    CreditRatingAndSourceResourceWithStreamingResponse,
    AsyncCreditRatingAndSourceResourceWithStreamingResponse,
)
from .customer_number_query.customer_number_query import CustomerNumberQueryResource, AsyncCustomerNumberQueryResource

__all__ = ["CustomersResource", "AsyncCustomersResource"]


class CustomersResource(SyncAPIResource):
    @cached_property
    def messages(self) -> MessagesResource:
        return MessagesResource(self._client)

    @cached_property
    def minimal(self) -> MinimalResource:
        return MinimalResource(self._client)

    @cached_property
    def addresses(self) -> AddressesResource:
        return AddressesResource(self._client)

    @cached_property
    def attribute(self) -> AttributeResource:
        return AttributeResource(self._client)

    @cached_property
    def attributes(self) -> AttributesResource:
        return AttributesResource(self._client)

    @cached_property
    def branch(self) -> BranchResource:
        return BranchResource(self._client)

    @cached_property
    def correlated_users(self) -> CorrelatedUsersResource:
        return CorrelatedUsersResource(self._client)

    @cached_property
    def credit_limit(self) -> CreditLimitResource:
        return CreditLimitResource(self._client)

    @cached_property
    def credit_rating_and_source(self) -> CreditRatingAndSourceResource:
        return CreditRatingAndSourceResource(self._client)

    @cached_property
    def customer_account_links(self) -> CustomerAccountLinksResource:
        return CustomerAccountLinksResource(self._client)

    @cached_property
    def data(self) -> DataResource:
        return DataResource(self._client)

    @cached_property
    def email(self) -> EmailResource:
        return EmailResource(self._client)

    @cached_property
    def identity(self) -> IdentityResource:
        return IdentityResource(self._client)

    @cached_property
    def kyc_checks(self) -> KYCChecksResource:
        return KYCChecksResource(self._client)

    @cached_property
    def kyc_documents(self) -> KYCDocumentsResource:
        return KYCDocumentsResource(self._client)

    @cached_property
    def kyc_media(self) -> KYCMediaResource:
        return KYCMediaResource(self._client)

    @cached_property
    def kyc_statuses(self) -> KYCStatusesResource:
        return KYCStatusesResource(self._client)

    @cached_property
    def mobile_number(self) -> MobileNumberResource:
        return MobileNumberResource(self._client)

    @cached_property
    def number(self) -> NumberResource:
        return NumberResource(self._client)

    @cached_property
    def social_media_handles(self) -> SocialMediaHandlesResource:
        return SocialMediaHandlesResource(self._client)

    @cached_property
    def tax_residences(self) -> TaxResidencesResource:
        return TaxResidencesResource(self._client)

    @cached_property
    def customer_number(self) -> CustomerNumberResource:
        return CustomerNumberResource(self._client)

    @cached_property
    def customer_number_query(self) -> CustomerNumberQueryResource:
        return CustomerNumberQueryResource(self._client)

    @cached_property
    def accounts_minimal(self) -> AccountsMinimalResource:
        return AccountsMinimalResource(self._client)

    @cached_property
    def cascade(self) -> CascadeResource:
        return CascadeResource(self._client)

    @cached_property
    def with_raw_response(self) -> CustomersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return CustomersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CustomersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return CustomersResourceWithStreamingResponse(self)

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
        <p>The Customer resource stores the customer number (which is set by the backend), legal name, email, phone number, their date of birth, relationship status, education attained, a url for a profile image, KYC status etc.<br />Dates need to be in the format 2013-01-21T23:08:00Z</p><p>Note: If you need to set a specific customer number, use the Update Customer Number endpoint after this call.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/customers",
            body=maybe_transform(body, customer_create_params.CustomerCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def retrieve(
        self,
        customer_id: str,
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
        <p>Gets the Customer specified by CUSTOMER_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}",
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
        <p>Gets all Customers that are linked to me.</p><p>Authentication via OAuth is required.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/my/customers",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncCustomersResource(AsyncAPIResource):
    @cached_property
    def messages(self) -> AsyncMessagesResource:
        return AsyncMessagesResource(self._client)

    @cached_property
    def minimal(self) -> AsyncMinimalResource:
        return AsyncMinimalResource(self._client)

    @cached_property
    def addresses(self) -> AsyncAddressesResource:
        return AsyncAddressesResource(self._client)

    @cached_property
    def attribute(self) -> AsyncAttributeResource:
        return AsyncAttributeResource(self._client)

    @cached_property
    def attributes(self) -> AsyncAttributesResource:
        return AsyncAttributesResource(self._client)

    @cached_property
    def branch(self) -> AsyncBranchResource:
        return AsyncBranchResource(self._client)

    @cached_property
    def correlated_users(self) -> AsyncCorrelatedUsersResource:
        return AsyncCorrelatedUsersResource(self._client)

    @cached_property
    def credit_limit(self) -> AsyncCreditLimitResource:
        return AsyncCreditLimitResource(self._client)

    @cached_property
    def credit_rating_and_source(self) -> AsyncCreditRatingAndSourceResource:
        return AsyncCreditRatingAndSourceResource(self._client)

    @cached_property
    def customer_account_links(self) -> AsyncCustomerAccountLinksResource:
        return AsyncCustomerAccountLinksResource(self._client)

    @cached_property
    def data(self) -> AsyncDataResource:
        return AsyncDataResource(self._client)

    @cached_property
    def email(self) -> AsyncEmailResource:
        return AsyncEmailResource(self._client)

    @cached_property
    def identity(self) -> AsyncIdentityResource:
        return AsyncIdentityResource(self._client)

    @cached_property
    def kyc_checks(self) -> AsyncKYCChecksResource:
        return AsyncKYCChecksResource(self._client)

    @cached_property
    def kyc_documents(self) -> AsyncKYCDocumentsResource:
        return AsyncKYCDocumentsResource(self._client)

    @cached_property
    def kyc_media(self) -> AsyncKYCMediaResource:
        return AsyncKYCMediaResource(self._client)

    @cached_property
    def kyc_statuses(self) -> AsyncKYCStatusesResource:
        return AsyncKYCStatusesResource(self._client)

    @cached_property
    def mobile_number(self) -> AsyncMobileNumberResource:
        return AsyncMobileNumberResource(self._client)

    @cached_property
    def number(self) -> AsyncNumberResource:
        return AsyncNumberResource(self._client)

    @cached_property
    def social_media_handles(self) -> AsyncSocialMediaHandlesResource:
        return AsyncSocialMediaHandlesResource(self._client)

    @cached_property
    def tax_residences(self) -> AsyncTaxResidencesResource:
        return AsyncTaxResidencesResource(self._client)

    @cached_property
    def customer_number(self) -> AsyncCustomerNumberResource:
        return AsyncCustomerNumberResource(self._client)

    @cached_property
    def customer_number_query(self) -> AsyncCustomerNumberQueryResource:
        return AsyncCustomerNumberQueryResource(self._client)

    @cached_property
    def accounts_minimal(self) -> AsyncAccountsMinimalResource:
        return AsyncAccountsMinimalResource(self._client)

    @cached_property
    def cascade(self) -> AsyncCascadeResource:
        return AsyncCascadeResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCustomersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCustomersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCustomersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncCustomersResourceWithStreamingResponse(self)

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
        <p>The Customer resource stores the customer number (which is set by the backend), legal name, email, phone number, their date of birth, relationship status, education attained, a url for a profile image, KYC status etc.<br />Dates need to be in the format 2013-01-21T23:08:00Z</p><p>Note: If you need to set a specific customer number, use the Update Customer Number endpoint after this call.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/customers",
            body=await async_maybe_transform(body, customer_create_params.CustomerCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def retrieve(
        self,
        customer_id: str,
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
        <p>Gets the Customer specified by CUSTOMER_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not customer_id:
            raise ValueError(f"Expected a non-empty value for `customer_id` but received {customer_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/customers/{customer_id}",
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
        <p>Gets all Customers that are linked to me.</p><p>Authentication via OAuth is required.</p><p>Authentication is Mandatory</p>
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/my/customers",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class CustomersResourceWithRawResponse:
    def __init__(self, customers: CustomersResource) -> None:
        self._customers = customers

        self.create = to_custom_raw_response_wrapper(
            customers.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            customers.retrieve,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            customers.list,
            BinaryAPIResponse,
        )

    @cached_property
    def messages(self) -> MessagesResourceWithRawResponse:
        return MessagesResourceWithRawResponse(self._customers.messages)

    @cached_property
    def minimal(self) -> MinimalResourceWithRawResponse:
        return MinimalResourceWithRawResponse(self._customers.minimal)

    @cached_property
    def addresses(self) -> AddressesResourceWithRawResponse:
        return AddressesResourceWithRawResponse(self._customers.addresses)

    @cached_property
    def attribute(self) -> AttributeResourceWithRawResponse:
        return AttributeResourceWithRawResponse(self._customers.attribute)

    @cached_property
    def attributes(self) -> AttributesResourceWithRawResponse:
        return AttributesResourceWithRawResponse(self._customers.attributes)

    @cached_property
    def branch(self) -> BranchResourceWithRawResponse:
        return BranchResourceWithRawResponse(self._customers.branch)

    @cached_property
    def correlated_users(self) -> CorrelatedUsersResourceWithRawResponse:
        return CorrelatedUsersResourceWithRawResponse(self._customers.correlated_users)

    @cached_property
    def credit_limit(self) -> CreditLimitResourceWithRawResponse:
        return CreditLimitResourceWithRawResponse(self._customers.credit_limit)

    @cached_property
    def credit_rating_and_source(self) -> CreditRatingAndSourceResourceWithRawResponse:
        return CreditRatingAndSourceResourceWithRawResponse(self._customers.credit_rating_and_source)

    @cached_property
    def customer_account_links(self) -> CustomerAccountLinksResourceWithRawResponse:
        return CustomerAccountLinksResourceWithRawResponse(self._customers.customer_account_links)

    @cached_property
    def data(self) -> DataResourceWithRawResponse:
        return DataResourceWithRawResponse(self._customers.data)

    @cached_property
    def email(self) -> EmailResourceWithRawResponse:
        return EmailResourceWithRawResponse(self._customers.email)

    @cached_property
    def identity(self) -> IdentityResourceWithRawResponse:
        return IdentityResourceWithRawResponse(self._customers.identity)

    @cached_property
    def kyc_checks(self) -> KYCChecksResourceWithRawResponse:
        return KYCChecksResourceWithRawResponse(self._customers.kyc_checks)

    @cached_property
    def kyc_documents(self) -> KYCDocumentsResourceWithRawResponse:
        return KYCDocumentsResourceWithRawResponse(self._customers.kyc_documents)

    @cached_property
    def kyc_media(self) -> KYCMediaResourceWithRawResponse:
        return KYCMediaResourceWithRawResponse(self._customers.kyc_media)

    @cached_property
    def kyc_statuses(self) -> KYCStatusesResourceWithRawResponse:
        return KYCStatusesResourceWithRawResponse(self._customers.kyc_statuses)

    @cached_property
    def mobile_number(self) -> MobileNumberResourceWithRawResponse:
        return MobileNumberResourceWithRawResponse(self._customers.mobile_number)

    @cached_property
    def number(self) -> NumberResourceWithRawResponse:
        return NumberResourceWithRawResponse(self._customers.number)

    @cached_property
    def social_media_handles(self) -> SocialMediaHandlesResourceWithRawResponse:
        return SocialMediaHandlesResourceWithRawResponse(self._customers.social_media_handles)

    @cached_property
    def tax_residences(self) -> TaxResidencesResourceWithRawResponse:
        return TaxResidencesResourceWithRawResponse(self._customers.tax_residences)

    @cached_property
    def customer_number(self) -> CustomerNumberResourceWithRawResponse:
        return CustomerNumberResourceWithRawResponse(self._customers.customer_number)

    @cached_property
    def customer_number_query(self) -> CustomerNumberQueryResourceWithRawResponse:
        return CustomerNumberQueryResourceWithRawResponse(self._customers.customer_number_query)

    @cached_property
    def accounts_minimal(self) -> AccountsMinimalResourceWithRawResponse:
        return AccountsMinimalResourceWithRawResponse(self._customers.accounts_minimal)

    @cached_property
    def cascade(self) -> CascadeResourceWithRawResponse:
        return CascadeResourceWithRawResponse(self._customers.cascade)


class AsyncCustomersResourceWithRawResponse:
    def __init__(self, customers: AsyncCustomersResource) -> None:
        self._customers = customers

        self.create = async_to_custom_raw_response_wrapper(
            customers.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            customers.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            customers.list,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def messages(self) -> AsyncMessagesResourceWithRawResponse:
        return AsyncMessagesResourceWithRawResponse(self._customers.messages)

    @cached_property
    def minimal(self) -> AsyncMinimalResourceWithRawResponse:
        return AsyncMinimalResourceWithRawResponse(self._customers.minimal)

    @cached_property
    def addresses(self) -> AsyncAddressesResourceWithRawResponse:
        return AsyncAddressesResourceWithRawResponse(self._customers.addresses)

    @cached_property
    def attribute(self) -> AsyncAttributeResourceWithRawResponse:
        return AsyncAttributeResourceWithRawResponse(self._customers.attribute)

    @cached_property
    def attributes(self) -> AsyncAttributesResourceWithRawResponse:
        return AsyncAttributesResourceWithRawResponse(self._customers.attributes)

    @cached_property
    def branch(self) -> AsyncBranchResourceWithRawResponse:
        return AsyncBranchResourceWithRawResponse(self._customers.branch)

    @cached_property
    def correlated_users(self) -> AsyncCorrelatedUsersResourceWithRawResponse:
        return AsyncCorrelatedUsersResourceWithRawResponse(self._customers.correlated_users)

    @cached_property
    def credit_limit(self) -> AsyncCreditLimitResourceWithRawResponse:
        return AsyncCreditLimitResourceWithRawResponse(self._customers.credit_limit)

    @cached_property
    def credit_rating_and_source(self) -> AsyncCreditRatingAndSourceResourceWithRawResponse:
        return AsyncCreditRatingAndSourceResourceWithRawResponse(self._customers.credit_rating_and_source)

    @cached_property
    def customer_account_links(self) -> AsyncCustomerAccountLinksResourceWithRawResponse:
        return AsyncCustomerAccountLinksResourceWithRawResponse(self._customers.customer_account_links)

    @cached_property
    def data(self) -> AsyncDataResourceWithRawResponse:
        return AsyncDataResourceWithRawResponse(self._customers.data)

    @cached_property
    def email(self) -> AsyncEmailResourceWithRawResponse:
        return AsyncEmailResourceWithRawResponse(self._customers.email)

    @cached_property
    def identity(self) -> AsyncIdentityResourceWithRawResponse:
        return AsyncIdentityResourceWithRawResponse(self._customers.identity)

    @cached_property
    def kyc_checks(self) -> AsyncKYCChecksResourceWithRawResponse:
        return AsyncKYCChecksResourceWithRawResponse(self._customers.kyc_checks)

    @cached_property
    def kyc_documents(self) -> AsyncKYCDocumentsResourceWithRawResponse:
        return AsyncKYCDocumentsResourceWithRawResponse(self._customers.kyc_documents)

    @cached_property
    def kyc_media(self) -> AsyncKYCMediaResourceWithRawResponse:
        return AsyncKYCMediaResourceWithRawResponse(self._customers.kyc_media)

    @cached_property
    def kyc_statuses(self) -> AsyncKYCStatusesResourceWithRawResponse:
        return AsyncKYCStatusesResourceWithRawResponse(self._customers.kyc_statuses)

    @cached_property
    def mobile_number(self) -> AsyncMobileNumberResourceWithRawResponse:
        return AsyncMobileNumberResourceWithRawResponse(self._customers.mobile_number)

    @cached_property
    def number(self) -> AsyncNumberResourceWithRawResponse:
        return AsyncNumberResourceWithRawResponse(self._customers.number)

    @cached_property
    def social_media_handles(self) -> AsyncSocialMediaHandlesResourceWithRawResponse:
        return AsyncSocialMediaHandlesResourceWithRawResponse(self._customers.social_media_handles)

    @cached_property
    def tax_residences(self) -> AsyncTaxResidencesResourceWithRawResponse:
        return AsyncTaxResidencesResourceWithRawResponse(self._customers.tax_residences)

    @cached_property
    def customer_number(self) -> AsyncCustomerNumberResourceWithRawResponse:
        return AsyncCustomerNumberResourceWithRawResponse(self._customers.customer_number)

    @cached_property
    def customer_number_query(self) -> AsyncCustomerNumberQueryResourceWithRawResponse:
        return AsyncCustomerNumberQueryResourceWithRawResponse(self._customers.customer_number_query)

    @cached_property
    def accounts_minimal(self) -> AsyncAccountsMinimalResourceWithRawResponse:
        return AsyncAccountsMinimalResourceWithRawResponse(self._customers.accounts_minimal)

    @cached_property
    def cascade(self) -> AsyncCascadeResourceWithRawResponse:
        return AsyncCascadeResourceWithRawResponse(self._customers.cascade)


class CustomersResourceWithStreamingResponse:
    def __init__(self, customers: CustomersResource) -> None:
        self._customers = customers

        self.create = to_custom_streamed_response_wrapper(
            customers.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            customers.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            customers.list,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def messages(self) -> MessagesResourceWithStreamingResponse:
        return MessagesResourceWithStreamingResponse(self._customers.messages)

    @cached_property
    def minimal(self) -> MinimalResourceWithStreamingResponse:
        return MinimalResourceWithStreamingResponse(self._customers.minimal)

    @cached_property
    def addresses(self) -> AddressesResourceWithStreamingResponse:
        return AddressesResourceWithStreamingResponse(self._customers.addresses)

    @cached_property
    def attribute(self) -> AttributeResourceWithStreamingResponse:
        return AttributeResourceWithStreamingResponse(self._customers.attribute)

    @cached_property
    def attributes(self) -> AttributesResourceWithStreamingResponse:
        return AttributesResourceWithStreamingResponse(self._customers.attributes)

    @cached_property
    def branch(self) -> BranchResourceWithStreamingResponse:
        return BranchResourceWithStreamingResponse(self._customers.branch)

    @cached_property
    def correlated_users(self) -> CorrelatedUsersResourceWithStreamingResponse:
        return CorrelatedUsersResourceWithStreamingResponse(self._customers.correlated_users)

    @cached_property
    def credit_limit(self) -> CreditLimitResourceWithStreamingResponse:
        return CreditLimitResourceWithStreamingResponse(self._customers.credit_limit)

    @cached_property
    def credit_rating_and_source(self) -> CreditRatingAndSourceResourceWithStreamingResponse:
        return CreditRatingAndSourceResourceWithStreamingResponse(self._customers.credit_rating_and_source)

    @cached_property
    def customer_account_links(self) -> CustomerAccountLinksResourceWithStreamingResponse:
        return CustomerAccountLinksResourceWithStreamingResponse(self._customers.customer_account_links)

    @cached_property
    def data(self) -> DataResourceWithStreamingResponse:
        return DataResourceWithStreamingResponse(self._customers.data)

    @cached_property
    def email(self) -> EmailResourceWithStreamingResponse:
        return EmailResourceWithStreamingResponse(self._customers.email)

    @cached_property
    def identity(self) -> IdentityResourceWithStreamingResponse:
        return IdentityResourceWithStreamingResponse(self._customers.identity)

    @cached_property
    def kyc_checks(self) -> KYCChecksResourceWithStreamingResponse:
        return KYCChecksResourceWithStreamingResponse(self._customers.kyc_checks)

    @cached_property
    def kyc_documents(self) -> KYCDocumentsResourceWithStreamingResponse:
        return KYCDocumentsResourceWithStreamingResponse(self._customers.kyc_documents)

    @cached_property
    def kyc_media(self) -> KYCMediaResourceWithStreamingResponse:
        return KYCMediaResourceWithStreamingResponse(self._customers.kyc_media)

    @cached_property
    def kyc_statuses(self) -> KYCStatusesResourceWithStreamingResponse:
        return KYCStatusesResourceWithStreamingResponse(self._customers.kyc_statuses)

    @cached_property
    def mobile_number(self) -> MobileNumberResourceWithStreamingResponse:
        return MobileNumberResourceWithStreamingResponse(self._customers.mobile_number)

    @cached_property
    def number(self) -> NumberResourceWithStreamingResponse:
        return NumberResourceWithStreamingResponse(self._customers.number)

    @cached_property
    def social_media_handles(self) -> SocialMediaHandlesResourceWithStreamingResponse:
        return SocialMediaHandlesResourceWithStreamingResponse(self._customers.social_media_handles)

    @cached_property
    def tax_residences(self) -> TaxResidencesResourceWithStreamingResponse:
        return TaxResidencesResourceWithStreamingResponse(self._customers.tax_residences)

    @cached_property
    def customer_number(self) -> CustomerNumberResourceWithStreamingResponse:
        return CustomerNumberResourceWithStreamingResponse(self._customers.customer_number)

    @cached_property
    def customer_number_query(self) -> CustomerNumberQueryResourceWithStreamingResponse:
        return CustomerNumberQueryResourceWithStreamingResponse(self._customers.customer_number_query)

    @cached_property
    def accounts_minimal(self) -> AccountsMinimalResourceWithStreamingResponse:
        return AccountsMinimalResourceWithStreamingResponse(self._customers.accounts_minimal)

    @cached_property
    def cascade(self) -> CascadeResourceWithStreamingResponse:
        return CascadeResourceWithStreamingResponse(self._customers.cascade)


class AsyncCustomersResourceWithStreamingResponse:
    def __init__(self, customers: AsyncCustomersResource) -> None:
        self._customers = customers

        self.create = async_to_custom_streamed_response_wrapper(
            customers.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            customers.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            customers.list,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def messages(self) -> AsyncMessagesResourceWithStreamingResponse:
        return AsyncMessagesResourceWithStreamingResponse(self._customers.messages)

    @cached_property
    def minimal(self) -> AsyncMinimalResourceWithStreamingResponse:
        return AsyncMinimalResourceWithStreamingResponse(self._customers.minimal)

    @cached_property
    def addresses(self) -> AsyncAddressesResourceWithStreamingResponse:
        return AsyncAddressesResourceWithStreamingResponse(self._customers.addresses)

    @cached_property
    def attribute(self) -> AsyncAttributeResourceWithStreamingResponse:
        return AsyncAttributeResourceWithStreamingResponse(self._customers.attribute)

    @cached_property
    def attributes(self) -> AsyncAttributesResourceWithStreamingResponse:
        return AsyncAttributesResourceWithStreamingResponse(self._customers.attributes)

    @cached_property
    def branch(self) -> AsyncBranchResourceWithStreamingResponse:
        return AsyncBranchResourceWithStreamingResponse(self._customers.branch)

    @cached_property
    def correlated_users(self) -> AsyncCorrelatedUsersResourceWithStreamingResponse:
        return AsyncCorrelatedUsersResourceWithStreamingResponse(self._customers.correlated_users)

    @cached_property
    def credit_limit(self) -> AsyncCreditLimitResourceWithStreamingResponse:
        return AsyncCreditLimitResourceWithStreamingResponse(self._customers.credit_limit)

    @cached_property
    def credit_rating_and_source(self) -> AsyncCreditRatingAndSourceResourceWithStreamingResponse:
        return AsyncCreditRatingAndSourceResourceWithStreamingResponse(self._customers.credit_rating_and_source)

    @cached_property
    def customer_account_links(self) -> AsyncCustomerAccountLinksResourceWithStreamingResponse:
        return AsyncCustomerAccountLinksResourceWithStreamingResponse(self._customers.customer_account_links)

    @cached_property
    def data(self) -> AsyncDataResourceWithStreamingResponse:
        return AsyncDataResourceWithStreamingResponse(self._customers.data)

    @cached_property
    def email(self) -> AsyncEmailResourceWithStreamingResponse:
        return AsyncEmailResourceWithStreamingResponse(self._customers.email)

    @cached_property
    def identity(self) -> AsyncIdentityResourceWithStreamingResponse:
        return AsyncIdentityResourceWithStreamingResponse(self._customers.identity)

    @cached_property
    def kyc_checks(self) -> AsyncKYCChecksResourceWithStreamingResponse:
        return AsyncKYCChecksResourceWithStreamingResponse(self._customers.kyc_checks)

    @cached_property
    def kyc_documents(self) -> AsyncKYCDocumentsResourceWithStreamingResponse:
        return AsyncKYCDocumentsResourceWithStreamingResponse(self._customers.kyc_documents)

    @cached_property
    def kyc_media(self) -> AsyncKYCMediaResourceWithStreamingResponse:
        return AsyncKYCMediaResourceWithStreamingResponse(self._customers.kyc_media)

    @cached_property
    def kyc_statuses(self) -> AsyncKYCStatusesResourceWithStreamingResponse:
        return AsyncKYCStatusesResourceWithStreamingResponse(self._customers.kyc_statuses)

    @cached_property
    def mobile_number(self) -> AsyncMobileNumberResourceWithStreamingResponse:
        return AsyncMobileNumberResourceWithStreamingResponse(self._customers.mobile_number)

    @cached_property
    def number(self) -> AsyncNumberResourceWithStreamingResponse:
        return AsyncNumberResourceWithStreamingResponse(self._customers.number)

    @cached_property
    def social_media_handles(self) -> AsyncSocialMediaHandlesResourceWithStreamingResponse:
        return AsyncSocialMediaHandlesResourceWithStreamingResponse(self._customers.social_media_handles)

    @cached_property
    def tax_residences(self) -> AsyncTaxResidencesResourceWithStreamingResponse:
        return AsyncTaxResidencesResourceWithStreamingResponse(self._customers.tax_residences)

    @cached_property
    def customer_number(self) -> AsyncCustomerNumberResourceWithStreamingResponse:
        return AsyncCustomerNumberResourceWithStreamingResponse(self._customers.customer_number)

    @cached_property
    def customer_number_query(self) -> AsyncCustomerNumberQueryResourceWithStreamingResponse:
        return AsyncCustomerNumberQueryResourceWithStreamingResponse(self._customers.customer_number_query)

    @cached_property
    def accounts_minimal(self) -> AsyncAccountsMinimalResourceWithStreamingResponse:
        return AsyncAccountsMinimalResourceWithStreamingResponse(self._customers.accounts_minimal)

    @cached_property
    def cascade(self) -> AsyncCascadeResourceWithStreamingResponse:
        return AsyncCascadeResourceWithStreamingResponse(self._customers.cascade)
