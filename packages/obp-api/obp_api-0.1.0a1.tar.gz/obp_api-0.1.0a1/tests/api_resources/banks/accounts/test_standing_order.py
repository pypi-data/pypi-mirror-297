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


class TestStandingOrder:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/standing-order").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        standing_order = client.banks.accounts.standing_order.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert standing_order.is_closed
        assert standing_order.json() == {"foo": "bar"}
        assert cast(Any, standing_order.is_closed) is True
        assert isinstance(standing_order, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/standing-order").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        standing_order = client.banks.accounts.standing_order.with_raw_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert standing_order.is_closed is True
        assert standing_order.http_request.headers.get("X-Stainless-Lang") == "python"
        assert standing_order.json() == {"foo": "bar"}
        assert isinstance(standing_order, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/standing-order").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.accounts.standing_order.with_streaming_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as standing_order:
            assert not standing_order.is_closed
            assert standing_order.http_request.headers.get("X-Stainless-Lang") == "python"

            assert standing_order.json() == {"foo": "bar"}
            assert cast(Any, standing_order.is_closed) is True
            assert isinstance(standing_order, StreamedBinaryAPIResponse)

        assert cast(Any, standing_order.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.standing_order.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.standing_order.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.standing_order.with_raw_response.create(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )


class TestAsyncStandingOrder:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/standing-order").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        standing_order = await async_client.banks.accounts.standing_order.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert standing_order.is_closed
        assert await standing_order.json() == {"foo": "bar"}
        assert cast(Any, standing_order.is_closed) is True
        assert isinstance(standing_order, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/standing-order").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        standing_order = await async_client.banks.accounts.standing_order.with_raw_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert standing_order.is_closed is True
        assert standing_order.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await standing_order.json() == {"foo": "bar"}
        assert isinstance(standing_order, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/standing-order").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.accounts.standing_order.with_streaming_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as standing_order:
            assert not standing_order.is_closed
            assert standing_order.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await standing_order.json() == {"foo": "bar"}
            assert cast(Any, standing_order.is_closed) is True
            assert isinstance(standing_order, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, standing_order.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.standing_order.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.standing_order.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.standing_order.with_raw_response.create(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )
