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


class TestIDs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views-ids").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        id = client.system_views.ids.list()
        assert id.is_closed
        assert id.json() == {"foo": "bar"}
        assert cast(Any, id.is_closed) is True
        assert isinstance(id, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views-ids").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        id = client.system_views.ids.with_raw_response.list()

        assert id.is_closed is True
        assert id.http_request.headers.get("X-Stainless-Lang") == "python"
        assert id.json() == {"foo": "bar"}
        assert isinstance(id, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views-ids").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.system_views.ids.with_streaming_response.list() as id:
            assert not id.is_closed
            assert id.http_request.headers.get("X-Stainless-Lang") == "python"

            assert id.json() == {"foo": "bar"}
            assert cast(Any, id.is_closed) is True
            assert isinstance(id, StreamedBinaryAPIResponse)

        assert cast(Any, id.is_closed) is True


class TestAsyncIDs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views-ids").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        id = await async_client.system_views.ids.list()
        assert id.is_closed
        assert await id.json() == {"foo": "bar"}
        assert cast(Any, id.is_closed) is True
        assert isinstance(id, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views-ids").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        id = await async_client.system_views.ids.with_raw_response.list()

        assert id.is_closed is True
        assert id.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await id.json() == {"foo": "bar"}
        assert isinstance(id, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views-ids").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.system_views.ids.with_streaming_response.list() as id:
            assert not id.is_closed
            assert id.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await id.json() == {"foo": "bar"}
            assert cast(Any, id.is_closed) is True
            assert isinstance(id, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, id.is_closed) is True
