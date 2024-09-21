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


class TestGlossary:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api/glossary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        glossary = client.api.glossary.retrieve()
        assert glossary.is_closed
        assert glossary.json() == {"foo": "bar"}
        assert cast(Any, glossary.is_closed) is True
        assert isinstance(glossary, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api/glossary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        glossary = client.api.glossary.with_raw_response.retrieve()

        assert glossary.is_closed is True
        assert glossary.http_request.headers.get("X-Stainless-Lang") == "python"
        assert glossary.json() == {"foo": "bar"}
        assert isinstance(glossary, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api/glossary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.api.glossary.with_streaming_response.retrieve() as glossary:
            assert not glossary.is_closed
            assert glossary.http_request.headers.get("X-Stainless-Lang") == "python"

            assert glossary.json() == {"foo": "bar"}
            assert cast(Any, glossary.is_closed) is True
            assert isinstance(glossary, StreamedBinaryAPIResponse)

        assert cast(Any, glossary.is_closed) is True


class TestAsyncGlossary:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api/glossary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        glossary = await async_client.api.glossary.retrieve()
        assert glossary.is_closed
        assert await glossary.json() == {"foo": "bar"}
        assert cast(Any, glossary.is_closed) is True
        assert isinstance(glossary, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api/glossary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        glossary = await async_client.api.glossary.with_raw_response.retrieve()

        assert glossary.is_closed is True
        assert glossary.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await glossary.json() == {"foo": "bar"}
        assert isinstance(glossary, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api/glossary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.api.glossary.with_streaming_response.retrieve() as glossary:
            assert not glossary.is_closed
            assert glossary.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await glossary.json() == {"foo": "bar"}
            assert cast(Any, glossary.is_closed) is True
            assert isinstance(glossary, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, glossary.is_closed) is True
