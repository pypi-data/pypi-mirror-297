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


class TestBanks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_account_currency_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/account-currency-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        bank = client.system_integrity.banks.account_currency_check(
            "BANK_ID",
        )
        assert bank.is_closed
        assert bank.json() == {"foo": "bar"}
        assert cast(Any, bank.is_closed) is True
        assert isinstance(bank, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_account_currency_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/account-currency-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        bank = client.system_integrity.banks.with_raw_response.account_currency_check(
            "BANK_ID",
        )

        assert bank.is_closed is True
        assert bank.http_request.headers.get("X-Stainless-Lang") == "python"
        assert bank.json() == {"foo": "bar"}
        assert isinstance(bank, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_account_currency_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/account-currency-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.system_integrity.banks.with_streaming_response.account_currency_check(
            "BANK_ID",
        ) as bank:
            assert not bank.is_closed
            assert bank.http_request.headers.get("X-Stainless-Lang") == "python"

            assert bank.json() == {"foo": "bar"}
            assert cast(Any, bank.is_closed) is True
            assert isinstance(bank, StreamedBinaryAPIResponse)

        assert cast(Any, bank.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_account_currency_check(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.system_integrity.banks.with_raw_response.account_currency_check(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_orphaned_account_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/orphaned-account-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        bank = client.system_integrity.banks.orphaned_account_check(
            "BANK_ID",
        )
        assert bank.is_closed
        assert bank.json() == {"foo": "bar"}
        assert cast(Any, bank.is_closed) is True
        assert isinstance(bank, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_orphaned_account_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/orphaned-account-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        bank = client.system_integrity.banks.with_raw_response.orphaned_account_check(
            "BANK_ID",
        )

        assert bank.is_closed is True
        assert bank.http_request.headers.get("X-Stainless-Lang") == "python"
        assert bank.json() == {"foo": "bar"}
        assert isinstance(bank, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_orphaned_account_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/orphaned-account-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.system_integrity.banks.with_streaming_response.orphaned_account_check(
            "BANK_ID",
        ) as bank:
            assert not bank.is_closed
            assert bank.http_request.headers.get("X-Stainless-Lang") == "python"

            assert bank.json() == {"foo": "bar"}
            assert cast(Any, bank.is_closed) is True
            assert isinstance(bank, StreamedBinaryAPIResponse)

        assert cast(Any, bank.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_orphaned_account_check(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.system_integrity.banks.with_raw_response.orphaned_account_check(
                "",
            )


class TestAsyncBanks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_account_currency_check(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/account-currency-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        bank = await async_client.system_integrity.banks.account_currency_check(
            "BANK_ID",
        )
        assert bank.is_closed
        assert await bank.json() == {"foo": "bar"}
        assert cast(Any, bank.is_closed) is True
        assert isinstance(bank, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_account_currency_check(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/account-currency-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        bank = await async_client.system_integrity.banks.with_raw_response.account_currency_check(
            "BANK_ID",
        )

        assert bank.is_closed is True
        assert bank.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await bank.json() == {"foo": "bar"}
        assert isinstance(bank, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_account_currency_check(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/account-currency-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.system_integrity.banks.with_streaming_response.account_currency_check(
            "BANK_ID",
        ) as bank:
            assert not bank.is_closed
            assert bank.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await bank.json() == {"foo": "bar"}
            assert cast(Any, bank.is_closed) is True
            assert isinstance(bank, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, bank.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_account_currency_check(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.system_integrity.banks.with_raw_response.account_currency_check(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_orphaned_account_check(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/orphaned-account-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        bank = await async_client.system_integrity.banks.orphaned_account_check(
            "BANK_ID",
        )
        assert bank.is_closed
        assert await bank.json() == {"foo": "bar"}
        assert cast(Any, bank.is_closed) is True
        assert isinstance(bank, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_orphaned_account_check(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/orphaned-account-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        bank = await async_client.system_integrity.banks.with_raw_response.orphaned_account_check(
            "BANK_ID",
        )

        assert bank.is_closed is True
        assert bank.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await bank.json() == {"foo": "bar"}
        assert isinstance(bank, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_orphaned_account_check(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/banks/BANK_ID/orphaned-account-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.system_integrity.banks.with_streaming_response.orphaned_account_check(
            "BANK_ID",
        ) as bank:
            assert not bank.is_closed
            assert bank.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await bank.json() == {"foo": "bar"}
            assert cast(Any, bank.is_closed) is True
            assert isinstance(bank, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, bank.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_orphaned_account_check(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.system_integrity.banks.with_raw_response.orphaned_account_check(
                "",
            )
