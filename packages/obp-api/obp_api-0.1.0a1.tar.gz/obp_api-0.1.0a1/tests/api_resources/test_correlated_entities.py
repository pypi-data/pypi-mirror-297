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


class TestCorrelatedEntities:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/correlated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        correlated_entity = client.correlated_entities.list()
        assert correlated_entity.is_closed
        assert correlated_entity.json() == {"foo": "bar"}
        assert cast(Any, correlated_entity.is_closed) is True
        assert isinstance(correlated_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/correlated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        correlated_entity = client.correlated_entities.with_raw_response.list()

        assert correlated_entity.is_closed is True
        assert correlated_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert correlated_entity.json() == {"foo": "bar"}
        assert isinstance(correlated_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/correlated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.correlated_entities.with_streaming_response.list() as correlated_entity:
            assert not correlated_entity.is_closed
            assert correlated_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert correlated_entity.json() == {"foo": "bar"}
            assert cast(Any, correlated_entity.is_closed) is True
            assert isinstance(correlated_entity, StreamedBinaryAPIResponse)

        assert cast(Any, correlated_entity.is_closed) is True


class TestAsyncCorrelatedEntities:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/correlated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        correlated_entity = await async_client.correlated_entities.list()
        assert correlated_entity.is_closed
        assert await correlated_entity.json() == {"foo": "bar"}
        assert cast(Any, correlated_entity.is_closed) is True
        assert isinstance(correlated_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/correlated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        correlated_entity = await async_client.correlated_entities.with_raw_response.list()

        assert correlated_entity.is_closed is True
        assert correlated_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await correlated_entity.json() == {"foo": "bar"}
        assert isinstance(correlated_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/correlated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.correlated_entities.with_streaming_response.list() as correlated_entity:
            assert not correlated_entity.is_closed
            assert correlated_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await correlated_entity.json() == {"foo": "bar"}
            assert cast(Any, correlated_entity.is_closed) is True
            assert isinstance(correlated_entity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, correlated_entity.is_closed) is True
