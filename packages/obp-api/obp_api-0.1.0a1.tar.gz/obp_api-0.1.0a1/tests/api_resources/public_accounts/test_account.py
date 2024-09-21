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


class TestAccount:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/public/accounts/ACCOUNT_ID/VIEW_ID/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account = client.public_accounts.account.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert account.is_closed
        assert account.json() == {"foo": "bar"}
        assert cast(Any, account.is_closed) is True
        assert isinstance(account, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/public/accounts/ACCOUNT_ID/VIEW_ID/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account = client.public_accounts.account.with_raw_response.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert account.is_closed is True
        assert account.http_request.headers.get("X-Stainless-Lang") == "python"
        assert account.json() == {"foo": "bar"}
        assert isinstance(account, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/public/accounts/ACCOUNT_ID/VIEW_ID/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.public_accounts.account.with_streaming_response.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as account:
            assert not account.is_closed
            assert account.http_request.headers.get("X-Stainless-Lang") == "python"

            assert account.json() == {"foo": "bar"}
            assert cast(Any, account.is_closed) is True
            assert isinstance(account, StreamedBinaryAPIResponse)

        assert cast(Any, account.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.public_accounts.account.with_raw_response.retrieve(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.public_accounts.account.with_raw_response.retrieve(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.public_accounts.account.with_raw_response.retrieve(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )


class TestAsyncAccount:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/public/accounts/ACCOUNT_ID/VIEW_ID/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account = await async_client.public_accounts.account.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert account.is_closed
        assert await account.json() == {"foo": "bar"}
        assert cast(Any, account.is_closed) is True
        assert isinstance(account, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/public/accounts/ACCOUNT_ID/VIEW_ID/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account = await async_client.public_accounts.account.with_raw_response.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert account.is_closed is True
        assert account.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await account.json() == {"foo": "bar"}
        assert isinstance(account, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/public/accounts/ACCOUNT_ID/VIEW_ID/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.public_accounts.account.with_streaming_response.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as account:
            assert not account.is_closed
            assert account.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await account.json() == {"foo": "bar"}
            assert cast(Any, account.is_closed) is True
            assert isinstance(account, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, account.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.public_accounts.account.with_raw_response.retrieve(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.public_accounts.account.with_raw_response.retrieve(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.public_accounts.account.with_raw_response.retrieve(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )
