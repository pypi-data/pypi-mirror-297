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


class TestSwagger2:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_0(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR/swagger2.0").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        swagger2 = client.documentation.message_docs.swagger2._0()
        assert swagger2.is_closed
        assert swagger2.json() == {"foo": "bar"}
        assert cast(Any, swagger2.is_closed) is True
        assert isinstance(swagger2, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_0(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR/swagger2.0").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        swagger2 = client.documentation.message_docs.swagger2.with_raw_response._0()

        assert swagger2.is_closed is True
        assert swagger2.http_request.headers.get("X-Stainless-Lang") == "python"
        assert swagger2.json() == {"foo": "bar"}
        assert isinstance(swagger2, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_0(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR/swagger2.0").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.documentation.message_docs.swagger2.with_streaming_response._0() as swagger2:
            assert not swagger2.is_closed
            assert swagger2.http_request.headers.get("X-Stainless-Lang") == "python"

            assert swagger2.json() == {"foo": "bar"}
            assert cast(Any, swagger2.is_closed) is True
            assert isinstance(swagger2, StreamedBinaryAPIResponse)

        assert cast(Any, swagger2.is_closed) is True


class TestAsyncSwagger2:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_0(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR/swagger2.0").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        swagger2 = await async_client.documentation.message_docs.swagger2._0()
        assert swagger2.is_closed
        assert await swagger2.json() == {"foo": "bar"}
        assert cast(Any, swagger2.is_closed) is True
        assert isinstance(swagger2, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_0(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR/swagger2.0").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        swagger2 = await async_client.documentation.message_docs.swagger2.with_raw_response._0()

        assert swagger2.is_closed is True
        assert swagger2.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await swagger2.json() == {"foo": "bar"}
        assert isinstance(swagger2, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_0(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR/swagger2.0").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.documentation.message_docs.swagger2.with_streaming_response._0() as swagger2:
            assert not swagger2.is_closed
            assert swagger2.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await swagger2.json() == {"foo": "bar"}
            assert cast(Any, swagger2.is_closed) is True
            assert isinstance(swagger2, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, swagger2.is_closed) is True
