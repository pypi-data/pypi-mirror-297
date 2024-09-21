# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from obp_api import ObpAPI, AsyncObpAPI
from obp_api._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCustomerAccountLinks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_account_link = client.customers.customer_account_links.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert customer_account_link.is_closed
        assert customer_account_link.json() == {"foo": "bar"}
        assert cast(Any, customer_account_link.is_closed) is True
        assert isinstance(customer_account_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_account_link = client.customers.customer_account_links.with_raw_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert customer_account_link.is_closed is True
        assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert customer_account_link.json() == {"foo": "bar"}
        assert isinstance(customer_account_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.customer_account_links.with_streaming_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as customer_account_link:
            assert not customer_account_link.is_closed
            assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert customer_account_link.json() == {"foo": "bar"}
            assert cast(Any, customer_account_link.is_closed) is True
            assert isinstance(customer_account_link, StreamedBinaryAPIResponse)

        assert cast(Any, customer_account_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.customer_account_links.with_raw_response.list(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.customer_account_links.with_raw_response.list(
                customer_id="",
                bank_id="BANK_ID",
            )


class TestAsyncCustomerAccountLinks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_account_link = await async_client.customers.customer_account_links.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert customer_account_link.is_closed
        assert await customer_account_link.json() == {"foo": "bar"}
        assert cast(Any, customer_account_link.is_closed) is True
        assert isinstance(customer_account_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_account_link = await async_client.customers.customer_account_links.with_raw_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert customer_account_link.is_closed is True
        assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await customer_account_link.json() == {"foo": "bar"}
        assert isinstance(customer_account_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.customer_account_links.with_streaming_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as customer_account_link:
            assert not customer_account_link.is_closed
            assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await customer_account_link.json() == {"foo": "bar"}
            assert cast(Any, customer_account_link.is_closed) is True
            assert isinstance(customer_account_link, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, customer_account_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.customer_account_links.with_raw_response.list(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.customer_account_links.with_raw_response.list(
                customer_id="",
                bank_id="BANK_ID",
            )
