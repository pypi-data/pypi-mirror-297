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


class TestCurrent:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/mtls/certificate/current").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        current = client.mtls.certificate.current.retrieve()
        assert current.is_closed
        assert current.json() == {"foo": "bar"}
        assert cast(Any, current.is_closed) is True
        assert isinstance(current, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/mtls/certificate/current").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        current = client.mtls.certificate.current.with_raw_response.retrieve()

        assert current.is_closed is True
        assert current.http_request.headers.get("X-Stainless-Lang") == "python"
        assert current.json() == {"foo": "bar"}
        assert isinstance(current, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/mtls/certificate/current").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.mtls.certificate.current.with_streaming_response.retrieve() as current:
            assert not current.is_closed
            assert current.http_request.headers.get("X-Stainless-Lang") == "python"

            assert current.json() == {"foo": "bar"}
            assert cast(Any, current.is_closed) is True
            assert isinstance(current, StreamedBinaryAPIResponse)

        assert cast(Any, current.is_closed) is True


class TestAsyncCurrent:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/mtls/certificate/current").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        current = await async_client.mtls.certificate.current.retrieve()
        assert current.is_closed
        assert await current.json() == {"foo": "bar"}
        assert cast(Any, current.is_closed) is True
        assert isinstance(current, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/mtls/certificate/current").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        current = await async_client.mtls.certificate.current.with_raw_response.retrieve()

        assert current.is_closed is True
        assert current.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await current.json() == {"foo": "bar"}
        assert isinstance(current, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/mtls/certificate/current").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.mtls.certificate.current.with_streaming_response.retrieve() as current:
            assert not current.is_closed
            assert current.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await current.json() == {"foo": "bar"}
            assert cast(Any, current.is_closed) is True
            assert isinstance(current, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, current.is_closed) is True
