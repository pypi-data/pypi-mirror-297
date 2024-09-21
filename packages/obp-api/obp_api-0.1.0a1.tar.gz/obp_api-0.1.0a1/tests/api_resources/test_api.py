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


class TestAPI:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_root(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/root").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        api = client.api.root()
        assert api.is_closed
        assert api.json() == {"foo": "bar"}
        assert cast(Any, api.is_closed) is True
        assert isinstance(api, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_root(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/root").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        api = client.api.with_raw_response.root()

        assert api.is_closed is True
        assert api.http_request.headers.get("X-Stainless-Lang") == "python"
        assert api.json() == {"foo": "bar"}
        assert isinstance(api, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_root(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/root").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.api.with_streaming_response.root() as api:
            assert not api.is_closed
            assert api.http_request.headers.get("X-Stainless-Lang") == "python"

            assert api.json() == {"foo": "bar"}
            assert cast(Any, api.is_closed) is True
            assert isinstance(api, StreamedBinaryAPIResponse)

        assert cast(Any, api.is_closed) is True


class TestAsyncAPI:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_root(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/root").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        api = await async_client.api.root()
        assert api.is_closed
        assert await api.json() == {"foo": "bar"}
        assert cast(Any, api.is_closed) is True
        assert isinstance(api, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_root(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/root").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        api = await async_client.api.with_raw_response.root()

        assert api.is_closed is True
        assert api.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await api.json() == {"foo": "bar"}
        assert isinstance(api, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_root(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/root").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.api.with_streaming_response.root() as api:
            assert not api.is_closed
            assert api.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await api.json() == {"foo": "bar"}
            assert cast(Any, api.is_closed) is True
            assert isinstance(api, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, api.is_closed) is True
