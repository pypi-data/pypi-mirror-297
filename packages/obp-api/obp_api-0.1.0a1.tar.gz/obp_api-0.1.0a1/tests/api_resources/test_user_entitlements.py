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


class TestUserEntitlements:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/user-entitlements").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        user_entitlement = client.user_entitlements.create(
            body={},
        )
        assert user_entitlement.is_closed
        assert user_entitlement.json() == {"foo": "bar"}
        assert cast(Any, user_entitlement.is_closed) is True
        assert isinstance(user_entitlement, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/user-entitlements").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        user_entitlement = client.user_entitlements.with_raw_response.create(
            body={},
        )

        assert user_entitlement.is_closed is True
        assert user_entitlement.http_request.headers.get("X-Stainless-Lang") == "python"
        assert user_entitlement.json() == {"foo": "bar"}
        assert isinstance(user_entitlement, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/user-entitlements").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.user_entitlements.with_streaming_response.create(
            body={},
        ) as user_entitlement:
            assert not user_entitlement.is_closed
            assert user_entitlement.http_request.headers.get("X-Stainless-Lang") == "python"

            assert user_entitlement.json() == {"foo": "bar"}
            assert cast(Any, user_entitlement.is_closed) is True
            assert isinstance(user_entitlement, StreamedBinaryAPIResponse)

        assert cast(Any, user_entitlement.is_closed) is True


class TestAsyncUserEntitlements:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/user-entitlements").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        user_entitlement = await async_client.user_entitlements.create(
            body={},
        )
        assert user_entitlement.is_closed
        assert await user_entitlement.json() == {"foo": "bar"}
        assert cast(Any, user_entitlement.is_closed) is True
        assert isinstance(user_entitlement, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/user-entitlements").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        user_entitlement = await async_client.user_entitlements.with_raw_response.create(
            body={},
        )

        assert user_entitlement.is_closed is True
        assert user_entitlement.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await user_entitlement.json() == {"foo": "bar"}
        assert isinstance(user_entitlement, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/user-entitlements").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.user_entitlements.with_streaming_response.create(
            body={},
        ) as user_entitlement:
            assert not user_entitlement.is_closed
            assert user_entitlement.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await user_entitlement.json() == {"foo": "bar"}
            assert cast(Any, user_entitlement.is_closed) is True
            assert isinstance(user_entitlement, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, user_entitlement.is_closed) is True
