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


class TestCustomers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user_customer_links/customers/CUSTOMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer = client.user_customer_links.customers.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert customer.is_closed
        assert customer.json() == {"foo": "bar"}
        assert cast(Any, customer.is_closed) is True
        assert isinstance(customer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user_customer_links/customers/CUSTOMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer = client.user_customer_links.customers.with_raw_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert customer.is_closed is True
        assert customer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert customer.json() == {"foo": "bar"}
        assert isinstance(customer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user_customer_links/customers/CUSTOMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.user_customer_links.customers.with_streaming_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as customer:
            assert not customer.is_closed
            assert customer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert customer.json() == {"foo": "bar"}
            assert cast(Any, customer.is_closed) is True
            assert isinstance(customer, StreamedBinaryAPIResponse)

        assert cast(Any, customer.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.user_customer_links.customers.with_raw_response.list(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.user_customer_links.customers.with_raw_response.list(
                customer_id="",
                bank_id="BANK_ID",
            )


class TestAsyncCustomers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user_customer_links/customers/CUSTOMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer = await async_client.user_customer_links.customers.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert customer.is_closed
        assert await customer.json() == {"foo": "bar"}
        assert cast(Any, customer.is_closed) is True
        assert isinstance(customer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user_customer_links/customers/CUSTOMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer = await async_client.user_customer_links.customers.with_raw_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert customer.is_closed is True
        assert customer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await customer.json() == {"foo": "bar"}
        assert isinstance(customer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user_customer_links/customers/CUSTOMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.user_customer_links.customers.with_streaming_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as customer:
            assert not customer.is_closed
            assert customer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await customer.json() == {"foo": "bar"}
            assert cast(Any, customer.is_closed) is True
            assert isinstance(customer, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, customer.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.user_customer_links.customers.with_raw_response.list(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.user_customer_links.customers.with_raw_response.list(
                customer_id="",
                bank_id="BANK_ID",
            )
