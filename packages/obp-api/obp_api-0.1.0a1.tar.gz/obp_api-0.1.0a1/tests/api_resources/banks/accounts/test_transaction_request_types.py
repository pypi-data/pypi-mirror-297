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


class TestTransactionRequestTypes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-request-types").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        transaction_request_type = client.banks.accounts.transaction_request_types.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert transaction_request_type.is_closed
        assert transaction_request_type.json() == {"foo": "bar"}
        assert cast(Any, transaction_request_type.is_closed) is True
        assert isinstance(transaction_request_type, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-request-types").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        transaction_request_type = client.banks.accounts.transaction_request_types.with_raw_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert transaction_request_type.is_closed is True
        assert transaction_request_type.http_request.headers.get("X-Stainless-Lang") == "python"
        assert transaction_request_type.json() == {"foo": "bar"}
        assert isinstance(transaction_request_type, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-request-types").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.accounts.transaction_request_types.with_streaming_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as transaction_request_type:
            assert not transaction_request_type.is_closed
            assert transaction_request_type.http_request.headers.get("X-Stainless-Lang") == "python"

            assert transaction_request_type.json() == {"foo": "bar"}
            assert cast(Any, transaction_request_type.is_closed) is True
            assert isinstance(transaction_request_type, StreamedBinaryAPIResponse)

        assert cast(Any, transaction_request_type.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.transaction_request_types.with_raw_response.list(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.transaction_request_types.with_raw_response.list(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.transaction_request_types.with_raw_response.list(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )


class TestAsyncTransactionRequestTypes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-request-types").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        transaction_request_type = await async_client.banks.accounts.transaction_request_types.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert transaction_request_type.is_closed
        assert await transaction_request_type.json() == {"foo": "bar"}
        assert cast(Any, transaction_request_type.is_closed) is True
        assert isinstance(transaction_request_type, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-request-types").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        transaction_request_type = await async_client.banks.accounts.transaction_request_types.with_raw_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert transaction_request_type.is_closed is True
        assert transaction_request_type.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await transaction_request_type.json() == {"foo": "bar"}
        assert isinstance(transaction_request_type, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-request-types").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.accounts.transaction_request_types.with_streaming_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as transaction_request_type:
            assert not transaction_request_type.is_closed
            assert transaction_request_type.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await transaction_request_type.json() == {"foo": "bar"}
            assert cast(Any, transaction_request_type.is_closed) is True
            assert isinstance(transaction_request_type, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, transaction_request_type.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.transaction_request_types.with_raw_response.list(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.transaction_request_types.with_raw_response.list(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.transaction_request_types.with_raw_response.list(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )
