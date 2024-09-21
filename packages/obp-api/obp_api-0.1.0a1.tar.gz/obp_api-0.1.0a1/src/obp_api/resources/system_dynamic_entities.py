# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import system_dynamic_entity_create_params, system_dynamic_entity_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
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
from .._base_client import make_request_options

__all__ = ["SystemDynamicEntitiesResource", "AsyncSystemDynamicEntitiesResource"]


class SystemDynamicEntitiesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SystemDynamicEntitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return SystemDynamicEntitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SystemDynamicEntitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return SystemDynamicEntitiesResourceWithStreamingResponse(self)

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
        <p>Create a system level Dynamic Entity.</p><p>Authentication is Mandatory</p><p>Create a DynamicEntity. If creation is successful, the corresponding POST, GET, PUT and DELETE (Create, Read, Update, Delete or CRUD for short) endpoints will be generated automatically</p><p>The following field types are as supported:<br />[number, integer, boolean, string, DATE_WITH_DAY, reference]</p><p>The DATE_WITH_DAY format is: yyyy-MM-dd</p><p>Reference types are like foreign keys and composite foreign keys are supported. The value you need to supply as the (composite) foreign key is a UUID (or several UUIDs in the case of a composite key) that match value in another Entity..<br />See the following list of currently available reference types and examples of how to construct key values correctly. Note: As more Dynamic Entities are created on this instance, this list will grow:</p><pre><code>&quot;someField0&quot;: {    &quot;type&quot;: &quot;reference:FishPort&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField1&quot;: {    &quot;type&quot;: &quot;reference:FooBar&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField2&quot;: {    &quot;type&quot;: &quot;reference:sustrans&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField3&quot;: {    &quot;type&quot;: &quot;reference:SimonCovid&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField4&quot;: {    &quot;type&quot;: &quot;reference:CovidAPIDays&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField5&quot;: {    &quot;type&quot;: &quot;reference:customer_cars&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField6&quot;: {    &quot;type&quot;: &quot;reference:MarchHare&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField7&quot;: {    &quot;type&quot;: &quot;reference:InsurancePolicy&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField8&quot;: {    &quot;type&quot;: &quot;reference:Odometer&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField9&quot;: {    &quot;type&quot;: &quot;reference:InsurancePremium&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField10&quot;: {    &quot;type&quot;: &quot;reference:ObpActivity&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField11&quot;: {    &quot;type&quot;: &quot;reference:test1&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField12&quot;: {    &quot;type&quot;: &quot;reference:D-Entity1&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField13&quot;: {    &quot;type&quot;: &quot;reference:test_daniel707&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField14&quot;: {    &quot;type&quot;: &quot;reference:Bank&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField15&quot;: {    &quot;type&quot;: &quot;reference:Consumer&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField16&quot;: {    &quot;type&quot;: &quot;reference:Customer&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField17&quot;: {    &quot;type&quot;: &quot;reference:MethodRouting&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField18&quot;: {    &quot;type&quot;: &quot;reference:DynamicEntity&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField19&quot;: {    &quot;type&quot;: &quot;reference:TransactionRequest&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField20&quot;: {    &quot;type&quot;: &quot;reference:ProductAttribute&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField21&quot;: {    &quot;type&quot;: &quot;reference:AccountAttribute&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField22&quot;: {    &quot;type&quot;: &quot;reference:TransactionAttribute&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField23&quot;: {    &quot;type&quot;: &quot;reference:CustomerAttribute&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField24&quot;: {    &quot;type&quot;: &quot;reference:AccountApplication&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField25&quot;: {    &quot;type&quot;: &quot;reference:CardAttribute&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField26&quot;: {    &quot;type&quot;: &quot;reference:Counterparty&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField27&quot;: {    &quot;type&quot;: &quot;reference:Branch:bankId&amp;branchId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;branchId=9d911282-6609-4e0a-9982-ed24f02ea9f7&quot;}&quot;someField28&quot;: {    &quot;type&quot;: &quot;reference:Atm:bankId&amp;atmId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;atmId=9d911282-6609-4e0a-9982-ed24f02ea9f7&quot;}&quot;someField29&quot;: {    &quot;type&quot;: &quot;reference:BankAccount:bankId&amp;accountId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;accountId=9d911282-6609-4e0a-9982-ed24f02ea9f7&quot;}&quot;someField30&quot;: {    &quot;type&quot;: &quot;reference:Product:bankId&amp;productCode&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;productCode=9d911282-6609-4e0a-9982-ed24f02ea9f7&quot;}&quot;someField31&quot;: {    &quot;type&quot;: &quot;reference:PhysicalCard:bankId&amp;cardId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;cardId=9d911282-6609-4e0a-9982-ed24f02ea9f7&quot;}&quot;someField32&quot;: {    &quot;type&quot;: &quot;reference:Transaction:bankId&amp;accountId&amp;transactionId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;accountId=9d911282-6609-4e0a-9982-ed24f02ea9f7&amp;transactionId=e305cdf4-b9ad-4f53-b9a0-7ff65114a087&quot;}&quot;someField33&quot;: {    &quot;type&quot;: &quot;reference:Counterparty:bankId&amp;accountId&amp;counterpartyId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;accountId=9d911282-6609-4e0a-9982-ed24f02ea9f7&amp;counterpartyId=e305cdf4-b9ad-4f53-b9a0-7ff65114a087&quot;}</code></pre><p>Note: if you set <code>hasPersonalEntity</code> = false, then OBP will not generate the CRUD my FooBar endpoints.</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/obp/v5.1.0/management/system-dynamic-entities",
            body=maybe_transform(body, system_dynamic_entity_create_params.SystemDynamicEntityCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def update(
        self,
        dynamic_entity_id: str,
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
        <p>Update a System Level Dynamic Entity.</p><p>Authentication is Mandatory</p><p>Update one DynamicEntity, after update finished, the corresponding CRUD endpoints will be changed.</p><p>The following field types are as supported:<br />[number, integer, boolean, string, DATE_WITH_DAY, reference]</p><p>DATE_WITH_DAY format: yyyy-MM-dd</p><p>Reference types are like foreign keys and composite foreign keys are supported. The value you need to supply as the (composite) foreign key is a UUID (or several UUIDs in the case of a composite key) that match value in another Entity..<br />The following list shows all the possible reference types in the system with corresponding examples values so you can see how to construct each reference type value.</p><pre><code>&quot;someField0&quot;: {    &quot;type&quot;: &quot;reference:FishPort&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField1&quot;: {    &quot;type&quot;: &quot;reference:FooBar&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField2&quot;: {    &quot;type&quot;: &quot;reference:sustrans&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField3&quot;: {    &quot;type&quot;: &quot;reference:SimonCovid&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField4&quot;: {    &quot;type&quot;: &quot;reference:CovidAPIDays&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField5&quot;: {    &quot;type&quot;: &quot;reference:customer_cars&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField6&quot;: {    &quot;type&quot;: &quot;reference:MarchHare&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField7&quot;: {    &quot;type&quot;: &quot;reference:InsurancePolicy&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField8&quot;: {    &quot;type&quot;: &quot;reference:Odometer&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField9&quot;: {    &quot;type&quot;: &quot;reference:InsurancePremium&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField10&quot;: {    &quot;type&quot;: &quot;reference:ObpActivity&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField11&quot;: {    &quot;type&quot;: &quot;reference:test1&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField12&quot;: {    &quot;type&quot;: &quot;reference:D-Entity1&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField13&quot;: {    &quot;type&quot;: &quot;reference:test_daniel707&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField14&quot;: {    &quot;type&quot;: &quot;reference:Bank&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField15&quot;: {    &quot;type&quot;: &quot;reference:Consumer&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField16&quot;: {    &quot;type&quot;: &quot;reference:Customer&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField17&quot;: {    &quot;type&quot;: &quot;reference:MethodRouting&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField18&quot;: {    &quot;type&quot;: &quot;reference:DynamicEntity&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField19&quot;: {    &quot;type&quot;: &quot;reference:TransactionRequest&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField20&quot;: {    &quot;type&quot;: &quot;reference:ProductAttribute&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField21&quot;: {    &quot;type&quot;: &quot;reference:AccountAttribute&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField22&quot;: {    &quot;type&quot;: &quot;reference:TransactionAttribute&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField23&quot;: {    &quot;type&quot;: &quot;reference:CustomerAttribute&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField24&quot;: {    &quot;type&quot;: &quot;reference:AccountApplication&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField25&quot;: {    &quot;type&quot;: &quot;reference:CardAttribute&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField26&quot;: {    &quot;type&quot;: &quot;reference:Counterparty&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField27&quot;: {    &quot;type&quot;: &quot;reference:Branch:bankId&amp;branchId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;branchId=399c2edf-4c5f-4a35-930f-b8f28074e775&quot;}&quot;someField28&quot;: {    &quot;type&quot;: &quot;reference:Atm:bankId&amp;atmId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;atmId=399c2edf-4c5f-4a35-930f-b8f28074e775&quot;}&quot;someField29&quot;: {    &quot;type&quot;: &quot;reference:BankAccount:bankId&amp;accountId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;accountId=399c2edf-4c5f-4a35-930f-b8f28074e775&quot;}&quot;someField30&quot;: {    &quot;type&quot;: &quot;reference:Product:bankId&amp;productCode&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;productCode=399c2edf-4c5f-4a35-930f-b8f28074e775&quot;}&quot;someField31&quot;: {    &quot;type&quot;: &quot;reference:PhysicalCard:bankId&amp;cardId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;cardId=399c2edf-4c5f-4a35-930f-b8f28074e775&quot;}&quot;someField32&quot;: {    &quot;type&quot;: &quot;reference:Transaction:bankId&amp;accountId&amp;transactionId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;accountId=399c2edf-4c5f-4a35-930f-b8f28074e775&amp;transactionId=68876319-84ce-4c58-8ec9-470494cd5ddd&quot;}&quot;someField33&quot;: {    &quot;type&quot;: &quot;reference:Counterparty:bankId&amp;accountId&amp;counterpartyId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;accountId=399c2edf-4c5f-4a35-930f-b8f28074e775&amp;counterpartyId=68876319-84ce-4c58-8ec9-470494cd5ddd&quot;}</code></pre>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dynamic_entity_id:
            raise ValueError(f"Expected a non-empty value for `dynamic_entity_id` but received {dynamic_entity_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/management/system-dynamic-entities/{dynamic_entity_id}",
            body=maybe_transform(body, system_dynamic_entity_update_params.SystemDynamicEntityUpdateParams),
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
        """<p>Get all System Dynamic Entities</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/management/system-dynamic-entities",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        dynamic_entity_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete a DynamicEntity specified by DYNAMIC_ENTITY_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dynamic_entity_id:
            raise ValueError(f"Expected a non-empty value for `dynamic_entity_id` but received {dynamic_entity_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/management/system-dynamic-entities/{dynamic_entity_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncSystemDynamicEntitiesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSystemDynamicEntitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSystemDynamicEntitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSystemDynamicEntitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncSystemDynamicEntitiesResourceWithStreamingResponse(self)

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
        <p>Create a system level Dynamic Entity.</p><p>Authentication is Mandatory</p><p>Create a DynamicEntity. If creation is successful, the corresponding POST, GET, PUT and DELETE (Create, Read, Update, Delete or CRUD for short) endpoints will be generated automatically</p><p>The following field types are as supported:<br />[number, integer, boolean, string, DATE_WITH_DAY, reference]</p><p>The DATE_WITH_DAY format is: yyyy-MM-dd</p><p>Reference types are like foreign keys and composite foreign keys are supported. The value you need to supply as the (composite) foreign key is a UUID (or several UUIDs in the case of a composite key) that match value in another Entity..<br />See the following list of currently available reference types and examples of how to construct key values correctly. Note: As more Dynamic Entities are created on this instance, this list will grow:</p><pre><code>&quot;someField0&quot;: {    &quot;type&quot;: &quot;reference:FishPort&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField1&quot;: {    &quot;type&quot;: &quot;reference:FooBar&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField2&quot;: {    &quot;type&quot;: &quot;reference:sustrans&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField3&quot;: {    &quot;type&quot;: &quot;reference:SimonCovid&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField4&quot;: {    &quot;type&quot;: &quot;reference:CovidAPIDays&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField5&quot;: {    &quot;type&quot;: &quot;reference:customer_cars&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField6&quot;: {    &quot;type&quot;: &quot;reference:MarchHare&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField7&quot;: {    &quot;type&quot;: &quot;reference:InsurancePolicy&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField8&quot;: {    &quot;type&quot;: &quot;reference:Odometer&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField9&quot;: {    &quot;type&quot;: &quot;reference:InsurancePremium&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField10&quot;: {    &quot;type&quot;: &quot;reference:ObpActivity&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField11&quot;: {    &quot;type&quot;: &quot;reference:test1&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField12&quot;: {    &quot;type&quot;: &quot;reference:D-Entity1&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField13&quot;: {    &quot;type&quot;: &quot;reference:test_daniel707&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField14&quot;: {    &quot;type&quot;: &quot;reference:Bank&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField15&quot;: {    &quot;type&quot;: &quot;reference:Consumer&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField16&quot;: {    &quot;type&quot;: &quot;reference:Customer&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField17&quot;: {    &quot;type&quot;: &quot;reference:MethodRouting&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField18&quot;: {    &quot;type&quot;: &quot;reference:DynamicEntity&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField19&quot;: {    &quot;type&quot;: &quot;reference:TransactionRequest&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField20&quot;: {    &quot;type&quot;: &quot;reference:ProductAttribute&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField21&quot;: {    &quot;type&quot;: &quot;reference:AccountAttribute&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField22&quot;: {    &quot;type&quot;: &quot;reference:TransactionAttribute&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField23&quot;: {    &quot;type&quot;: &quot;reference:CustomerAttribute&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField24&quot;: {    &quot;type&quot;: &quot;reference:AccountApplication&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField25&quot;: {    &quot;type&quot;: &quot;reference:CardAttribute&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField26&quot;: {    &quot;type&quot;: &quot;reference:Counterparty&quot;,    &quot;example&quot;: &quot;67947b30-abf6-4f50-a9ef-c479d52f143a&quot;}&quot;someField27&quot;: {    &quot;type&quot;: &quot;reference:Branch:bankId&amp;branchId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;branchId=9d911282-6609-4e0a-9982-ed24f02ea9f7&quot;}&quot;someField28&quot;: {    &quot;type&quot;: &quot;reference:Atm:bankId&amp;atmId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;atmId=9d911282-6609-4e0a-9982-ed24f02ea9f7&quot;}&quot;someField29&quot;: {    &quot;type&quot;: &quot;reference:BankAccount:bankId&amp;accountId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;accountId=9d911282-6609-4e0a-9982-ed24f02ea9f7&quot;}&quot;someField30&quot;: {    &quot;type&quot;: &quot;reference:Product:bankId&amp;productCode&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;productCode=9d911282-6609-4e0a-9982-ed24f02ea9f7&quot;}&quot;someField31&quot;: {    &quot;type&quot;: &quot;reference:PhysicalCard:bankId&amp;cardId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;cardId=9d911282-6609-4e0a-9982-ed24f02ea9f7&quot;}&quot;someField32&quot;: {    &quot;type&quot;: &quot;reference:Transaction:bankId&amp;accountId&amp;transactionId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;accountId=9d911282-6609-4e0a-9982-ed24f02ea9f7&amp;transactionId=e305cdf4-b9ad-4f53-b9a0-7ff65114a087&quot;}&quot;someField33&quot;: {    &quot;type&quot;: &quot;reference:Counterparty:bankId&amp;accountId&amp;counterpartyId&quot;,    &quot;example&quot;: &quot;bankId=67947b30-abf6-4f50-a9ef-c479d52f143a&amp;accountId=9d911282-6609-4e0a-9982-ed24f02ea9f7&amp;counterpartyId=e305cdf4-b9ad-4f53-b9a0-7ff65114a087&quot;}</code></pre><p>Note: if you set <code>hasPersonalEntity</code> = false, then OBP will not generate the CRUD my FooBar endpoints.</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/obp/v5.1.0/management/system-dynamic-entities",
            body=await async_maybe_transform(body, system_dynamic_entity_create_params.SystemDynamicEntityCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def update(
        self,
        dynamic_entity_id: str,
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
        <p>Update a System Level Dynamic Entity.</p><p>Authentication is Mandatory</p><p>Update one DynamicEntity, after update finished, the corresponding CRUD endpoints will be changed.</p><p>The following field types are as supported:<br />[number, integer, boolean, string, DATE_WITH_DAY, reference]</p><p>DATE_WITH_DAY format: yyyy-MM-dd</p><p>Reference types are like foreign keys and composite foreign keys are supported. The value you need to supply as the (composite) foreign key is a UUID (or several UUIDs in the case of a composite key) that match value in another Entity..<br />The following list shows all the possible reference types in the system with corresponding examples values so you can see how to construct each reference type value.</p><pre><code>&quot;someField0&quot;: {    &quot;type&quot;: &quot;reference:FishPort&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField1&quot;: {    &quot;type&quot;: &quot;reference:FooBar&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField2&quot;: {    &quot;type&quot;: &quot;reference:sustrans&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField3&quot;: {    &quot;type&quot;: &quot;reference:SimonCovid&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField4&quot;: {    &quot;type&quot;: &quot;reference:CovidAPIDays&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField5&quot;: {    &quot;type&quot;: &quot;reference:customer_cars&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField6&quot;: {    &quot;type&quot;: &quot;reference:MarchHare&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField7&quot;: {    &quot;type&quot;: &quot;reference:InsurancePolicy&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField8&quot;: {    &quot;type&quot;: &quot;reference:Odometer&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField9&quot;: {    &quot;type&quot;: &quot;reference:InsurancePremium&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField10&quot;: {    &quot;type&quot;: &quot;reference:ObpActivity&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField11&quot;: {    &quot;type&quot;: &quot;reference:test1&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField12&quot;: {    &quot;type&quot;: &quot;reference:D-Entity1&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField13&quot;: {    &quot;type&quot;: &quot;reference:test_daniel707&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField14&quot;: {    &quot;type&quot;: &quot;reference:Bank&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField15&quot;: {    &quot;type&quot;: &quot;reference:Consumer&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField16&quot;: {    &quot;type&quot;: &quot;reference:Customer&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField17&quot;: {    &quot;type&quot;: &quot;reference:MethodRouting&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField18&quot;: {    &quot;type&quot;: &quot;reference:DynamicEntity&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField19&quot;: {    &quot;type&quot;: &quot;reference:TransactionRequest&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField20&quot;: {    &quot;type&quot;: &quot;reference:ProductAttribute&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField21&quot;: {    &quot;type&quot;: &quot;reference:AccountAttribute&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField22&quot;: {    &quot;type&quot;: &quot;reference:TransactionAttribute&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField23&quot;: {    &quot;type&quot;: &quot;reference:CustomerAttribute&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField24&quot;: {    &quot;type&quot;: &quot;reference:AccountApplication&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField25&quot;: {    &quot;type&quot;: &quot;reference:CardAttribute&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField26&quot;: {    &quot;type&quot;: &quot;reference:Counterparty&quot;,    &quot;example&quot;: &quot;be7fb82c-eddd-4840-a03b-8b851fc6eedc&quot;}&quot;someField27&quot;: {    &quot;type&quot;: &quot;reference:Branch:bankId&amp;branchId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;branchId=399c2edf-4c5f-4a35-930f-b8f28074e775&quot;}&quot;someField28&quot;: {    &quot;type&quot;: &quot;reference:Atm:bankId&amp;atmId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;atmId=399c2edf-4c5f-4a35-930f-b8f28074e775&quot;}&quot;someField29&quot;: {    &quot;type&quot;: &quot;reference:BankAccount:bankId&amp;accountId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;accountId=399c2edf-4c5f-4a35-930f-b8f28074e775&quot;}&quot;someField30&quot;: {    &quot;type&quot;: &quot;reference:Product:bankId&amp;productCode&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;productCode=399c2edf-4c5f-4a35-930f-b8f28074e775&quot;}&quot;someField31&quot;: {    &quot;type&quot;: &quot;reference:PhysicalCard:bankId&amp;cardId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;cardId=399c2edf-4c5f-4a35-930f-b8f28074e775&quot;}&quot;someField32&quot;: {    &quot;type&quot;: &quot;reference:Transaction:bankId&amp;accountId&amp;transactionId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;accountId=399c2edf-4c5f-4a35-930f-b8f28074e775&amp;transactionId=68876319-84ce-4c58-8ec9-470494cd5ddd&quot;}&quot;someField33&quot;: {    &quot;type&quot;: &quot;reference:Counterparty:bankId&amp;accountId&amp;counterpartyId&quot;,    &quot;example&quot;: &quot;bankId=be7fb82c-eddd-4840-a03b-8b851fc6eedc&amp;accountId=399c2edf-4c5f-4a35-930f-b8f28074e775&amp;counterpartyId=68876319-84ce-4c58-8ec9-470494cd5ddd&quot;}</code></pre>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dynamic_entity_id:
            raise ValueError(f"Expected a non-empty value for `dynamic_entity_id` but received {dynamic_entity_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/management/system-dynamic-entities/{dynamic_entity_id}",
            body=await async_maybe_transform(body, system_dynamic_entity_update_params.SystemDynamicEntityUpdateParams),
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
        """<p>Get all System Dynamic Entities</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/management/system-dynamic-entities",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        dynamic_entity_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete a DynamicEntity specified by DYNAMIC_ENTITY_ID.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dynamic_entity_id:
            raise ValueError(f"Expected a non-empty value for `dynamic_entity_id` but received {dynamic_entity_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/management/system-dynamic-entities/{dynamic_entity_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class SystemDynamicEntitiesResourceWithRawResponse:
    def __init__(self, system_dynamic_entities: SystemDynamicEntitiesResource) -> None:
        self._system_dynamic_entities = system_dynamic_entities

        self.create = to_custom_raw_response_wrapper(
            system_dynamic_entities.create,
            BinaryAPIResponse,
        )
        self.update = to_custom_raw_response_wrapper(
            system_dynamic_entities.update,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            system_dynamic_entities.list,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            system_dynamic_entities.delete,
        )


class AsyncSystemDynamicEntitiesResourceWithRawResponse:
    def __init__(self, system_dynamic_entities: AsyncSystemDynamicEntitiesResource) -> None:
        self._system_dynamic_entities = system_dynamic_entities

        self.create = async_to_custom_raw_response_wrapper(
            system_dynamic_entities.create,
            AsyncBinaryAPIResponse,
        )
        self.update = async_to_custom_raw_response_wrapper(
            system_dynamic_entities.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            system_dynamic_entities.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            system_dynamic_entities.delete,
        )


class SystemDynamicEntitiesResourceWithStreamingResponse:
    def __init__(self, system_dynamic_entities: SystemDynamicEntitiesResource) -> None:
        self._system_dynamic_entities = system_dynamic_entities

        self.create = to_custom_streamed_response_wrapper(
            system_dynamic_entities.create,
            StreamedBinaryAPIResponse,
        )
        self.update = to_custom_streamed_response_wrapper(
            system_dynamic_entities.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            system_dynamic_entities.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            system_dynamic_entities.delete,
        )


class AsyncSystemDynamicEntitiesResourceWithStreamingResponse:
    def __init__(self, system_dynamic_entities: AsyncSystemDynamicEntitiesResource) -> None:
        self._system_dynamic_entities = system_dynamic_entities

        self.create = async_to_custom_streamed_response_wrapper(
            system_dynamic_entities.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.update = async_to_custom_streamed_response_wrapper(
            system_dynamic_entities.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            system_dynamic_entities.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            system_dynamic_entities.delete,
        )
