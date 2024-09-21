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


class TestAPICollections:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/api-collections").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        api_collection = client.management.api_collections.list()
        assert api_collection.is_closed
        assert api_collection.json() == {"foo": "bar"}
        assert cast(Any, api_collection.is_closed) is True
        assert isinstance(api_collection, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/api-collections").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        api_collection = client.management.api_collections.with_raw_response.list()

        assert api_collection.is_closed is True
        assert api_collection.http_request.headers.get("X-Stainless-Lang") == "python"
        assert api_collection.json() == {"foo": "bar"}
        assert isinstance(api_collection, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/api-collections").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.management.api_collections.with_streaming_response.list() as api_collection:
            assert not api_collection.is_closed
            assert api_collection.http_request.headers.get("X-Stainless-Lang") == "python"

            assert api_collection.json() == {"foo": "bar"}
            assert cast(Any, api_collection.is_closed) is True
            assert isinstance(api_collection, StreamedBinaryAPIResponse)

        assert cast(Any, api_collection.is_closed) is True


class TestAsyncAPICollections:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/api-collections").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        api_collection = await async_client.management.api_collections.list()
        assert api_collection.is_closed
        assert await api_collection.json() == {"foo": "bar"}
        assert cast(Any, api_collection.is_closed) is True
        assert isinstance(api_collection, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/api-collections").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        api_collection = await async_client.management.api_collections.with_raw_response.list()

        assert api_collection.is_closed is True
        assert api_collection.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await api_collection.json() == {"foo": "bar"}
        assert isinstance(api_collection, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/api-collections").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.management.api_collections.with_streaming_response.list() as api_collection:
            assert not api_collection.is_closed
            assert api_collection.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await api_collection.json() == {"foo": "bar"}
            assert cast(Any, api_collection.is_closed) is True
            assert isinstance(api_collection, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, api_collection.is_closed) is True
