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


class TestCerts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/certs").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        cert = client.certs.list()
        assert cert.is_closed
        assert cert.json() == {"foo": "bar"}
        assert cast(Any, cert.is_closed) is True
        assert isinstance(cert, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/certs").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        cert = client.certs.with_raw_response.list()

        assert cert.is_closed is True
        assert cert.http_request.headers.get("X-Stainless-Lang") == "python"
        assert cert.json() == {"foo": "bar"}
        assert isinstance(cert, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/certs").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.certs.with_streaming_response.list() as cert:
            assert not cert.is_closed
            assert cert.http_request.headers.get("X-Stainless-Lang") == "python"

            assert cert.json() == {"foo": "bar"}
            assert cast(Any, cert.is_closed) is True
            assert isinstance(cert, StreamedBinaryAPIResponse)

        assert cast(Any, cert.is_closed) is True


class TestAsyncCerts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/certs").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        cert = await async_client.certs.list()
        assert cert.is_closed
        assert await cert.json() == {"foo": "bar"}
        assert cast(Any, cert.is_closed) is True
        assert isinstance(cert, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/certs").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        cert = await async_client.certs.with_raw_response.list()

        assert cert.is_closed is True
        assert cert.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await cert.json() == {"foo": "bar"}
        assert isinstance(cert, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/certs").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.certs.with_streaming_response.list() as cert:
            assert not cert.is_closed
            assert cert.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await cert.json() == {"foo": "bar"}
            assert cast(Any, cert.is_closed) is True
            assert isinstance(cert, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, cert.is_closed) is True
