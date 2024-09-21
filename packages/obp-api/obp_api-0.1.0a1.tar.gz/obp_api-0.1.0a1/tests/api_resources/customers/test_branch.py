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


class TestBranch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/branch").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        branch = client.customers.branch.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert branch.is_closed
        assert branch.json() == {"foo": "bar"}
        assert cast(Any, branch.is_closed) is True
        assert isinstance(branch, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/branch").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        branch = client.customers.branch.with_raw_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert branch.is_closed is True
        assert branch.http_request.headers.get("X-Stainless-Lang") == "python"
        assert branch.json() == {"foo": "bar"}
        assert isinstance(branch, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/branch").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.branch.with_streaming_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as branch:
            assert not branch.is_closed
            assert branch.http_request.headers.get("X-Stainless-Lang") == "python"

            assert branch.json() == {"foo": "bar"}
            assert cast(Any, branch.is_closed) is True
            assert isinstance(branch, StreamedBinaryAPIResponse)

        assert cast(Any, branch.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.branch.with_raw_response.update(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.branch.with_raw_response.update(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )


class TestAsyncBranch:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/branch").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        branch = await async_client.customers.branch.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert branch.is_closed
        assert await branch.json() == {"foo": "bar"}
        assert cast(Any, branch.is_closed) is True
        assert isinstance(branch, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/branch").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        branch = await async_client.customers.branch.with_raw_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert branch.is_closed is True
        assert branch.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await branch.json() == {"foo": "bar"}
        assert isinstance(branch, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/branch").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.branch.with_streaming_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as branch:
            assert not branch.is_closed
            assert branch.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await branch.json() == {"foo": "bar"}
            assert cast(Any, branch.is_closed) is True
            assert isinstance(branch, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, branch.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.branch.with_raw_response.update(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.branch.with_raw_response.update(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )
