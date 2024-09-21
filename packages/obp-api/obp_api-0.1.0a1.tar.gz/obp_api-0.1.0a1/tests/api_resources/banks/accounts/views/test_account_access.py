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
    def test_method_grant(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/grant").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account_access = client.banks.accounts.views.account_access.grant(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert account_access.is_closed
        assert account_access.json() == {"foo": "bar"}
        assert cast(Any, account_access.is_closed) is True
        assert isinstance(account_access, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_grant(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/grant").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account_access = client.banks.accounts.views.account_access.with_raw_response.grant(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert account_access.is_closed is True
        assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"
        assert account_access.json() == {"foo": "bar"}
        assert isinstance(account_access, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_grant(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/grant").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.accounts.views.account_access.with_streaming_response.grant(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as account_access:
            assert not account_access.is_closed
            assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"

            assert account_access.json() == {"foo": "bar"}
            assert cast(Any, account_access.is_closed) is True
            assert isinstance(account_access, StreamedBinaryAPIResponse)

        assert cast(Any, account_access.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_grant(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.views.account_access.with_raw_response.grant(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.views.account_access.with_raw_response.grant(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.views.account_access.with_raw_response.grant(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_revoke(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account_access = client.banks.accounts.views.account_access.revoke(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert account_access.is_closed
        assert account_access.json() == {"foo": "bar"}
        assert cast(Any, account_access.is_closed) is True
        assert isinstance(account_access, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_revoke(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account_access = client.banks.accounts.views.account_access.with_raw_response.revoke(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert account_access.is_closed is True
        assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"
        assert account_access.json() == {"foo": "bar"}
        assert isinstance(account_access, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_revoke(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.accounts.views.account_access.with_streaming_response.revoke(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as account_access:
            assert not account_access.is_closed
            assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"

            assert account_access.json() == {"foo": "bar"}
            assert cast(Any, account_access.is_closed) is True
            assert isinstance(account_access, StreamedBinaryAPIResponse)

        assert cast(Any, account_access.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_revoke(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.views.account_access.with_raw_response.revoke(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.views.account_access.with_raw_response.revoke(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.views.account_access.with_raw_response.revoke(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )


class TestAsyncAccountAccess:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_grant(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/grant").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account_access = await async_client.banks.accounts.views.account_access.grant(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert account_access.is_closed
        assert await account_access.json() == {"foo": "bar"}
        assert cast(Any, account_access.is_closed) is True
        assert isinstance(account_access, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_grant(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/grant").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account_access = await async_client.banks.accounts.views.account_access.with_raw_response.grant(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert account_access.is_closed is True
        assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await account_access.json() == {"foo": "bar"}
        assert isinstance(account_access, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_grant(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/grant").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.accounts.views.account_access.with_streaming_response.grant(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as account_access:
            assert not account_access.is_closed
            assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await account_access.json() == {"foo": "bar"}
            assert cast(Any, account_access.is_closed) is True
            assert isinstance(account_access, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, account_access.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_grant(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.views.account_access.with_raw_response.grant(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.views.account_access.with_raw_response.grant(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.views.account_access.with_raw_response.grant(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_revoke(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account_access = await async_client.banks.accounts.views.account_access.revoke(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert account_access.is_closed
        assert await account_access.json() == {"foo": "bar"}
        assert cast(Any, account_access.is_closed) is True
        assert isinstance(account_access, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_revoke(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account_access = await async_client.banks.accounts.views.account_access.with_raw_response.revoke(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert account_access.is_closed is True
        assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await account_access.json() == {"foo": "bar"}
        assert isinstance(account_access, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_revoke(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/account-access/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.accounts.views.account_access.with_streaming_response.revoke(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as account_access:
            assert not account_access.is_closed
            assert account_access.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await account_access.json() == {"foo": "bar"}
            assert cast(Any, account_access.is_closed) is True
            assert isinstance(account_access, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, account_access.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_revoke(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.views.account_access.with_raw_response.revoke(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.views.account_access.with_raw_response.revoke(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.views.account_access.with_raw_response.revoke(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )
