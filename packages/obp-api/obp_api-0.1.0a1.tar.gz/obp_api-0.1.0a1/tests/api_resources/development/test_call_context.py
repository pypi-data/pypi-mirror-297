# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from obp_api import ObpAPI, AsyncObpAPI

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCallContext:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: ObpAPI) -> None:
        call_context = client.development.call_context.retrieve()
        assert call_context is None

    @parametrize
    def test_raw_response_retrieve(self, client: ObpAPI) -> None:
        response = client.development.call_context.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call_context = response.parse()
        assert call_context is None

    @parametrize
    def test_streaming_response_retrieve(self, client: ObpAPI) -> None:
        with client.development.call_context.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call_context = response.parse()
            assert call_context is None

        assert cast(Any, response.is_closed) is True


class TestAsyncCallContext:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncObpAPI) -> None:
        call_context = await async_client.development.call_context.retrieve()
        assert call_context is None

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.development.call_context.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call_context = await response.parse()
        assert call_context is None

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI) -> None:
        async with async_client.development.call_context.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call_context = await response.parse()
            assert call_context is None

        assert cast(Any, response.is_closed) is True
