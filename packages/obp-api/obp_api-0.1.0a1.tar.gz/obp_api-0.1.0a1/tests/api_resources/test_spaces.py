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


class TestSpaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/spaces").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        space = client.spaces.list()
        assert space.is_closed
        assert space.json() == {"foo": "bar"}
        assert cast(Any, space.is_closed) is True
        assert isinstance(space, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/spaces").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        space = client.spaces.with_raw_response.list()

        assert space.is_closed is True
        assert space.http_request.headers.get("X-Stainless-Lang") == "python"
        assert space.json() == {"foo": "bar"}
        assert isinstance(space, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/spaces").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.spaces.with_streaming_response.list() as space:
            assert not space.is_closed
            assert space.http_request.headers.get("X-Stainless-Lang") == "python"

            assert space.json() == {"foo": "bar"}
            assert cast(Any, space.is_closed) is True
            assert isinstance(space, StreamedBinaryAPIResponse)

        assert cast(Any, space.is_closed) is True


class TestAsyncSpaces:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/spaces").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        space = await async_client.spaces.list()
        assert space.is_closed
        assert await space.json() == {"foo": "bar"}
        assert cast(Any, space.is_closed) is True
        assert isinstance(space, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/spaces").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        space = await async_client.spaces.with_raw_response.list()

        assert space.is_closed is True
        assert space.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await space.json() == {"foo": "bar"}
        assert isinstance(space, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/spaces").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.spaces.with_streaming_response.list() as space:
            assert not space.is_closed
            assert space.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await space.json() == {"foo": "bar"}
            assert cast(Any, space.is_closed) is True
            assert isinstance(space, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, space.is_closed) is True
