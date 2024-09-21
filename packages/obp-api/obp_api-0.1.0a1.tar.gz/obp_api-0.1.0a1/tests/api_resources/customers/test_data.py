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


class TestData:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/data").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        data = client.customers.data.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert data.is_closed
        assert data.json() == {"foo": "bar"}
        assert cast(Any, data.is_closed) is True
        assert isinstance(data, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/data").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        data = client.customers.data.with_raw_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert data.is_closed is True
        assert data.http_request.headers.get("X-Stainless-Lang") == "python"
        assert data.json() == {"foo": "bar"}
        assert isinstance(data, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/data").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.data.with_streaming_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as data:
            assert not data.is_closed
            assert data.http_request.headers.get("X-Stainless-Lang") == "python"

            assert data.json() == {"foo": "bar"}
            assert cast(Any, data.is_closed) is True
            assert isinstance(data, StreamedBinaryAPIResponse)

        assert cast(Any, data.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.data.with_raw_response.update(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.data.with_raw_response.update(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )


class TestAsyncData:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/data").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        data = await async_client.customers.data.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert data.is_closed
        assert await data.json() == {"foo": "bar"}
        assert cast(Any, data.is_closed) is True
        assert isinstance(data, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/data").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        data = await async_client.customers.data.with_raw_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert data.is_closed is True
        assert data.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await data.json() == {"foo": "bar"}
        assert isinstance(data, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/data").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.data.with_streaming_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as data:
            assert not data.is_closed
            assert data.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await data.json() == {"foo": "bar"}
            assert cast(Any, data.is_closed) is True
            assert isinstance(data, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, data.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.data.with_raw_response.update(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.data.with_raw_response.update(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )
