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


class TestSuggestedSessionTimeout:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/ui/suggested-session-timeout").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        suggested_session_timeout = client.api.suggested_session_timeout.retrieve()
        assert suggested_session_timeout.is_closed
        assert suggested_session_timeout.json() == {"foo": "bar"}
        assert cast(Any, suggested_session_timeout.is_closed) is True
        assert isinstance(suggested_session_timeout, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/ui/suggested-session-timeout").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        suggested_session_timeout = client.api.suggested_session_timeout.with_raw_response.retrieve()

        assert suggested_session_timeout.is_closed is True
        assert suggested_session_timeout.http_request.headers.get("X-Stainless-Lang") == "python"
        assert suggested_session_timeout.json() == {"foo": "bar"}
        assert isinstance(suggested_session_timeout, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/ui/suggested-session-timeout").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.api.suggested_session_timeout.with_streaming_response.retrieve() as suggested_session_timeout:
            assert not suggested_session_timeout.is_closed
            assert suggested_session_timeout.http_request.headers.get("X-Stainless-Lang") == "python"

            assert suggested_session_timeout.json() == {"foo": "bar"}
            assert cast(Any, suggested_session_timeout.is_closed) is True
            assert isinstance(suggested_session_timeout, StreamedBinaryAPIResponse)

        assert cast(Any, suggested_session_timeout.is_closed) is True


class TestAsyncSuggestedSessionTimeout:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/ui/suggested-session-timeout").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        suggested_session_timeout = await async_client.api.suggested_session_timeout.retrieve()
        assert suggested_session_timeout.is_closed
        assert await suggested_session_timeout.json() == {"foo": "bar"}
        assert cast(Any, suggested_session_timeout.is_closed) is True
        assert isinstance(suggested_session_timeout, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/ui/suggested-session-timeout").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        suggested_session_timeout = await async_client.api.suggested_session_timeout.with_raw_response.retrieve()

        assert suggested_session_timeout.is_closed is True
        assert suggested_session_timeout.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await suggested_session_timeout.json() == {"foo": "bar"}
        assert isinstance(suggested_session_timeout, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/ui/suggested-session-timeout").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.api.suggested_session_timeout.with_streaming_response.retrieve() as suggested_session_timeout:
            assert not suggested_session_timeout.is_closed
            assert suggested_session_timeout.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await suggested_session_timeout.json() == {"foo": "bar"}
            assert cast(Any, suggested_session_timeout.is_closed) is True
            assert isinstance(suggested_session_timeout, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, suggested_session_timeout.is_closed) is True
