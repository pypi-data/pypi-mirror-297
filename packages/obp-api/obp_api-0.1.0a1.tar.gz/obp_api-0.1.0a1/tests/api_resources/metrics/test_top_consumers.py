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


class TestTopConsumers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-consumers").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        top_consumer = client.metrics.top_consumers.list()
        assert top_consumer.is_closed
        assert top_consumer.json() == {"foo": "bar"}
        assert cast(Any, top_consumer.is_closed) is True
        assert isinstance(top_consumer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-consumers").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        top_consumer = client.metrics.top_consumers.with_raw_response.list()

        assert top_consumer.is_closed is True
        assert top_consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert top_consumer.json() == {"foo": "bar"}
        assert isinstance(top_consumer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-consumers").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.metrics.top_consumers.with_streaming_response.list() as top_consumer:
            assert not top_consumer.is_closed
            assert top_consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert top_consumer.json() == {"foo": "bar"}
            assert cast(Any, top_consumer.is_closed) is True
            assert isinstance(top_consumer, StreamedBinaryAPIResponse)

        assert cast(Any, top_consumer.is_closed) is True


class TestAsyncTopConsumers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-consumers").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        top_consumer = await async_client.metrics.top_consumers.list()
        assert top_consumer.is_closed
        assert await top_consumer.json() == {"foo": "bar"}
        assert cast(Any, top_consumer.is_closed) is True
        assert isinstance(top_consumer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-consumers").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        top_consumer = await async_client.metrics.top_consumers.with_raw_response.list()

        assert top_consumer.is_closed is True
        assert top_consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await top_consumer.json() == {"foo": "bar"}
        assert isinstance(top_consumer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/top-consumers").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.metrics.top_consumers.with_streaming_response.list() as top_consumer:
            assert not top_consumer.is_closed
            assert top_consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await top_consumer.json() == {"foo": "bar"}
            assert cast(Any, top_consumer.is_closed) is True
            assert isinstance(top_consumer, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, top_consumer.is_closed) is True
