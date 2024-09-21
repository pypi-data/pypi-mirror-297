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


class TestSandbox:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_data_import(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/sandbox/data-import").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        sandbox = client.sandbox.data_import(
            body={},
        )
        assert sandbox.is_closed
        assert sandbox.json() == {"foo": "bar"}
        assert cast(Any, sandbox.is_closed) is True
        assert isinstance(sandbox, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_data_import(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/sandbox/data-import").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        sandbox = client.sandbox.with_raw_response.data_import(
            body={},
        )

        assert sandbox.is_closed is True
        assert sandbox.http_request.headers.get("X-Stainless-Lang") == "python"
        assert sandbox.json() == {"foo": "bar"}
        assert isinstance(sandbox, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_data_import(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/sandbox/data-import").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.sandbox.with_streaming_response.data_import(
            body={},
        ) as sandbox:
            assert not sandbox.is_closed
            assert sandbox.http_request.headers.get("X-Stainless-Lang") == "python"

            assert sandbox.json() == {"foo": "bar"}
            assert cast(Any, sandbox.is_closed) is True
            assert isinstance(sandbox, StreamedBinaryAPIResponse)

        assert cast(Any, sandbox.is_closed) is True


class TestAsyncSandbox:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_data_import(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/sandbox/data-import").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        sandbox = await async_client.sandbox.data_import(
            body={},
        )
        assert sandbox.is_closed
        assert await sandbox.json() == {"foo": "bar"}
        assert cast(Any, sandbox.is_closed) is True
        assert isinstance(sandbox, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_data_import(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/sandbox/data-import").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        sandbox = await async_client.sandbox.with_raw_response.data_import(
            body={},
        )

        assert sandbox.is_closed is True
        assert sandbox.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await sandbox.json() == {"foo": "bar"}
        assert isinstance(sandbox, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_data_import(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/sandbox/data-import").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.sandbox.with_streaming_response.data_import(
            body={},
        ) as sandbox:
            assert not sandbox.is_closed
            assert sandbox.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await sandbox.json() == {"foo": "bar"}
            assert cast(Any, sandbox.is_closed) is True
            assert isinstance(sandbox, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, sandbox.is_closed) is True
