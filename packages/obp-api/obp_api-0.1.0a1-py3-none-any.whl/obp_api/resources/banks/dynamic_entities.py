# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...types.banks import dynamic_entity_create_params, dynamic_entity_update_params
from ..._base_client import make_request_options

__all__ = ["DynamicEntitiesResource", "AsyncDynamicEntitiesResource"]


class DynamicEntitiesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DynamicEntitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return DynamicEntitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DynamicEntitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return DynamicEntitiesResourceWithStreamingResponse(self)

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
        <p>Create a Bank Level DynamicEntity.</p><p>Authentication is Mandatory</p><p>Create a DynamicEntity. If creation is successful, the corresponding POST, GET, PUT and DELETE (Create, Read, Update, Delete or CRUD for short) endpoints will be generated automatically</p><p>The following field types are as supported:<br />[number, integer, boolean, string, DATE_WITH_DAY, reference]</p><p>The DATE_WITH_DAY format is: yyyy-MM-dd</p><p>Reference types are like foreign keys and composite foreign keys are supported. The value you need to supply as the (composite) foreign key is a UUID (or several UUIDs in the case of a composite key) that match value in another Entity..<br />The following list shows all the possible reference types in the system with corresponding examples values so you can see how to construct each reference type value.</p><pre><code>&quot;someField0&quot;: {    &quot;type&quot;: &quot;reference:FishPort&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField1&quot;: {    &quot;type&quot;: &quot;reference:FooBar&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField2&quot;: {    &quot;type&quot;: &quot;reference:sustrans&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField3&quot;: {    &quot;type&quot;: &quot;reference:SimonCovid&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField4&quot;: {    &quot;type&quot;: &quot;reference:CovidAPIDays&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField5&quot;: {    &quot;type&quot;: &quot;reference:customer_cars&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField6&quot;: {    &quot;type&quot;: &quot;reference:MarchHare&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField7&quot;: {    &quot;type&quot;: &quot;reference:InsurancePolicy&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField8&quot;: {    &quot;type&quot;: &quot;reference:Odometer&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField9&quot;: {    &quot;type&quot;: &quot;reference:InsurancePremium&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField10&quot;: {    &quot;type&quot;: &quot;reference:ObpActivity&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField11&quot;: {    &quot;type&quot;: &quot;reference:test1&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField12&quot;: {    &quot;type&quot;: &quot;reference:D-Entity1&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField13&quot;: {    &quot;type&quot;: &quot;reference:test_daniel707&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField14&quot;: {    &quot;type&quot;: &quot;reference:Bank&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField15&quot;: {    &quot;type&quot;: &quot;reference:Consumer&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField16&quot;: {    &quot;type&quot;: &quot;reference:Customer&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField17&quot;: {    &quot;type&quot;: &quot;reference:MethodRouting&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField18&quot;: {    &quot;type&quot;: &quot;reference:DynamicEntity&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField19&quot;: {    &quot;type&quot;: &quot;reference:TransactionRequest&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField20&quot;: {    &quot;type&quot;: &quot;reference:ProductAttribute&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField21&quot;: {    &quot;type&quot;: &quot;reference:AccountAttribute&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField22&quot;: {    &quot;type&quot;: &quot;reference:TransactionAttribute&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField23&quot;: {    &quot;type&quot;: &quot;reference:CustomerAttribute&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField24&quot;: {    &quot;type&quot;: &quot;reference:AccountApplication&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField25&quot;: {    &quot;type&quot;: &quot;reference:CardAttribute&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField26&quot;: {    &quot;type&quot;: &quot;reference:Counterparty&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField27&quot;: {    &quot;type&quot;: &quot;reference:Branch:bankId&amp;branchId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;branchId=1660ed49-5956-47a1-a352-4f9b388a9586&quot;}&quot;someField28&quot;: {    &quot;type&quot;: &quot;reference:Atm:bankId&amp;atmId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;atmId=1660ed49-5956-47a1-a352-4f9b388a9586&quot;}&quot;someField29&quot;: {    &quot;type&quot;: &quot;reference:BankAccount:bankId&amp;accountId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;accountId=1660ed49-5956-47a1-a352-4f9b388a9586&quot;}&quot;someField30&quot;: {    &quot;type&quot;: &quot;reference:Product:bankId&amp;productCode&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;productCode=1660ed49-5956-47a1-a352-4f9b388a9586&quot;}&quot;someField31&quot;: {    &quot;type&quot;: &quot;reference:PhysicalCard:bankId&amp;cardId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;cardId=1660ed49-5956-47a1-a352-4f9b388a9586&quot;}&quot;someField32&quot;: {    &quot;type&quot;: &quot;reference:Transaction:bankId&amp;accountId&amp;transactionId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;accountId=1660ed49-5956-47a1-a352-4f9b388a9586&amp;transactionId=89619144-70d8-4b26-9fcb-45ada8dd1cad&quot;}&quot;someField33&quot;: {    &quot;type&quot;: &quot;reference:Counterparty:bankId&amp;accountId&amp;counterpartyId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;accountId=1660ed49-5956-47a1-a352-4f9b388a9586&amp;counterpartyId=89619144-70d8-4b26-9fcb-45ada8dd1cad&quot;}</code></pre><p>Note: if you set <code>hasPersonalEntity</code> = false, then OBP will not generate the CRUD my FooBar endpoints.</p>

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
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-entities",
            body=maybe_transform(body, dynamic_entity_create_params.DynamicEntityCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        dynamic_entity_id: str,
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
        <p>Update a Bank Level DynamicEntity.</p><p>Authentication is Mandatory</p><p>Update one DynamicEntity, after update finished, the corresponding CRUD endpoints will be changed.</p><p>The following field types are as supported:<br />[number, integer, boolean, string, DATE_WITH_DAY, reference]</p><p>DATE_WITH_DAY format: yyyy-MM-dd</p><p>Reference types are like foreign keys and composite foreign keys are supported. The value you need to supply as the (composite) foreign key is a UUID (or several UUIDs in the case of a composite key) that match value in another Entity..<br />The following list shows all the possible reference types in the system with corresponding examples values so you can see how to construct each reference type value.</p><pre><code>&quot;someField0&quot;: {    &quot;type&quot;: &quot;reference:FishPort&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField1&quot;: {    &quot;type&quot;: &quot;reference:FooBar&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField2&quot;: {    &quot;type&quot;: &quot;reference:sustrans&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField3&quot;: {    &quot;type&quot;: &quot;reference:SimonCovid&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField4&quot;: {    &quot;type&quot;: &quot;reference:CovidAPIDays&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField5&quot;: {    &quot;type&quot;: &quot;reference:customer_cars&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField6&quot;: {    &quot;type&quot;: &quot;reference:MarchHare&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField7&quot;: {    &quot;type&quot;: &quot;reference:InsurancePolicy&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField8&quot;: {    &quot;type&quot;: &quot;reference:Odometer&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField9&quot;: {    &quot;type&quot;: &quot;reference:InsurancePremium&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField10&quot;: {    &quot;type&quot;: &quot;reference:ObpActivity&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField11&quot;: {    &quot;type&quot;: &quot;reference:test1&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField12&quot;: {    &quot;type&quot;: &quot;reference:D-Entity1&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField13&quot;: {    &quot;type&quot;: &quot;reference:test_daniel707&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField14&quot;: {    &quot;type&quot;: &quot;reference:Bank&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField15&quot;: {    &quot;type&quot;: &quot;reference:Consumer&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField16&quot;: {    &quot;type&quot;: &quot;reference:Customer&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField17&quot;: {    &quot;type&quot;: &quot;reference:MethodRouting&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField18&quot;: {    &quot;type&quot;: &quot;reference:DynamicEntity&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField19&quot;: {    &quot;type&quot;: &quot;reference:TransactionRequest&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField20&quot;: {    &quot;type&quot;: &quot;reference:ProductAttribute&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField21&quot;: {    &quot;type&quot;: &quot;reference:AccountAttribute&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField22&quot;: {    &quot;type&quot;: &quot;reference:TransactionAttribute&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField23&quot;: {    &quot;type&quot;: &quot;reference:CustomerAttribute&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField24&quot;: {    &quot;type&quot;: &quot;reference:AccountApplication&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField25&quot;: {    &quot;type&quot;: &quot;reference:CardAttribute&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField26&quot;: {    &quot;type&quot;: &quot;reference:Counterparty&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField27&quot;: {    &quot;type&quot;: &quot;reference:Branch:bankId&amp;branchId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;branchId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&quot;}&quot;someField28&quot;: {    &quot;type&quot;: &quot;reference:Atm:bankId&amp;atmId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;atmId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&quot;}&quot;someField29&quot;: {    &quot;type&quot;: &quot;reference:BankAccount:bankId&amp;accountId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;accountId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&quot;}&quot;someField30&quot;: {    &quot;type&quot;: &quot;reference:Product:bankId&amp;productCode&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;productCode=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&quot;}&quot;someField31&quot;: {    &quot;type&quot;: &quot;reference:PhysicalCard:bankId&amp;cardId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;cardId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&quot;}&quot;someField32&quot;: {    &quot;type&quot;: &quot;reference:Transaction:bankId&amp;accountId&amp;transactionId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;accountId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&amp;transactionId=c169e030-f530-4540-a637-90816578686e&quot;}&quot;someField33&quot;: {    &quot;type&quot;: &quot;reference:Counterparty:bankId&amp;accountId&amp;counterpartyId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;accountId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&amp;counterpartyId=c169e030-f530-4540-a637-90816578686e&quot;}</code></pre>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not dynamic_entity_id:
            raise ValueError(f"Expected a non-empty value for `dynamic_entity_id` but received {dynamic_entity_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-entities/{dynamic_entity_id}",
            body=maybe_transform(body, dynamic_entity_update_params.DynamicEntityUpdateParams),
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
        <p>Get all the bank level Dynamic Entities for one bank.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-entities",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        dynamic_entity_id: str,
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
        <p>Delete a Bank Level DynamicEntity specified by DYNAMIC_ENTITY_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not dynamic_entity_id:
            raise ValueError(f"Expected a non-empty value for `dynamic_entity_id` but received {dynamic_entity_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-entities/{dynamic_entity_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncDynamicEntitiesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDynamicEntitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDynamicEntitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDynamicEntitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncDynamicEntitiesResourceWithStreamingResponse(self)

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
        <p>Create a Bank Level DynamicEntity.</p><p>Authentication is Mandatory</p><p>Create a DynamicEntity. If creation is successful, the corresponding POST, GET, PUT and DELETE (Create, Read, Update, Delete or CRUD for short) endpoints will be generated automatically</p><p>The following field types are as supported:<br />[number, integer, boolean, string, DATE_WITH_DAY, reference]</p><p>The DATE_WITH_DAY format is: yyyy-MM-dd</p><p>Reference types are like foreign keys and composite foreign keys are supported. The value you need to supply as the (composite) foreign key is a UUID (or several UUIDs in the case of a composite key) that match value in another Entity..<br />The following list shows all the possible reference types in the system with corresponding examples values so you can see how to construct each reference type value.</p><pre><code>&quot;someField0&quot;: {    &quot;type&quot;: &quot;reference:FishPort&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField1&quot;: {    &quot;type&quot;: &quot;reference:FooBar&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField2&quot;: {    &quot;type&quot;: &quot;reference:sustrans&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField3&quot;: {    &quot;type&quot;: &quot;reference:SimonCovid&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField4&quot;: {    &quot;type&quot;: &quot;reference:CovidAPIDays&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField5&quot;: {    &quot;type&quot;: &quot;reference:customer_cars&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField6&quot;: {    &quot;type&quot;: &quot;reference:MarchHare&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField7&quot;: {    &quot;type&quot;: &quot;reference:InsurancePolicy&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField8&quot;: {    &quot;type&quot;: &quot;reference:Odometer&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField9&quot;: {    &quot;type&quot;: &quot;reference:InsurancePremium&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField10&quot;: {    &quot;type&quot;: &quot;reference:ObpActivity&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField11&quot;: {    &quot;type&quot;: &quot;reference:test1&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField12&quot;: {    &quot;type&quot;: &quot;reference:D-Entity1&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField13&quot;: {    &quot;type&quot;: &quot;reference:test_daniel707&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField14&quot;: {    &quot;type&quot;: &quot;reference:Bank&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField15&quot;: {    &quot;type&quot;: &quot;reference:Consumer&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField16&quot;: {    &quot;type&quot;: &quot;reference:Customer&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField17&quot;: {    &quot;type&quot;: &quot;reference:MethodRouting&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField18&quot;: {    &quot;type&quot;: &quot;reference:DynamicEntity&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField19&quot;: {    &quot;type&quot;: &quot;reference:TransactionRequest&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField20&quot;: {    &quot;type&quot;: &quot;reference:ProductAttribute&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField21&quot;: {    &quot;type&quot;: &quot;reference:AccountAttribute&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField22&quot;: {    &quot;type&quot;: &quot;reference:TransactionAttribute&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField23&quot;: {    &quot;type&quot;: &quot;reference:CustomerAttribute&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField24&quot;: {    &quot;type&quot;: &quot;reference:AccountApplication&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField25&quot;: {    &quot;type&quot;: &quot;reference:CardAttribute&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField26&quot;: {    &quot;type&quot;: &quot;reference:Counterparty&quot;,    &quot;example&quot;: &quot;3c930951-498f-4634-9396-a4c1cc0828d3&quot;}&quot;someField27&quot;: {    &quot;type&quot;: &quot;reference:Branch:bankId&amp;branchId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;branchId=1660ed49-5956-47a1-a352-4f9b388a9586&quot;}&quot;someField28&quot;: {    &quot;type&quot;: &quot;reference:Atm:bankId&amp;atmId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;atmId=1660ed49-5956-47a1-a352-4f9b388a9586&quot;}&quot;someField29&quot;: {    &quot;type&quot;: &quot;reference:BankAccount:bankId&amp;accountId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;accountId=1660ed49-5956-47a1-a352-4f9b388a9586&quot;}&quot;someField30&quot;: {    &quot;type&quot;: &quot;reference:Product:bankId&amp;productCode&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;productCode=1660ed49-5956-47a1-a352-4f9b388a9586&quot;}&quot;someField31&quot;: {    &quot;type&quot;: &quot;reference:PhysicalCard:bankId&amp;cardId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;cardId=1660ed49-5956-47a1-a352-4f9b388a9586&quot;}&quot;someField32&quot;: {    &quot;type&quot;: &quot;reference:Transaction:bankId&amp;accountId&amp;transactionId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;accountId=1660ed49-5956-47a1-a352-4f9b388a9586&amp;transactionId=89619144-70d8-4b26-9fcb-45ada8dd1cad&quot;}&quot;someField33&quot;: {    &quot;type&quot;: &quot;reference:Counterparty:bankId&amp;accountId&amp;counterpartyId&quot;,    &quot;example&quot;: &quot;bankId=3c930951-498f-4634-9396-a4c1cc0828d3&amp;accountId=1660ed49-5956-47a1-a352-4f9b388a9586&amp;counterpartyId=89619144-70d8-4b26-9fcb-45ada8dd1cad&quot;}</code></pre><p>Note: if you set <code>hasPersonalEntity</code> = false, then OBP will not generate the CRUD my FooBar endpoints.</p>

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
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-entities",
            body=await async_maybe_transform(body, dynamic_entity_create_params.DynamicEntityCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        dynamic_entity_id: str,
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
        <p>Update a Bank Level DynamicEntity.</p><p>Authentication is Mandatory</p><p>Update one DynamicEntity, after update finished, the corresponding CRUD endpoints will be changed.</p><p>The following field types are as supported:<br />[number, integer, boolean, string, DATE_WITH_DAY, reference]</p><p>DATE_WITH_DAY format: yyyy-MM-dd</p><p>Reference types are like foreign keys and composite foreign keys are supported. The value you need to supply as the (composite) foreign key is a UUID (or several UUIDs in the case of a composite key) that match value in another Entity..<br />The following list shows all the possible reference types in the system with corresponding examples values so you can see how to construct each reference type value.</p><pre><code>&quot;someField0&quot;: {    &quot;type&quot;: &quot;reference:FishPort&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField1&quot;: {    &quot;type&quot;: &quot;reference:FooBar&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField2&quot;: {    &quot;type&quot;: &quot;reference:sustrans&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField3&quot;: {    &quot;type&quot;: &quot;reference:SimonCovid&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField4&quot;: {    &quot;type&quot;: &quot;reference:CovidAPIDays&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField5&quot;: {    &quot;type&quot;: &quot;reference:customer_cars&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField6&quot;: {    &quot;type&quot;: &quot;reference:MarchHare&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField7&quot;: {    &quot;type&quot;: &quot;reference:InsurancePolicy&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField8&quot;: {    &quot;type&quot;: &quot;reference:Odometer&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField9&quot;: {    &quot;type&quot;: &quot;reference:InsurancePremium&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField10&quot;: {    &quot;type&quot;: &quot;reference:ObpActivity&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField11&quot;: {    &quot;type&quot;: &quot;reference:test1&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField12&quot;: {    &quot;type&quot;: &quot;reference:D-Entity1&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField13&quot;: {    &quot;type&quot;: &quot;reference:test_daniel707&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField14&quot;: {    &quot;type&quot;: &quot;reference:Bank&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField15&quot;: {    &quot;type&quot;: &quot;reference:Consumer&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField16&quot;: {    &quot;type&quot;: &quot;reference:Customer&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField17&quot;: {    &quot;type&quot;: &quot;reference:MethodRouting&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField18&quot;: {    &quot;type&quot;: &quot;reference:DynamicEntity&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField19&quot;: {    &quot;type&quot;: &quot;reference:TransactionRequest&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField20&quot;: {    &quot;type&quot;: &quot;reference:ProductAttribute&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField21&quot;: {    &quot;type&quot;: &quot;reference:AccountAttribute&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField22&quot;: {    &quot;type&quot;: &quot;reference:TransactionAttribute&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField23&quot;: {    &quot;type&quot;: &quot;reference:CustomerAttribute&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField24&quot;: {    &quot;type&quot;: &quot;reference:AccountApplication&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField25&quot;: {    &quot;type&quot;: &quot;reference:CardAttribute&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField26&quot;: {    &quot;type&quot;: &quot;reference:Counterparty&quot;,    &quot;example&quot;: &quot;746b4e77-dc72-4853-ac0f-8866e5cdea4a&quot;}&quot;someField27&quot;: {    &quot;type&quot;: &quot;reference:Branch:bankId&amp;branchId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;branchId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&quot;}&quot;someField28&quot;: {    &quot;type&quot;: &quot;reference:Atm:bankId&amp;atmId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;atmId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&quot;}&quot;someField29&quot;: {    &quot;type&quot;: &quot;reference:BankAccount:bankId&amp;accountId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;accountId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&quot;}&quot;someField30&quot;: {    &quot;type&quot;: &quot;reference:Product:bankId&amp;productCode&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;productCode=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&quot;}&quot;someField31&quot;: {    &quot;type&quot;: &quot;reference:PhysicalCard:bankId&amp;cardId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;cardId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&quot;}&quot;someField32&quot;: {    &quot;type&quot;: &quot;reference:Transaction:bankId&amp;accountId&amp;transactionId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;accountId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&amp;transactionId=c169e030-f530-4540-a637-90816578686e&quot;}&quot;someField33&quot;: {    &quot;type&quot;: &quot;reference:Counterparty:bankId&amp;accountId&amp;counterpartyId&quot;,    &quot;example&quot;: &quot;bankId=746b4e77-dc72-4853-ac0f-8866e5cdea4a&amp;accountId=cee45f24-13d9-41e5-81ea-1075dfe2b0f8&amp;counterpartyId=c169e030-f530-4540-a637-90816578686e&quot;}</code></pre>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not dynamic_entity_id:
            raise ValueError(f"Expected a non-empty value for `dynamic_entity_id` but received {dynamic_entity_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-entities/{dynamic_entity_id}",
            body=await async_maybe_transform(body, dynamic_entity_update_params.DynamicEntityUpdateParams),
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
        <p>Get all the bank level Dynamic Entities for one bank.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-entities",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        dynamic_entity_id: str,
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
        <p>Delete a Bank Level DynamicEntity specified by DYNAMIC_ENTITY_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not dynamic_entity_id:
            raise ValueError(f"Expected a non-empty value for `dynamic_entity_id` but received {dynamic_entity_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/management/banks/{bank_id}/dynamic-entities/{dynamic_entity_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class DynamicEntitiesResourceWithRawResponse:
    def __init__(self, dynamic_entities: DynamicEntitiesResource) -> None:
        self._dynamic_entities = dynamic_entities

        self.create = to_custom_raw_response_wrapper(
            dynamic_entities.create,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            dynamic_entities.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            dynamic_entities.list,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            dynamic_entities.delete,
        )


class AsyncDynamicEntitiesResourceWithRawResponse:
    def __init__(self, dynamic_entities: AsyncDynamicEntitiesResource) -> None:
        self._dynamic_entities = dynamic_entities

        self.create = async_to_custom_raw_response_wrapper(
            dynamic_entities.create,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            dynamic_entities.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            dynamic_entities.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            dynamic_entities.delete,
        )


class DynamicEntitiesResourceWithStreamingResponse:
    def __init__(self, dynamic_entities: DynamicEntitiesResource) -> None:
        self._dynamic_entities = dynamic_entities

        self.create = to_custom_streamed_response_wrapper(
            dynamic_entities.create,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            dynamic_entities.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            dynamic_entities.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            dynamic_entities.delete,
        )


class AsyncDynamicEntitiesResourceWithStreamingResponse:
    def __init__(self, dynamic_entities: AsyncDynamicEntitiesResource) -> None:
        self._dynamic_entities = dynamic_entities

        self.create = async_to_custom_streamed_response_wrapper(
            dynamic_entities.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            dynamic_entities.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            dynamic_entities.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            dynamic_entities.delete,
        )
