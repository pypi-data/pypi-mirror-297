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


class TestTopAPIs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-apis").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        top_api = client.metrics.top_apis.list()
        assert top_api.is_closed
        assert top_api.json() == {"foo": "bar"}
        assert cast(Any, top_api.is_closed) is True
        assert isinstance(top_api, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-apis").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        top_api = client.metrics.top_apis.with_raw_response.list()

        assert top_api.is_closed is True
        assert top_api.http_request.headers.get("X-Stainless-Lang") == "python"
        assert top_api.json() == {"foo": "bar"}
        assert isinstance(top_api, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-apis").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.metrics.top_apis.with_streaming_response.list() as top_api:
            assert not top_api.is_closed
            assert top_api.http_request.headers.get("X-Stainless-Lang") == "python"

            assert top_api.json() == {"foo": "bar"}
            assert cast(Any, top_api.is_closed) is True
            assert isinstance(top_api, StreamedBinaryAPIResponse)

        assert cast(Any, top_api.is_closed) is True


class TestAsyncTopAPIs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-apis").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        top_api = await async_client.metrics.top_apis.list()
        assert top_api.is_closed
        assert await top_api.json() == {"foo": "bar"}
        assert cast(Any, top_api.is_closed) is True
        assert isinstance(top_api, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-apis").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        top_api = await async_client.metrics.top_apis.with_raw_response.list()

        assert top_api.is_closed is True
        assert top_api.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await top_api.json() == {"foo": "bar"}
        assert isinstance(top_api, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-apis").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.metrics.top_apis.with_streaming_response.list() as top_api:
            assert not top_api.is_closed
            assert top_api.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await top_api.json() == {"foo": "bar"}
            assert cast(Any, top_api.is_closed) is True
            assert isinstance(top_api, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, top_api.is_closed) is True
