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


class TestTaxResidences:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residence").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tax_residence = client.customers.tax_residences.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert tax_residence.is_closed
        assert tax_residence.json() == {"foo": "bar"}
        assert cast(Any, tax_residence.is_closed) is True
        assert isinstance(tax_residence, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residence").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tax_residence = client.customers.tax_residences.with_raw_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert tax_residence.is_closed is True
        assert tax_residence.http_request.headers.get("X-Stainless-Lang") == "python"
        assert tax_residence.json() == {"foo": "bar"}
        assert isinstance(tax_residence, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residence").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.tax_residences.with_streaming_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as tax_residence:
            assert not tax_residence.is_closed
            assert tax_residence.http_request.headers.get("X-Stainless-Lang") == "python"

            assert tax_residence.json() == {"foo": "bar"}
            assert cast(Any, tax_residence.is_closed) is True
            assert isinstance(tax_residence, StreamedBinaryAPIResponse)

        assert cast(Any, tax_residence.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.tax_residences.with_raw_response.create(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.tax_residences.with_raw_response.create(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residences").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tax_residence = client.customers.tax_residences.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert tax_residence.is_closed
        assert tax_residence.json() == {"foo": "bar"}
        assert cast(Any, tax_residence.is_closed) is True
        assert isinstance(tax_residence, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residences").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tax_residence = client.customers.tax_residences.with_raw_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert tax_residence.is_closed is True
        assert tax_residence.http_request.headers.get("X-Stainless-Lang") == "python"
        assert tax_residence.json() == {"foo": "bar"}
        assert isinstance(tax_residence, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residences").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.tax_residences.with_streaming_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as tax_residence:
            assert not tax_residence.is_closed
            assert tax_residence.http_request.headers.get("X-Stainless-Lang") == "python"

            assert tax_residence.json() == {"foo": "bar"}
            assert cast(Any, tax_residence.is_closed) is True
            assert isinstance(tax_residence, StreamedBinaryAPIResponse)

        assert cast(Any, tax_residence.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.tax_residences.with_raw_response.list(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.tax_residences.with_raw_response.list(
                customer_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        tax_residence = client.customers.tax_residences.delete(
            tax_residence_id="TAX_RESIDENCE_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        )
        assert tax_residence is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.customers.tax_residences.with_raw_response.delete(
            tax_residence_id="TAX_RESIDENCE_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tax_residence = response.parse()
        assert tax_residence is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.customers.tax_residences.with_streaming_response.delete(
            tax_residence_id="TAX_RESIDENCE_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tax_residence = response.parse()
            assert tax_residence is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.tax_residences.with_raw_response.delete(
                tax_residence_id="TAX_RESIDENCE_ID",
                bank_id="",
                customer_id="CUSTOMER_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.tax_residences.with_raw_response.delete(
                tax_residence_id="TAX_RESIDENCE_ID",
                bank_id="BANK_ID",
                customer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tax_residence_id` but received ''"):
            client.customers.tax_residences.with_raw_response.delete(
                tax_residence_id="",
                bank_id="BANK_ID",
                customer_id="CUSTOMER_ID",
            )


class TestAsyncTaxResidences:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residence").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tax_residence = await async_client.customers.tax_residences.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert tax_residence.is_closed
        assert await tax_residence.json() == {"foo": "bar"}
        assert cast(Any, tax_residence.is_closed) is True
        assert isinstance(tax_residence, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residence").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tax_residence = await async_client.customers.tax_residences.with_raw_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert tax_residence.is_closed is True
        assert tax_residence.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await tax_residence.json() == {"foo": "bar"}
        assert isinstance(tax_residence, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residence").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.tax_residences.with_streaming_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as tax_residence:
            assert not tax_residence.is_closed
            assert tax_residence.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await tax_residence.json() == {"foo": "bar"}
            assert cast(Any, tax_residence.is_closed) is True
            assert isinstance(tax_residence, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, tax_residence.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.tax_residences.with_raw_response.create(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.tax_residences.with_raw_response.create(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residences").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tax_residence = await async_client.customers.tax_residences.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert tax_residence.is_closed
        assert await tax_residence.json() == {"foo": "bar"}
        assert cast(Any, tax_residence.is_closed) is True
        assert isinstance(tax_residence, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residences").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tax_residence = await async_client.customers.tax_residences.with_raw_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert tax_residence.is_closed is True
        assert tax_residence.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await tax_residence.json() == {"foo": "bar"}
        assert isinstance(tax_residence, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/tax-residences").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.tax_residences.with_streaming_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as tax_residence:
            assert not tax_residence.is_closed
            assert tax_residence.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await tax_residence.json() == {"foo": "bar"}
            assert cast(Any, tax_residence.is_closed) is True
            assert isinstance(tax_residence, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, tax_residence.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.tax_residences.with_raw_response.list(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.tax_residences.with_raw_response.list(
                customer_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        tax_residence = await async_client.customers.tax_residences.delete(
            tax_residence_id="TAX_RESIDENCE_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        )
        assert tax_residence is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.customers.tax_residences.with_raw_response.delete(
            tax_residence_id="TAX_RESIDENCE_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tax_residence = await response.parse()
        assert tax_residence is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.customers.tax_residences.with_streaming_response.delete(
            tax_residence_id="TAX_RESIDENCE_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tax_residence = await response.parse()
            assert tax_residence is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.tax_residences.with_raw_response.delete(
                tax_residence_id="TAX_RESIDENCE_ID",
                bank_id="",
                customer_id="CUSTOMER_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.tax_residences.with_raw_response.delete(
                tax_residence_id="TAX_RESIDENCE_ID",
                bank_id="BANK_ID",
                customer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tax_residence_id` but received ''"):
            await async_client.customers.tax_residences.with_raw_response.delete(
                tax_residence_id="",
                bank_id="BANK_ID",
                customer_id="CUSTOMER_ID",
            )
