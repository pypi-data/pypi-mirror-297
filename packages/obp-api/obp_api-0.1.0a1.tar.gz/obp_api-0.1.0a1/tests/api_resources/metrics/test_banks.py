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
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/banks/BANK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        bank = client.metrics.banks.retrieve(
            "BANK_ID",
        )
        assert bank.is_closed
        assert bank.json() == {"foo": "bar"}
        assert cast(Any, bank.is_closed) is True
        assert isinstance(bank, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/banks/BANK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        bank = client.metrics.banks.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert bank.is_closed is True
        assert bank.http_request.headers.get("X-Stainless-Lang") == "python"
        assert bank.json() == {"foo": "bar"}
        assert isinstance(bank, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/banks/BANK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.metrics.banks.with_streaming_response.retrieve(
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
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.metrics.banks.with_raw_response.retrieve(
                "",
            )


class TestAsyncBanks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/banks/BANK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        bank = await async_client.metrics.banks.retrieve(
            "BANK_ID",
        )
        assert bank.is_closed
        assert await bank.json() == {"foo": "bar"}
        assert cast(Any, bank.is_closed) is True
        assert isinstance(bank, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/banks/BANK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        bank = await async_client.metrics.banks.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert bank.is_closed is True
        assert bank.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await bank.json() == {"foo": "bar"}
        assert isinstance(bank, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/metrics/banks/BANK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.metrics.banks.with_streaming_response.retrieve(
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
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.metrics.banks.with_raw_response.retrieve(
                "",
            )
