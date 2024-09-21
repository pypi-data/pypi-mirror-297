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


class TestProducts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/attribute-definitions/ATTRIBUTE_DEFINITION_ID/transaction-request"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        product = client.banks.attribute_definitions.products.delete(
            "BANK_ID",
        )
        assert product.is_closed
        assert product.json() == {"foo": "bar"}
        assert cast(Any, product.is_closed) is True
        assert isinstance(product, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/attribute-definitions/ATTRIBUTE_DEFINITION_ID/transaction-request"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        product = client.banks.attribute_definitions.products.with_raw_response.delete(
            "BANK_ID",
        )

        assert product.is_closed is True
        assert product.http_request.headers.get("X-Stainless-Lang") == "python"
        assert product.json() == {"foo": "bar"}
        assert isinstance(product, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/attribute-definitions/ATTRIBUTE_DEFINITION_ID/transaction-request"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.attribute_definitions.products.with_streaming_response.delete(
            "BANK_ID",
        ) as product:
            assert not product.is_closed
            assert product.http_request.headers.get("X-Stainless-Lang") == "python"

            assert product.json() == {"foo": "bar"}
            assert cast(Any, product.is_closed) is True
            assert isinstance(product, StreamedBinaryAPIResponse)

        assert cast(Any, product.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.attribute_definitions.products.with_raw_response.delete(
                "",
            )


class TestAsyncProducts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/attribute-definitions/ATTRIBUTE_DEFINITION_ID/transaction-request"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        product = await async_client.banks.attribute_definitions.products.delete(
            "BANK_ID",
        )
        assert product.is_closed
        assert await product.json() == {"foo": "bar"}
        assert cast(Any, product.is_closed) is True
        assert isinstance(product, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/attribute-definitions/ATTRIBUTE_DEFINITION_ID/transaction-request"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        product = await async_client.banks.attribute_definitions.products.with_raw_response.delete(
            "BANK_ID",
        )

        assert product.is_closed is True
        assert product.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await product.json() == {"foo": "bar"}
        assert isinstance(product, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/attribute-definitions/ATTRIBUTE_DEFINITION_ID/transaction-request"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.attribute_definitions.products.with_streaming_response.delete(
            "BANK_ID",
        ) as product:
            assert not product.is_closed
            assert product.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await product.json() == {"foo": "bar"}
            assert cast(Any, product.is_closed) is True
            assert isinstance(product, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, product.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.attribute_definitions.products.with_raw_response.delete(
                "",
            )
