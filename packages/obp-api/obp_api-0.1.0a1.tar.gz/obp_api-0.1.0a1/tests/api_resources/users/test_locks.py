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


class TestLocks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users/PROVIDER/USERNAME/locks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        lock = client.users.locks.create(
            username="USERNAME",
            provider="PROVIDER",
        )
        assert lock.is_closed
        assert lock.json() == {"foo": "bar"}
        assert cast(Any, lock.is_closed) is True
        assert isinstance(lock, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users/PROVIDER/USERNAME/locks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        lock = client.users.locks.with_raw_response.create(
            username="USERNAME",
            provider="PROVIDER",
        )

        assert lock.is_closed is True
        assert lock.http_request.headers.get("X-Stainless-Lang") == "python"
        assert lock.json() == {"foo": "bar"}
        assert isinstance(lock, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users/PROVIDER/USERNAME/locks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.users.locks.with_streaming_response.create(
            username="USERNAME",
            provider="PROVIDER",
        ) as lock:
            assert not lock.is_closed
            assert lock.http_request.headers.get("X-Stainless-Lang") == "python"

            assert lock.json() == {"foo": "bar"}
            assert cast(Any, lock.is_closed) is True
            assert isinstance(lock, StreamedBinaryAPIResponse)

        assert cast(Any, lock.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider` but received ''"):
            client.users.locks.with_raw_response.create(
                username="USERNAME",
                provider="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `username` but received ''"):
            client.users.locks.with_raw_response.create(
                username="",
                provider="PROVIDER",
            )


class TestAsyncLocks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users/PROVIDER/USERNAME/locks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        lock = await async_client.users.locks.create(
            username="USERNAME",
            provider="PROVIDER",
        )
        assert lock.is_closed
        assert await lock.json() == {"foo": "bar"}
        assert cast(Any, lock.is_closed) is True
        assert isinstance(lock, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users/PROVIDER/USERNAME/locks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        lock = await async_client.users.locks.with_raw_response.create(
            username="USERNAME",
            provider="PROVIDER",
        )

        assert lock.is_closed is True
        assert lock.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await lock.json() == {"foo": "bar"}
        assert isinstance(lock, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users/PROVIDER/USERNAME/locks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.users.locks.with_streaming_response.create(
            username="USERNAME",
            provider="PROVIDER",
        ) as lock:
            assert not lock.is_closed
            assert lock.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await lock.json() == {"foo": "bar"}
            assert cast(Any, lock.is_closed) is True
            assert isinstance(lock, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, lock.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider` but received ''"):
            await async_client.users.locks.with_raw_response.create(
                username="USERNAME",
                provider="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `username` but received ''"):
            await async_client.users.locks.with_raw_response.create(
                username="",
                provider="PROVIDER",
            )
