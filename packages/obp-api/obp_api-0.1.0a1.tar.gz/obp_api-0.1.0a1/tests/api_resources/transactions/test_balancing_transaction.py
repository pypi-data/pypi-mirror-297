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


class TestBalancingTransaction:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/transactions/TRANSACTION_ID/balancing-transaction").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        balancing_transaction = client.transactions.balancing_transaction.retrieve(
            "TRANSACTION_ID",
        )
        assert balancing_transaction.is_closed
        assert balancing_transaction.json() == {"foo": "bar"}
        assert cast(Any, balancing_transaction.is_closed) is True
        assert isinstance(balancing_transaction, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/transactions/TRANSACTION_ID/balancing-transaction").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        balancing_transaction = client.transactions.balancing_transaction.with_raw_response.retrieve(
            "TRANSACTION_ID",
        )

        assert balancing_transaction.is_closed is True
        assert balancing_transaction.http_request.headers.get("X-Stainless-Lang") == "python"
        assert balancing_transaction.json() == {"foo": "bar"}
        assert isinstance(balancing_transaction, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/transactions/TRANSACTION_ID/balancing-transaction").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.transactions.balancing_transaction.with_streaming_response.retrieve(
            "TRANSACTION_ID",
        ) as balancing_transaction:
            assert not balancing_transaction.is_closed
            assert balancing_transaction.http_request.headers.get("X-Stainless-Lang") == "python"

            assert balancing_transaction.json() == {"foo": "bar"}
            assert cast(Any, balancing_transaction.is_closed) is True
            assert isinstance(balancing_transaction, StreamedBinaryAPIResponse)

        assert cast(Any, balancing_transaction.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.balancing_transaction.with_raw_response.retrieve(
                "",
            )


class TestAsyncBalancingTransaction:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/transactions/TRANSACTION_ID/balancing-transaction").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        balancing_transaction = await async_client.transactions.balancing_transaction.retrieve(
            "TRANSACTION_ID",
        )
        assert balancing_transaction.is_closed
        assert await balancing_transaction.json() == {"foo": "bar"}
        assert cast(Any, balancing_transaction.is_closed) is True
        assert isinstance(balancing_transaction, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/transactions/TRANSACTION_ID/balancing-transaction").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        balancing_transaction = await async_client.transactions.balancing_transaction.with_raw_response.retrieve(
            "TRANSACTION_ID",
        )

        assert balancing_transaction.is_closed is True
        assert balancing_transaction.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await balancing_transaction.json() == {"foo": "bar"}
        assert isinstance(balancing_transaction, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/transactions/TRANSACTION_ID/balancing-transaction").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.transactions.balancing_transaction.with_streaming_response.retrieve(
            "TRANSACTION_ID",
        ) as balancing_transaction:
            assert not balancing_transaction.is_closed
            assert balancing_transaction.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await balancing_transaction.json() == {"foo": "bar"}
            assert cast(Any, balancing_transaction.is_closed) is True
            assert isinstance(balancing_transaction, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, balancing_transaction.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.balancing_transaction.with_raw_response.retrieve(
                "",
            )
