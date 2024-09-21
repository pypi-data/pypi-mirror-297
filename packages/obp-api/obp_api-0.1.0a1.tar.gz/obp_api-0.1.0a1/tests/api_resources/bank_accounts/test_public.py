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


class TestPublic:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/public").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        public = client.bank_accounts.public.list(
            "BANK_ID",
        )
        assert public.is_closed
        assert public.json() == {"foo": "bar"}
        assert cast(Any, public.is_closed) is True
        assert isinstance(public, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/public").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        public = client.bank_accounts.public.with_raw_response.list(
            "BANK_ID",
        )

        assert public.is_closed is True
        assert public.http_request.headers.get("X-Stainless-Lang") == "python"
        assert public.json() == {"foo": "bar"}
        assert isinstance(public, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/public").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.bank_accounts.public.with_streaming_response.list(
            "BANK_ID",
        ) as public:
            assert not public.is_closed
            assert public.http_request.headers.get("X-Stainless-Lang") == "python"

            assert public.json() == {"foo": "bar"}
            assert cast(Any, public.is_closed) is True
            assert isinstance(public, StreamedBinaryAPIResponse)

        assert cast(Any, public.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.bank_accounts.public.with_raw_response.list(
                "",
            )


class TestAsyncPublic:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/public").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        public = await async_client.bank_accounts.public.list(
            "BANK_ID",
        )
        assert public.is_closed
        assert await public.json() == {"foo": "bar"}
        assert cast(Any, public.is_closed) is True
        assert isinstance(public, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/public").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        public = await async_client.bank_accounts.public.with_raw_response.list(
            "BANK_ID",
        )

        assert public.is_closed is True
        assert public.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await public.json() == {"foo": "bar"}
        assert isinstance(public, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/public").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.bank_accounts.public.with_streaming_response.list(
            "BANK_ID",
        ) as public:
            assert not public.is_closed
            assert public.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await public.json() == {"foo": "bar"}
            assert cast(Any, public.is_closed) is True
            assert isinstance(public, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, public.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.bank_accounts.public.with_raw_response.list(
                "",
            )
