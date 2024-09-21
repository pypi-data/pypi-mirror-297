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


class TestUserAccountAccess:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/user-account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        user_account_access = client.accounts.views.user_account_access.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert user_account_access.is_closed
        assert user_account_access.json() == {"foo": "bar"}
        assert cast(Any, user_account_access.is_closed) is True
        assert isinstance(user_account_access, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/user-account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        user_account_access = client.accounts.views.user_account_access.with_raw_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert user_account_access.is_closed is True
        assert user_account_access.http_request.headers.get("X-Stainless-Lang") == "python"
        assert user_account_access.json() == {"foo": "bar"}
        assert isinstance(user_account_access, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/user-account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.accounts.views.user_account_access.with_streaming_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as user_account_access:
            assert not user_account_access.is_closed
            assert user_account_access.http_request.headers.get("X-Stainless-Lang") == "python"

            assert user_account_access.json() == {"foo": "bar"}
            assert cast(Any, user_account_access.is_closed) is True
            assert isinstance(user_account_access, StreamedBinaryAPIResponse)

        assert cast(Any, user_account_access.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.user_account_access.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.user_account_access.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.user_account_access.with_raw_response.create(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )


class TestAsyncUserAccountAccess:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/user-account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        user_account_access = await async_client.accounts.views.user_account_access.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert user_account_access.is_closed
        assert await user_account_access.json() == {"foo": "bar"}
        assert cast(Any, user_account_access.is_closed) is True
        assert isinstance(user_account_access, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/user-account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        user_account_access = await async_client.accounts.views.user_account_access.with_raw_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert user_account_access.is_closed is True
        assert user_account_access.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await user_account_access.json() == {"foo": "bar"}
        assert isinstance(user_account_access, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/user-account-access").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.accounts.views.user_account_access.with_streaming_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as user_account_access:
            assert not user_account_access.is_closed
            assert user_account_access.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await user_account_access.json() == {"foo": "bar"}
            assert cast(Any, user_account_access.is_closed) is True
            assert isinstance(user_account_access, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, user_account_access.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.user_account_access.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.user_account_access.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.user_account_access.with_raw_response.create(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )
