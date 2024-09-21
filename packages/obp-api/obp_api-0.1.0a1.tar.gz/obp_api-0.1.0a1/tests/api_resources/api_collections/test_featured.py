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


class TestFeatured:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/featured").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        featured = client.api_collections.featured.list()
        assert featured.is_closed
        assert featured.json() == {"foo": "bar"}
        assert cast(Any, featured.is_closed) is True
        assert isinstance(featured, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/featured").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        featured = client.api_collections.featured.with_raw_response.list()

        assert featured.is_closed is True
        assert featured.http_request.headers.get("X-Stainless-Lang") == "python"
        assert featured.json() == {"foo": "bar"}
        assert isinstance(featured, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/featured").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.api_collections.featured.with_streaming_response.list() as featured:
            assert not featured.is_closed
            assert featured.http_request.headers.get("X-Stainless-Lang") == "python"

            assert featured.json() == {"foo": "bar"}
            assert cast(Any, featured.is_closed) is True
            assert isinstance(featured, StreamedBinaryAPIResponse)

        assert cast(Any, featured.is_closed) is True


class TestAsyncFeatured:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/featured").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        featured = await async_client.api_collections.featured.list()
        assert featured.is_closed
        assert await featured.json() == {"foo": "bar"}
        assert cast(Any, featured.is_closed) is True
        assert isinstance(featured, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/featured").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        featured = await async_client.api_collections.featured.with_raw_response.list()

        assert featured.is_closed is True
        assert featured.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await featured.json() == {"foo": "bar"}
        assert isinstance(featured, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/featured").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.api_collections.featured.with_streaming_response.list() as featured:
            assert not featured.is_closed
            assert featured.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await featured.json() == {"foo": "bar"}
            assert cast(Any, featured.is_closed) is True
            assert isinstance(featured, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, featured.is_closed) is True
