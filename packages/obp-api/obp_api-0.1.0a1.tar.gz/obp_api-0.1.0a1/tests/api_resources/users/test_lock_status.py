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


class TestLockStatus:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        lock_status = client.users.lock_status.retrieve(
            username="USERNAME",
            provider="PROVIDER",
        )
        assert lock_status.is_closed
        assert lock_status.json() == {"foo": "bar"}
        assert cast(Any, lock_status.is_closed) is True
        assert isinstance(lock_status, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        lock_status = client.users.lock_status.with_raw_response.retrieve(
            username="USERNAME",
            provider="PROVIDER",
        )

        assert lock_status.is_closed is True
        assert lock_status.http_request.headers.get("X-Stainless-Lang") == "python"
        assert lock_status.json() == {"foo": "bar"}
        assert isinstance(lock_status, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.users.lock_status.with_streaming_response.retrieve(
            username="USERNAME",
            provider="PROVIDER",
        ) as lock_status:
            assert not lock_status.is_closed
            assert lock_status.http_request.headers.get("X-Stainless-Lang") == "python"

            assert lock_status.json() == {"foo": "bar"}
            assert cast(Any, lock_status.is_closed) is True
            assert isinstance(lock_status, StreamedBinaryAPIResponse)

        assert cast(Any, lock_status.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider` but received ''"):
            client.users.lock_status.with_raw_response.retrieve(
                username="USERNAME",
                provider="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `username` but received ''"):
            client.users.lock_status.with_raw_response.retrieve(
                username="",
                provider="PROVIDER",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        lock_status = client.users.lock_status.update(
            username="USERNAME",
            provider="PROVIDER",
        )
        assert lock_status.is_closed
        assert lock_status.json() == {"foo": "bar"}
        assert cast(Any, lock_status.is_closed) is True
        assert isinstance(lock_status, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        lock_status = client.users.lock_status.with_raw_response.update(
            username="USERNAME",
            provider="PROVIDER",
        )

        assert lock_status.is_closed is True
        assert lock_status.http_request.headers.get("X-Stainless-Lang") == "python"
        assert lock_status.json() == {"foo": "bar"}
        assert isinstance(lock_status, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.users.lock_status.with_streaming_response.update(
            username="USERNAME",
            provider="PROVIDER",
        ) as lock_status:
            assert not lock_status.is_closed
            assert lock_status.http_request.headers.get("X-Stainless-Lang") == "python"

            assert lock_status.json() == {"foo": "bar"}
            assert cast(Any, lock_status.is_closed) is True
            assert isinstance(lock_status, StreamedBinaryAPIResponse)

        assert cast(Any, lock_status.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider` but received ''"):
            client.users.lock_status.with_raw_response.update(
                username="USERNAME",
                provider="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `username` but received ''"):
            client.users.lock_status.with_raw_response.update(
                username="",
                provider="PROVIDER",
            )


class TestAsyncLockStatus:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        lock_status = await async_client.users.lock_status.retrieve(
            username="USERNAME",
            provider="PROVIDER",
        )
        assert lock_status.is_closed
        assert await lock_status.json() == {"foo": "bar"}
        assert cast(Any, lock_status.is_closed) is True
        assert isinstance(lock_status, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        lock_status = await async_client.users.lock_status.with_raw_response.retrieve(
            username="USERNAME",
            provider="PROVIDER",
        )

        assert lock_status.is_closed is True
        assert lock_status.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await lock_status.json() == {"foo": "bar"}
        assert isinstance(lock_status, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.users.lock_status.with_streaming_response.retrieve(
            username="USERNAME",
            provider="PROVIDER",
        ) as lock_status:
            assert not lock_status.is_closed
            assert lock_status.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await lock_status.json() == {"foo": "bar"}
            assert cast(Any, lock_status.is_closed) is True
            assert isinstance(lock_status, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, lock_status.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider` but received ''"):
            await async_client.users.lock_status.with_raw_response.retrieve(
                username="USERNAME",
                provider="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `username` but received ''"):
            await async_client.users.lock_status.with_raw_response.retrieve(
                username="",
                provider="PROVIDER",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        lock_status = await async_client.users.lock_status.update(
            username="USERNAME",
            provider="PROVIDER",
        )
        assert lock_status.is_closed
        assert await lock_status.json() == {"foo": "bar"}
        assert cast(Any, lock_status.is_closed) is True
        assert isinstance(lock_status, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        lock_status = await async_client.users.lock_status.with_raw_response.update(
            username="USERNAME",
            provider="PROVIDER",
        )

        assert lock_status.is_closed is True
        assert lock_status.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await lock_status.json() == {"foo": "bar"}
        assert isinstance(lock_status, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/users/PROVIDER/USERNAME/lock-status").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.users.lock_status.with_streaming_response.update(
            username="USERNAME",
            provider="PROVIDER",
        ) as lock_status:
            assert not lock_status.is_closed
            assert lock_status.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await lock_status.json() == {"foo": "bar"}
            assert cast(Any, lock_status.is_closed) is True
            assert isinstance(lock_status, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, lock_status.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider` but received ''"):
            await async_client.users.lock_status.with_raw_response.update(
                username="USERNAME",
                provider="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `username` but received ''"):
            await async_client.users.lock_status.with_raw_response.update(
                username="",
                provider="PROVIDER",
            )
