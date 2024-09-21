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


class TestJwksUris:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/jwks-uris").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        jwks_uris = client.jwks_uris.retrieve()
        assert jwks_uris.is_closed
        assert jwks_uris.json() == {"foo": "bar"}
        assert cast(Any, jwks_uris.is_closed) is True
        assert isinstance(jwks_uris, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/jwks-uris").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        jwks_uris = client.jwks_uris.with_raw_response.retrieve()

        assert jwks_uris.is_closed is True
        assert jwks_uris.http_request.headers.get("X-Stainless-Lang") == "python"
        assert jwks_uris.json() == {"foo": "bar"}
        assert isinstance(jwks_uris, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/jwks-uris").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.jwks_uris.with_streaming_response.retrieve() as jwks_uris:
            assert not jwks_uris.is_closed
            assert jwks_uris.http_request.headers.get("X-Stainless-Lang") == "python"

            assert jwks_uris.json() == {"foo": "bar"}
            assert cast(Any, jwks_uris.is_closed) is True
            assert isinstance(jwks_uris, StreamedBinaryAPIResponse)

        assert cast(Any, jwks_uris.is_closed) is True


class TestAsyncJwksUris:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/jwks-uris").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        jwks_uris = await async_client.jwks_uris.retrieve()
        assert jwks_uris.is_closed
        assert await jwks_uris.json() == {"foo": "bar"}
        assert cast(Any, jwks_uris.is_closed) is True
        assert isinstance(jwks_uris, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/jwks-uris").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        jwks_uris = await async_client.jwks_uris.with_raw_response.retrieve()

        assert jwks_uris.is_closed is True
        assert jwks_uris.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await jwks_uris.json() == {"foo": "bar"}
        assert isinstance(jwks_uris, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/jwks-uris").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.jwks_uris.with_streaming_response.retrieve() as jwks_uris:
            assert not jwks_uris.is_closed
            assert jwks_uris.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await jwks_uris.json() == {"foo": "bar"}
            assert cast(Any, jwks_uris.is_closed) is True
            assert isinstance(jwks_uris, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, jwks_uris.is_closed) is True
