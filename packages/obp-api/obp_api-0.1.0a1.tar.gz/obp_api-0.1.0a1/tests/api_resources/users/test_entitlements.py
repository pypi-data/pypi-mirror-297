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


class TestEntitlements:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/users/USER_ID/entitlements").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        entitlement = client.users.entitlements.list(
            user_id="USER_ID",
            bank_id="BANK_ID",
        )
        assert entitlement.is_closed
        assert entitlement.json() == {"foo": "bar"}
        assert cast(Any, entitlement.is_closed) is True
        assert isinstance(entitlement, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/users/USER_ID/entitlements").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        entitlement = client.users.entitlements.with_raw_response.list(
            user_id="USER_ID",
            bank_id="BANK_ID",
        )

        assert entitlement.is_closed is True
        assert entitlement.http_request.headers.get("X-Stainless-Lang") == "python"
        assert entitlement.json() == {"foo": "bar"}
        assert isinstance(entitlement, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/users/USER_ID/entitlements").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.users.entitlements.with_streaming_response.list(
            user_id="USER_ID",
            bank_id="BANK_ID",
        ) as entitlement:
            assert not entitlement.is_closed
            assert entitlement.http_request.headers.get("X-Stainless-Lang") == "python"

            assert entitlement.json() == {"foo": "bar"}
            assert cast(Any, entitlement.is_closed) is True
            assert isinstance(entitlement, StreamedBinaryAPIResponse)

        assert cast(Any, entitlement.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.users.entitlements.with_raw_response.list(
                user_id="USER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.entitlements.with_raw_response.list(
                user_id="",
                bank_id="BANK_ID",
            )


class TestAsyncEntitlements:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/users/USER_ID/entitlements").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        entitlement = await async_client.users.entitlements.list(
            user_id="USER_ID",
            bank_id="BANK_ID",
        )
        assert entitlement.is_closed
        assert await entitlement.json() == {"foo": "bar"}
        assert cast(Any, entitlement.is_closed) is True
        assert isinstance(entitlement, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/users/USER_ID/entitlements").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        entitlement = await async_client.users.entitlements.with_raw_response.list(
            user_id="USER_ID",
            bank_id="BANK_ID",
        )

        assert entitlement.is_closed is True
        assert entitlement.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await entitlement.json() == {"foo": "bar"}
        assert isinstance(entitlement, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/users/USER_ID/entitlements").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.users.entitlements.with_streaming_response.list(
            user_id="USER_ID",
            bank_id="BANK_ID",
        ) as entitlement:
            assert not entitlement.is_closed
            assert entitlement.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await entitlement.json() == {"foo": "bar"}
            assert cast(Any, entitlement.is_closed) is True
            assert isinstance(entitlement, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, entitlement.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.users.entitlements.with_raw_response.list(
                user_id="USER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.entitlements.with_raw_response.list(
                user_id="",
                bank_id="BANK_ID",
            )
