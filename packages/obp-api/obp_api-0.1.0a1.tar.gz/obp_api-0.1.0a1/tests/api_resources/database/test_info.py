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


class TestInfo:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/database/info").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        info = client.database.info.retrieve()
        assert info.is_closed
        assert info.json() == {"foo": "bar"}
        assert cast(Any, info.is_closed) is True
        assert isinstance(info, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/database/info").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        info = client.database.info.with_raw_response.retrieve()

        assert info.is_closed is True
        assert info.http_request.headers.get("X-Stainless-Lang") == "python"
        assert info.json() == {"foo": "bar"}
        assert isinstance(info, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/database/info").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.database.info.with_streaming_response.retrieve() as info:
            assert not info.is_closed
            assert info.http_request.headers.get("X-Stainless-Lang") == "python"

            assert info.json() == {"foo": "bar"}
            assert cast(Any, info.is_closed) is True
            assert isinstance(info, StreamedBinaryAPIResponse)

        assert cast(Any, info.is_closed) is True


class TestAsyncInfo:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/database/info").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        info = await async_client.database.info.retrieve()
        assert info.is_closed
        assert await info.json() == {"foo": "bar"}
        assert cast(Any, info.is_closed) is True
        assert isinstance(info, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/database/info").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        info = await async_client.database.info.with_raw_response.retrieve()

        assert info.is_closed is True
        assert info.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await info.json() == {"foo": "bar"}
        assert isinstance(info, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/database/info").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.database.info.with_streaming_response.retrieve() as info:
            assert not info.is_closed
            assert info.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await info.json() == {"foo": "bar"}
            assert cast(Any, info.is_closed) is True
            assert isinstance(info, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, info.is_closed) is True
