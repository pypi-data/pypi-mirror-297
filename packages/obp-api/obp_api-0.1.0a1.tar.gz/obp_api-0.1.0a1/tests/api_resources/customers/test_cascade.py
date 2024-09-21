# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from obp_api import ObpAPI, AsyncObpAPI

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCascade:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        cascade = client.customers.cascade.delete(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert cascade is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.customers.cascade.with_raw_response.delete(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        cascade = response.parse()
        assert cascade is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.customers.cascade.with_streaming_response.delete(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            cascade = response.parse()
            assert cascade is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.cascade.with_raw_response.delete(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.cascade.with_raw_response.delete(
                customer_id="",
                bank_id="BANK_ID",
            )


class TestAsyncCascade:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        cascade = await async_client.customers.cascade.delete(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert cascade is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.customers.cascade.with_raw_response.delete(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        cascade = await response.parse()
        assert cascade is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.customers.cascade.with_streaming_response.delete(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            cascade = await response.parse()
            assert cascade is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.cascade.with_raw_response.delete(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.cascade.with_raw_response.delete(
                customer_id="",
                bank_id="BANK_ID",
            )
