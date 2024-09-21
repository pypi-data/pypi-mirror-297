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


class TestConnector:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_loopback(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/connector/loopback").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        connector = client.connector.loopback()
        assert connector.is_closed
        assert connector.json() == {"foo": "bar"}
        assert cast(Any, connector.is_closed) is True
        assert isinstance(connector, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_loopback(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/connector/loopback").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        connector = client.connector.with_raw_response.loopback()

        assert connector.is_closed is True
        assert connector.http_request.headers.get("X-Stainless-Lang") == "python"
        assert connector.json() == {"foo": "bar"}
        assert isinstance(connector, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_loopback(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/connector/loopback").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.connector.with_streaming_response.loopback() as connector:
            assert not connector.is_closed
            assert connector.http_request.headers.get("X-Stainless-Lang") == "python"

            assert connector.json() == {"foo": "bar"}
            assert cast(Any, connector.is_closed) is True
            assert isinstance(connector, StreamedBinaryAPIResponse)

        assert cast(Any, connector.is_closed) is True


class TestAsyncConnector:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_loopback(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/connector/loopback").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        connector = await async_client.connector.loopback()
        assert connector.is_closed
        assert await connector.json() == {"foo": "bar"}
        assert cast(Any, connector.is_closed) is True
        assert isinstance(connector, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_loopback(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/connector/loopback").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        connector = await async_client.connector.with_raw_response.loopback()

        assert connector.is_closed is True
        assert connector.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await connector.json() == {"foo": "bar"}
        assert isinstance(connector, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_loopback(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/connector/loopback").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.connector.with_streaming_response.loopback() as connector:
            assert not connector.is_closed
            assert connector.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await connector.json() == {"foo": "bar"}
            assert cast(Any, connector.is_closed) is True
            assert isinstance(connector, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, connector.is_closed) is True
