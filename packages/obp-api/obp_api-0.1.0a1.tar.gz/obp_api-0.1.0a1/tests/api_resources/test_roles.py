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


class TestRoles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/roles").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        role = client.roles.list()
        assert role.is_closed
        assert role.json() == {"foo": "bar"}
        assert cast(Any, role.is_closed) is True
        assert isinstance(role, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/roles").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        role = client.roles.with_raw_response.list()

        assert role.is_closed is True
        assert role.http_request.headers.get("X-Stainless-Lang") == "python"
        assert role.json() == {"foo": "bar"}
        assert isinstance(role, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/roles").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.roles.with_streaming_response.list() as role:
            assert not role.is_closed
            assert role.http_request.headers.get("X-Stainless-Lang") == "python"

            assert role.json() == {"foo": "bar"}
            assert cast(Any, role.is_closed) is True
            assert isinstance(role, StreamedBinaryAPIResponse)

        assert cast(Any, role.is_closed) is True


class TestAsyncRoles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/roles").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        role = await async_client.roles.list()
        assert role.is_closed
        assert await role.json() == {"foo": "bar"}
        assert cast(Any, role.is_closed) is True
        assert isinstance(role, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/roles").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        role = await async_client.roles.with_raw_response.list()

        assert role.is_closed is True
        assert role.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await role.json() == {"foo": "bar"}
        assert isinstance(role, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/roles").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.roles.with_streaming_response.list() as role:
            assert not role.is_closed
            assert role.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await role.json() == {"foo": "bar"}
            assert cast(Any, role.is_closed) is True
            assert isinstance(role, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, role.is_closed) is True
