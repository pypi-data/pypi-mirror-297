# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from obp_api import ObpAPI, AsyncObpAPI

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEcho:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_jws_verified_request_jws_signed_response(self, client: ObpAPI) -> None:
        echo = client.development.echo.jws_verified_request_jws_signed_response()
        assert echo is None

    @parametrize
    def test_raw_response_jws_verified_request_jws_signed_response(self, client: ObpAPI) -> None:
        response = client.development.echo.with_raw_response.jws_verified_request_jws_signed_response()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        echo = response.parse()
        assert echo is None

    @parametrize
    def test_streaming_response_jws_verified_request_jws_signed_response(self, client: ObpAPI) -> None:
        with client.development.echo.with_streaming_response.jws_verified_request_jws_signed_response() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            echo = response.parse()
            assert echo is None

        assert cast(Any, response.is_closed) is True


class TestAsyncEcho:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_jws_verified_request_jws_signed_response(self, async_client: AsyncObpAPI) -> None:
        echo = await async_client.development.echo.jws_verified_request_jws_signed_response()
        assert echo is None

    @parametrize
    async def test_raw_response_jws_verified_request_jws_signed_response(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.development.echo.with_raw_response.jws_verified_request_jws_signed_response()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        echo = await response.parse()
        assert echo is None

    @parametrize
    async def test_streaming_response_jws_verified_request_jws_signed_response(self, async_client: AsyncObpAPI) -> None:
        async with async_client.development.echo.with_streaming_response.jws_verified_request_jws_signed_response() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            echo = await response.parse()
            assert echo is None

        assert cast(Any, response.is_closed) is True
