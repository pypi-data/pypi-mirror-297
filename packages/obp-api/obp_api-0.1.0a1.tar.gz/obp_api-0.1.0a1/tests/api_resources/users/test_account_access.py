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


class TestAccountAccess:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/USER_ID/account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account_access = client.users.account_access.list(
            "USER_ID",
        )
        assert account_access.is_closed
        assert account_access.json() == {"foo": "bar"}
        assert cast(Any, account_access.is_closed) is True
        assert isinstance(account_access, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/USER_ID/account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account_access = client.users.account_access.with_raw_response.list(
            "USER_ID",
        )

        assert account_access.is_closed is True
        assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"
        assert account_access.json() == {"foo": "bar"}
        assert isinstance(account_access, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/USER_ID/account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.users.account_access.with_streaming_response.list(
            "USER_ID",
        ) as account_access:
            assert not account_access.is_closed
            assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"

            assert account_access.json() == {"foo": "bar"}
            assert cast(Any, account_access.is_closed) is True
            assert isinstance(account_access, StreamedBinaryAPIResponse)

        assert cast(Any, account_access.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.account_access.with_raw_response.list(
                "",
            )


class TestAsyncAccountAccess:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/USER_ID/account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account_access = await async_client.users.account_access.list(
            "USER_ID",
        )
        assert account_access.is_closed
        assert await account_access.json() == {"foo": "bar"}
        assert cast(Any, account_access.is_closed) is True
        assert isinstance(account_access, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/USER_ID/account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account_access = await async_client.users.account_access.with_raw_response.list(
            "USER_ID",
        )

        assert account_access.is_closed is True
        assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await account_access.json() == {"foo": "bar"}
        assert isinstance(account_access, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users/USER_ID/account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.users.account_access.with_streaming_response.list(
            "USER_ID",
        ) as account_access:
            assert not account_access.is_closed
            assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await account_access.json() == {"foo": "bar"}
            assert cast(Any, account_access.is_closed) is True
            assert isinstance(account_access, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, account_access.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.account_access.with_raw_response.list(
                "",
            )
