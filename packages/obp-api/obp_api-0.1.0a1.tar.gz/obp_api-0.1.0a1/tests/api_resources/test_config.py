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


class TestConfig:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/config").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        config = client.config.retrieve()
        assert config.is_closed
        assert config.json() == {"foo": "bar"}
        assert cast(Any, config.is_closed) is True
        assert isinstance(config, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/config").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        config = client.config.with_raw_response.retrieve()

        assert config.is_closed is True
        assert config.http_request.headers.get("X-Stainless-Lang") == "python"
        assert config.json() == {"foo": "bar"}
        assert isinstance(config, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/config").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.config.with_streaming_response.retrieve() as config:
            assert not config.is_closed
            assert config.http_request.headers.get("X-Stainless-Lang") == "python"

            assert config.json() == {"foo": "bar"}
            assert cast(Any, config.is_closed) is True
            assert isinstance(config, StreamedBinaryAPIResponse)

        assert cast(Any, config.is_closed) is True


class TestAsyncConfig:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/config").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        config = await async_client.config.retrieve()
        assert config.is_closed
        assert await config.json() == {"foo": "bar"}
        assert cast(Any, config.is_closed) is True
        assert isinstance(config, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/config").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        config = await async_client.config.with_raw_response.retrieve()

        assert config.is_closed is True
        assert config.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await config.json() == {"foo": "bar"}
        assert isinstance(config, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/config").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.config.with_streaming_response.retrieve() as config:
            assert not config.is_closed
            assert config.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await config.json() == {"foo": "bar"}
            assert cast(Any, config.is_closed) is True
            assert isinstance(config, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, config.is_closed) is True
