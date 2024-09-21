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


class TestAggregateMetrics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/aggregate-metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        aggregate_metric = client.management.aggregate_metrics.list()
        assert aggregate_metric.is_closed
        assert aggregate_metric.json() == {"foo": "bar"}
        assert cast(Any, aggregate_metric.is_closed) is True
        assert isinstance(aggregate_metric, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/aggregate-metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        aggregate_metric = client.management.aggregate_metrics.with_raw_response.list()

        assert aggregate_metric.is_closed is True
        assert aggregate_metric.http_request.headers.get("X-Stainless-Lang") == "python"
        assert aggregate_metric.json() == {"foo": "bar"}
        assert isinstance(aggregate_metric, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/aggregate-metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.management.aggregate_metrics.with_streaming_response.list() as aggregate_metric:
            assert not aggregate_metric.is_closed
            assert aggregate_metric.http_request.headers.get("X-Stainless-Lang") == "python"

            assert aggregate_metric.json() == {"foo": "bar"}
            assert cast(Any, aggregate_metric.is_closed) is True
            assert isinstance(aggregate_metric, StreamedBinaryAPIResponse)

        assert cast(Any, aggregate_metric.is_closed) is True


class TestAsyncAggregateMetrics:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/aggregate-metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        aggregate_metric = await async_client.management.aggregate_metrics.list()
        assert aggregate_metric.is_closed
        assert await aggregate_metric.json() == {"foo": "bar"}
        assert cast(Any, aggregate_metric.is_closed) is True
        assert isinstance(aggregate_metric, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/aggregate-metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        aggregate_metric = await async_client.management.aggregate_metrics.with_raw_response.list()

        assert aggregate_metric.is_closed is True
        assert aggregate_metric.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await aggregate_metric.json() == {"foo": "bar"}
        assert isinstance(aggregate_metric, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/aggregate-metrics").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.management.aggregate_metrics.with_streaming_response.list() as aggregate_metric:
            assert not aggregate_metric.is_closed
            assert aggregate_metric.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await aggregate_metric.json() == {"foo": "bar"}
            assert cast(Any, aggregate_metric.is_closed) is True
            assert isinstance(aggregate_metric, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, aggregate_metric.is_closed) is True
