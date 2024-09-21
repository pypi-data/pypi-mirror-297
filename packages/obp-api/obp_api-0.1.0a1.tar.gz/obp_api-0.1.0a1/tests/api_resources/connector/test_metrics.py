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


class TestMetrics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector/metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        metric = client.connector.metrics.list()
        assert metric.is_closed
        assert metric.json() == {"foo": "bar"}
        assert cast(Any, metric.is_closed) is True
        assert isinstance(metric, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector/metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        metric = client.connector.metrics.with_raw_response.list()

        assert metric.is_closed is True
        assert metric.http_request.headers.get("X-Stainless-Lang") == "python"
        assert metric.json() == {"foo": "bar"}
        assert isinstance(metric, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector/metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.connector.metrics.with_streaming_response.list() as metric:
            assert not metric.is_closed
            assert metric.http_request.headers.get("X-Stainless-Lang") == "python"

            assert metric.json() == {"foo": "bar"}
            assert cast(Any, metric.is_closed) is True
            assert isinstance(metric, StreamedBinaryAPIResponse)

        assert cast(Any, metric.is_closed) is True


class TestAsyncMetrics:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector/metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        metric = await async_client.connector.metrics.list()
        assert metric.is_closed
        assert await metric.json() == {"foo": "bar"}
        assert cast(Any, metric.is_closed) is True
        assert isinstance(metric, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector/metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        metric = await async_client.connector.metrics.with_raw_response.list()

        assert metric.is_closed is True
        assert metric.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await metric.json() == {"foo": "bar"}
        assert isinstance(metric, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector/metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.connector.metrics.with_streaming_response.list() as metric:
            assert not metric.is_closed
            assert metric.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await metric.json() == {"foo": "bar"}
            assert cast(Any, metric.is_closed) is True
            assert isinstance(metric, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, metric.is_closed) is True
