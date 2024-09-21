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


class TestCustomersMinimal:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers-minimal").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        customers_minimal = client.customers_minimal.list()
        assert customers_minimal.is_closed
        assert customers_minimal.json() == {"foo": "bar"}
        assert cast(Any, customers_minimal.is_closed) is True
        assert isinstance(customers_minimal, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers-minimal").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        customers_minimal = client.customers_minimal.with_raw_response.list()

        assert customers_minimal.is_closed is True
        assert customers_minimal.http_request.headers.get("X-Stainless-Lang") == "python"
        assert customers_minimal.json() == {"foo": "bar"}
        assert isinstance(customers_minimal, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers-minimal").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.customers_minimal.with_streaming_response.list() as customers_minimal:
            assert not customers_minimal.is_closed
            assert customers_minimal.http_request.headers.get("X-Stainless-Lang") == "python"

            assert customers_minimal.json() == {"foo": "bar"}
            assert cast(Any, customers_minimal.is_closed) is True
            assert isinstance(customers_minimal, StreamedBinaryAPIResponse)

        assert cast(Any, customers_minimal.is_closed) is True


class TestAsyncCustomersMinimal:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers-minimal").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        customers_minimal = await async_client.customers_minimal.list()
        assert customers_minimal.is_closed
        assert await customers_minimal.json() == {"foo": "bar"}
        assert cast(Any, customers_minimal.is_closed) is True
        assert isinstance(customers_minimal, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers-minimal").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        customers_minimal = await async_client.customers_minimal.with_raw_response.list()

        assert customers_minimal.is_closed is True
        assert customers_minimal.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await customers_minimal.json() == {"foo": "bar"}
        assert isinstance(customers_minimal, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers-minimal").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.customers_minimal.with_streaming_response.list() as customers_minimal:
            assert not customers_minimal.is_closed
            assert customers_minimal.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await customers_minimal.json() == {"foo": "bar"}
            assert cast(Any, customers_minimal.is_closed) is True
            assert isinstance(customers_minimal, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, customers_minimal.is_closed) is True
