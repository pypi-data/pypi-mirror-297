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


class TestSharable:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/sharable/API_COLLECTION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        sharable = client.api_collections.sharable.retrieve()
        assert sharable.is_closed
        assert sharable.json() == {"foo": "bar"}
        assert cast(Any, sharable.is_closed) is True
        assert isinstance(sharable, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/sharable/API_COLLECTION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        sharable = client.api_collections.sharable.with_raw_response.retrieve()

        assert sharable.is_closed is True
        assert sharable.http_request.headers.get("X-Stainless-Lang") == "python"
        assert sharable.json() == {"foo": "bar"}
        assert isinstance(sharable, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/sharable/API_COLLECTION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.api_collections.sharable.with_streaming_response.retrieve() as sharable:
            assert not sharable.is_closed
            assert sharable.http_request.headers.get("X-Stainless-Lang") == "python"

            assert sharable.json() == {"foo": "bar"}
            assert cast(Any, sharable.is_closed) is True
            assert isinstance(sharable, StreamedBinaryAPIResponse)

        assert cast(Any, sharable.is_closed) is True


class TestAsyncSharable:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/sharable/API_COLLECTION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        sharable = await async_client.api_collections.sharable.retrieve()
        assert sharable.is_closed
        assert await sharable.json() == {"foo": "bar"}
        assert cast(Any, sharable.is_closed) is True
        assert isinstance(sharable, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/sharable/API_COLLECTION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        sharable = await async_client.api_collections.sharable.with_raw_response.retrieve()

        assert sharable.is_closed is True
        assert sharable.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await sharable.json() == {"foo": "bar"}
        assert isinstance(sharable, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/sharable/API_COLLECTION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.api_collections.sharable.with_streaming_response.retrieve() as sharable:
            assert not sharable.is_closed
            assert sharable.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await sharable.json() == {"foo": "bar"}
            assert cast(Any, sharable.is_closed) is True
            assert isinstance(sharable, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, sharable.is_closed) is True
