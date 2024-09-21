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


class TestSupportedCurrencies:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/supported-currencies").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        supported_currency = client.banks.atms.supported_currencies.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert supported_currency.is_closed
        assert supported_currency.json() == {"foo": "bar"}
        assert cast(Any, supported_currency.is_closed) is True
        assert isinstance(supported_currency, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/supported-currencies").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        supported_currency = client.banks.atms.supported_currencies.with_raw_response.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert supported_currency.is_closed is True
        assert supported_currency.http_request.headers.get("X-Stainless-Lang") == "python"
        assert supported_currency.json() == {"foo": "bar"}
        assert isinstance(supported_currency, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/supported-currencies").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.atms.supported_currencies.with_streaming_response.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        ) as supported_currency:
            assert not supported_currency.is_closed
            assert supported_currency.http_request.headers.get("X-Stainless-Lang") == "python"

            assert supported_currency.json() == {"foo": "bar"}
            assert cast(Any, supported_currency.is_closed) is True
            assert isinstance(supported_currency, StreamedBinaryAPIResponse)

        assert cast(Any, supported_currency.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.atms.supported_currencies.with_raw_response.update(
                atm_id="ATM_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `atm_id` but received ''"):
            client.banks.atms.supported_currencies.with_raw_response.update(
                atm_id="",
                bank_id="BANK_ID",
                body={},
            )


class TestAsyncSupportedCurrencies:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/supported-currencies").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        supported_currency = await async_client.banks.atms.supported_currencies.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert supported_currency.is_closed
        assert await supported_currency.json() == {"foo": "bar"}
        assert cast(Any, supported_currency.is_closed) is True
        assert isinstance(supported_currency, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/supported-currencies").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        supported_currency = await async_client.banks.atms.supported_currencies.with_raw_response.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert supported_currency.is_closed is True
        assert supported_currency.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await supported_currency.json() == {"foo": "bar"}
        assert isinstance(supported_currency, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/supported-currencies").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.atms.supported_currencies.with_streaming_response.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        ) as supported_currency:
            assert not supported_currency.is_closed
            assert supported_currency.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await supported_currency.json() == {"foo": "bar"}
            assert cast(Any, supported_currency.is_closed) is True
            assert isinstance(supported_currency, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, supported_currency.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.atms.supported_currencies.with_raw_response.update(
                atm_id="ATM_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `atm_id` but received ''"):
            await async_client.banks.atms.supported_currencies.with_raw_response.update(
                atm_id="",
                bank_id="BANK_ID",
                body={},
            )
