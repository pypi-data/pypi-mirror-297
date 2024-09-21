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


class TestCounterpartyNames:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/management/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/counterparty-names/COUNTERPARTY_NAME"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        counterparty_name = client.banks.accounts.counterparty_names.retrieve(
            counterparty_name="COUNTERPARTY_NAME",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert counterparty_name.is_closed
        assert counterparty_name.json() == {"foo": "bar"}
        assert cast(Any, counterparty_name.is_closed) is True
        assert isinstance(counterparty_name, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/management/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/counterparty-names/COUNTERPARTY_NAME"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        counterparty_name = client.banks.accounts.counterparty_names.with_raw_response.retrieve(
            counterparty_name="COUNTERPARTY_NAME",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert counterparty_name.is_closed is True
        assert counterparty_name.http_request.headers.get("X-Stainless-Lang") == "python"
        assert counterparty_name.json() == {"foo": "bar"}
        assert isinstance(counterparty_name, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/management/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/counterparty-names/COUNTERPARTY_NAME"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.accounts.counterparty_names.with_streaming_response.retrieve(
            counterparty_name="COUNTERPARTY_NAME",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as counterparty_name:
            assert not counterparty_name.is_closed
            assert counterparty_name.http_request.headers.get("X-Stainless-Lang") == "python"

            assert counterparty_name.json() == {"foo": "bar"}
            assert cast(Any, counterparty_name.is_closed) is True
            assert isinstance(counterparty_name, StreamedBinaryAPIResponse)

        assert cast(Any, counterparty_name.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.counterparty_names.with_raw_response.retrieve(
                counterparty_name="COUNTERPARTY_NAME",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.counterparty_names.with_raw_response.retrieve(
                counterparty_name="COUNTERPARTY_NAME",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.counterparty_names.with_raw_response.retrieve(
                counterparty_name="COUNTERPARTY_NAME",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `counterparty_name` but received ''"):
            client.banks.accounts.counterparty_names.with_raw_response.retrieve(
                counterparty_name="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )


class TestAsyncCounterpartyNames:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/management/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/counterparty-names/COUNTERPARTY_NAME"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        counterparty_name = await async_client.banks.accounts.counterparty_names.retrieve(
            counterparty_name="COUNTERPARTY_NAME",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert counterparty_name.is_closed
        assert await counterparty_name.json() == {"foo": "bar"}
        assert cast(Any, counterparty_name.is_closed) is True
        assert isinstance(counterparty_name, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/management/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/counterparty-names/COUNTERPARTY_NAME"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        counterparty_name = await async_client.banks.accounts.counterparty_names.with_raw_response.retrieve(
            counterparty_name="COUNTERPARTY_NAME",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert counterparty_name.is_closed is True
        assert counterparty_name.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await counterparty_name.json() == {"foo": "bar"}
        assert isinstance(counterparty_name, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/management/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/counterparty-names/COUNTERPARTY_NAME"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.accounts.counterparty_names.with_streaming_response.retrieve(
            counterparty_name="COUNTERPARTY_NAME",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as counterparty_name:
            assert not counterparty_name.is_closed
            assert counterparty_name.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await counterparty_name.json() == {"foo": "bar"}
            assert cast(Any, counterparty_name.is_closed) is True
            assert isinstance(counterparty_name, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, counterparty_name.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.counterparty_names.with_raw_response.retrieve(
                counterparty_name="COUNTERPARTY_NAME",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.counterparty_names.with_raw_response.retrieve(
                counterparty_name="COUNTERPARTY_NAME",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.counterparty_names.with_raw_response.retrieve(
                counterparty_name="COUNTERPARTY_NAME",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `counterparty_name` but received ''"):
            await async_client.banks.accounts.counterparty_names.with_raw_response.retrieve(
                counterparty_name="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )
