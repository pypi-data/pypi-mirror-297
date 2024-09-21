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


class TestAdapter:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/adapter").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        adapter = client.adapter.retrieve()
        assert adapter.is_closed
        assert adapter.json() == {"foo": "bar"}
        assert cast(Any, adapter.is_closed) is True
        assert isinstance(adapter, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/adapter").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        adapter = client.adapter.with_raw_response.retrieve()

        assert adapter.is_closed is True
        assert adapter.http_request.headers.get("X-Stainless-Lang") == "python"
        assert adapter.json() == {"foo": "bar"}
        assert isinstance(adapter, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/adapter").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.adapter.with_streaming_response.retrieve() as adapter:
            assert not adapter.is_closed
            assert adapter.http_request.headers.get("X-Stainless-Lang") == "python"

            assert adapter.json() == {"foo": "bar"}
            assert cast(Any, adapter.is_closed) is True
            assert isinstance(adapter, StreamedBinaryAPIResponse)

        assert cast(Any, adapter.is_closed) is True


class TestAsyncAdapter:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/adapter").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        adapter = await async_client.adapter.retrieve()
        assert adapter.is_closed
        assert await adapter.json() == {"foo": "bar"}
        assert cast(Any, adapter.is_closed) is True
        assert isinstance(adapter, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/adapter").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        adapter = await async_client.adapter.with_raw_response.retrieve()

        assert adapter.is_closed is True
        assert adapter.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await adapter.json() == {"foo": "bar"}
        assert isinstance(adapter, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/adapter").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.adapter.with_streaming_response.retrieve() as adapter:
            assert not adapter.is_closed
            assert adapter.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await adapter.json() == {"foo": "bar"}
            assert cast(Any, adapter.is_closed) is True
            assert isinstance(adapter, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, adapter.is_closed) is True
