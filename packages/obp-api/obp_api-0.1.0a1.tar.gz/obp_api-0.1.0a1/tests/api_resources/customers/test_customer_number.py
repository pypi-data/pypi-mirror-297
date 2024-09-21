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


class TestCustomerNumber:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/customer-number").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_number = client.customers.customer_number.retrieve(
            bank_id="BANK_ID",
            body={},
        )
        assert customer_number.is_closed
        assert customer_number.json() == {"foo": "bar"}
        assert cast(Any, customer_number.is_closed) is True
        assert isinstance(customer_number, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/customer-number").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_number = client.customers.customer_number.with_raw_response.retrieve(
            bank_id="BANK_ID",
            body={},
        )

        assert customer_number.is_closed is True
        assert customer_number.http_request.headers.get("X-Stainless-Lang") == "python"
        assert customer_number.json() == {"foo": "bar"}
        assert isinstance(customer_number, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/customer-number").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.customer_number.with_streaming_response.retrieve(
            bank_id="BANK_ID",
            body={},
        ) as customer_number:
            assert not customer_number.is_closed
            assert customer_number.http_request.headers.get("X-Stainless-Lang") == "python"

            assert customer_number.json() == {"foo": "bar"}
            assert cast(Any, customer_number.is_closed) is True
            assert isinstance(customer_number, StreamedBinaryAPIResponse)

        assert cast(Any, customer_number.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.customer_number.with_raw_response.retrieve(
                bank_id="",
                body={},
            )


class TestAsyncCustomerNumber:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/customer-number").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_number = await async_client.customers.customer_number.retrieve(
            bank_id="BANK_ID",
            body={},
        )
        assert customer_number.is_closed
        assert await customer_number.json() == {"foo": "bar"}
        assert cast(Any, customer_number.is_closed) is True
        assert isinstance(customer_number, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/customer-number").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_number = await async_client.customers.customer_number.with_raw_response.retrieve(
            bank_id="BANK_ID",
            body={},
        )

        assert customer_number.is_closed is True
        assert customer_number.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await customer_number.json() == {"foo": "bar"}
        assert isinstance(customer_number, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/customer-number").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.customer_number.with_streaming_response.retrieve(
            bank_id="BANK_ID",
            body={},
        ) as customer_number:
            assert not customer_number.is_closed
            assert customer_number.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await customer_number.json() == {"foo": "bar"}
            assert cast(Any, customer_number.is_closed) is True
            assert isinstance(customer_number, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, customer_number.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.customer_number.with_raw_response.retrieve(
                bank_id="",
                body={},
            )
