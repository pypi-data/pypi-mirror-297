# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import dynamic_entity_update_params
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
        <p>Update my DynamicEntity.</p><p>Authentication is Mandatory</p><p>Update one of my DynamicEntity, after update finished, the corresponding CRUD endpoints will be changed.</p><p>Current support filed types as follow:<br />[number, integer, boolean, string, DATE_WITH_DAY, reference]</p><p>DATE_WITH_DAY format: yyyy-MM-dd</p><p>Reference types are like foreign keys and composite foreign keys are supported. The value you need to supply as the (composite) foreign key is a UUID (or several UUIDs in the case of a composite key) that match value in another Entity..<br />The following list shows all the possible reference types in the system with corresponding examples values so you can see how to construct each reference type value.</p><pre><code>&quot;someField0&quot;: {    &quot;type&quot;: &quot;reference:FishPort&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField1&quot;: {    &quot;type&quot;: &quot;reference:FooBar&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField2&quot;: {    &quot;type&quot;: &quot;reference:sustrans&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField3&quot;: {    &quot;type&quot;: &quot;reference:SimonCovid&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField4&quot;: {    &quot;type&quot;: &quot;reference:CovidAPIDays&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField5&quot;: {    &quot;type&quot;: &quot;reference:customer_cars&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField6&quot;: {    &quot;type&quot;: &quot;reference:MarchHare&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField7&quot;: {    &quot;type&quot;: &quot;reference:InsurancePolicy&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField8&quot;: {    &quot;type&quot;: &quot;reference:Odometer&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField9&quot;: {    &quot;type&quot;: &quot;reference:InsurancePremium&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField10&quot;: {    &quot;type&quot;: &quot;reference:ObpActivity&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField11&quot;: {    &quot;type&quot;: &quot;reference:test1&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField12&quot;: {    &quot;type&quot;: &quot;reference:D-Entity1&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField13&quot;: {    &quot;type&quot;: &quot;reference:test_daniel707&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField14&quot;: {    &quot;type&quot;: &quot;reference:Bank&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField15&quot;: {    &quot;type&quot;: &quot;reference:Consumer&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField16&quot;: {    &quot;type&quot;: &quot;reference:Customer&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField17&quot;: {    &quot;type&quot;: &quot;reference:MethodRouting&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField18&quot;: {    &quot;type&quot;: &quot;reference:DynamicEntity&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField19&quot;: {    &quot;type&quot;: &quot;reference:TransactionRequest&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField20&quot;: {    &quot;type&quot;: &quot;reference:ProductAttribute&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField21&quot;: {    &quot;type&quot;: &quot;reference:AccountAttribute&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField22&quot;: {    &quot;type&quot;: &quot;reference:TransactionAttribute&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField23&quot;: {    &quot;type&quot;: &quot;reference:CustomerAttribute&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField24&quot;: {    &quot;type&quot;: &quot;reference:AccountApplication&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField25&quot;: {    &quot;type&quot;: &quot;reference:CardAttribute&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField26&quot;: {    &quot;type&quot;: &quot;reference:Counterparty&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField27&quot;: {    &quot;type&quot;: &quot;reference:Branch:bankId&amp;branchId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;branchId=702660e0-665a-4dac-8196-515b2b72f547&quot;}&quot;someField28&quot;: {    &quot;type&quot;: &quot;reference:Atm:bankId&amp;atmId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;atmId=702660e0-665a-4dac-8196-515b2b72f547&quot;}&quot;someField29&quot;: {    &quot;type&quot;: &quot;reference:BankAccount:bankId&amp;accountId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;accountId=702660e0-665a-4dac-8196-515b2b72f547&quot;}&quot;someField30&quot;: {    &quot;type&quot;: &quot;reference:Product:bankId&amp;productCode&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;productCode=702660e0-665a-4dac-8196-515b2b72f547&quot;}&quot;someField31&quot;: {    &quot;type&quot;: &quot;reference:PhysicalCard:bankId&amp;cardId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;cardId=702660e0-665a-4dac-8196-515b2b72f547&quot;}&quot;someField32&quot;: {    &quot;type&quot;: &quot;reference:Transaction:bankId&amp;accountId&amp;transactionId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;accountId=702660e0-665a-4dac-8196-515b2b72f547&amp;transactionId=aa583cd0-fe83-4b48-bb58-d6746019f197&quot;}&quot;someField33&quot;: {    &quot;type&quot;: &quot;reference:Counterparty:bankId&amp;accountId&amp;counterpartyId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;accountId=702660e0-665a-4dac-8196-515b2b72f547&amp;counterpartyId=aa583cd0-fe83-4b48-bb58-d6746019f197&quot;}</code></pre>

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
            f"/obp/v5.1.0/my/dynamic-entities/{dynamic_entity_id}",
            body=maybe_transform(body, dynamic_entity_update_params.DynamicEntityUpdateParams),
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
        """<p>Get all my Dynamic Entities.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/obp/v5.1.0/my/dynamic-entities",
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
        <p>Delete my DynamicEntity specified by DYNAMIC_ENTITY_ID.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/my/dynamic-entities/{dynamic_entity_id}",
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
        <p>Update my DynamicEntity.</p><p>Authentication is Mandatory</p><p>Update one of my DynamicEntity, after update finished, the corresponding CRUD endpoints will be changed.</p><p>Current support filed types as follow:<br />[number, integer, boolean, string, DATE_WITH_DAY, reference]</p><p>DATE_WITH_DAY format: yyyy-MM-dd</p><p>Reference types are like foreign keys and composite foreign keys are supported. The value you need to supply as the (composite) foreign key is a UUID (or several UUIDs in the case of a composite key) that match value in another Entity..<br />The following list shows all the possible reference types in the system with corresponding examples values so you can see how to construct each reference type value.</p><pre><code>&quot;someField0&quot;: {    &quot;type&quot;: &quot;reference:FishPort&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField1&quot;: {    &quot;type&quot;: &quot;reference:FooBar&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField2&quot;: {    &quot;type&quot;: &quot;reference:sustrans&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField3&quot;: {    &quot;type&quot;: &quot;reference:SimonCovid&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField4&quot;: {    &quot;type&quot;: &quot;reference:CovidAPIDays&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField5&quot;: {    &quot;type&quot;: &quot;reference:customer_cars&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField6&quot;: {    &quot;type&quot;: &quot;reference:MarchHare&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField7&quot;: {    &quot;type&quot;: &quot;reference:InsurancePolicy&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField8&quot;: {    &quot;type&quot;: &quot;reference:Odometer&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField9&quot;: {    &quot;type&quot;: &quot;reference:InsurancePremium&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField10&quot;: {    &quot;type&quot;: &quot;reference:ObpActivity&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField11&quot;: {    &quot;type&quot;: &quot;reference:test1&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField12&quot;: {    &quot;type&quot;: &quot;reference:D-Entity1&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField13&quot;: {    &quot;type&quot;: &quot;reference:test_daniel707&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField14&quot;: {    &quot;type&quot;: &quot;reference:Bank&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField15&quot;: {    &quot;type&quot;: &quot;reference:Consumer&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField16&quot;: {    &quot;type&quot;: &quot;reference:Customer&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField17&quot;: {    &quot;type&quot;: &quot;reference:MethodRouting&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField18&quot;: {    &quot;type&quot;: &quot;reference:DynamicEntity&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField19&quot;: {    &quot;type&quot;: &quot;reference:TransactionRequest&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField20&quot;: {    &quot;type&quot;: &quot;reference:ProductAttribute&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField21&quot;: {    &quot;type&quot;: &quot;reference:AccountAttribute&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField22&quot;: {    &quot;type&quot;: &quot;reference:TransactionAttribute&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField23&quot;: {    &quot;type&quot;: &quot;reference:CustomerAttribute&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField24&quot;: {    &quot;type&quot;: &quot;reference:AccountApplication&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField25&quot;: {    &quot;type&quot;: &quot;reference:CardAttribute&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField26&quot;: {    &quot;type&quot;: &quot;reference:Counterparty&quot;,    &quot;example&quot;: &quot;2a7852a1-6488-4100-9a9d-af4232063d47&quot;}&quot;someField27&quot;: {    &quot;type&quot;: &quot;reference:Branch:bankId&amp;branchId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;branchId=702660e0-665a-4dac-8196-515b2b72f547&quot;}&quot;someField28&quot;: {    &quot;type&quot;: &quot;reference:Atm:bankId&amp;atmId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;atmId=702660e0-665a-4dac-8196-515b2b72f547&quot;}&quot;someField29&quot;: {    &quot;type&quot;: &quot;reference:BankAccount:bankId&amp;accountId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;accountId=702660e0-665a-4dac-8196-515b2b72f547&quot;}&quot;someField30&quot;: {    &quot;type&quot;: &quot;reference:Product:bankId&amp;productCode&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;productCode=702660e0-665a-4dac-8196-515b2b72f547&quot;}&quot;someField31&quot;: {    &quot;type&quot;: &quot;reference:PhysicalCard:bankId&amp;cardId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;cardId=702660e0-665a-4dac-8196-515b2b72f547&quot;}&quot;someField32&quot;: {    &quot;type&quot;: &quot;reference:Transaction:bankId&amp;accountId&amp;transactionId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;accountId=702660e0-665a-4dac-8196-515b2b72f547&amp;transactionId=aa583cd0-fe83-4b48-bb58-d6746019f197&quot;}&quot;someField33&quot;: {    &quot;type&quot;: &quot;reference:Counterparty:bankId&amp;accountId&amp;counterpartyId&quot;,    &quot;example&quot;: &quot;bankId=2a7852a1-6488-4100-9a9d-af4232063d47&amp;accountId=702660e0-665a-4dac-8196-515b2b72f547&amp;counterpartyId=aa583cd0-fe83-4b48-bb58-d6746019f197&quot;}</code></pre>

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
            f"/obp/v5.1.0/my/dynamic-entities/{dynamic_entity_id}",
            body=await async_maybe_transform(body, dynamic_entity_update_params.DynamicEntityUpdateParams),
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
        """<p>Get all my Dynamic Entities.</p><p>Authentication is Mandatory</p>"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/obp/v5.1.0/my/dynamic-entities",
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
        <p>Delete my DynamicEntity specified by DYNAMIC_ENTITY_ID.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/my/dynamic-entities/{dynamic_entity_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class DynamicEntitiesResourceWithRawResponse:
    def __init__(self, dynamic_entities: DynamicEntitiesResource) -> None:
        self._dynamic_entities = dynamic_entities

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
