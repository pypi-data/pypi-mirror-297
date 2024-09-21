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


class TestProductCollections:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        product_collection = client.product_collections.retrieve(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
        )
        assert product_collection.is_closed
        assert product_collection.json() == {"foo": "bar"}
        assert cast(Any, product_collection.is_closed) is True
        assert isinstance(product_collection, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        product_collection = client.product_collections.with_raw_response.retrieve(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
        )

        assert product_collection.is_closed is True
        assert product_collection.http_request.headers.get("X-Stainless-Lang") == "python"
        assert product_collection.json() == {"foo": "bar"}
        assert isinstance(product_collection, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.product_collections.with_streaming_response.retrieve(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
        ) as product_collection:
            assert not product_collection.is_closed
            assert product_collection.http_request.headers.get("X-Stainless-Lang") == "python"

            assert product_collection.json() == {"foo": "bar"}
            assert cast(Any, product_collection.is_closed) is True
            assert isinstance(product_collection, StreamedBinaryAPIResponse)

        assert cast(Any, product_collection.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.product_collections.with_raw_response.retrieve(
                collection_code="COLLECTION_CODE",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_code` but received ''"):
            client.product_collections.with_raw_response.retrieve(
                collection_code="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        product_collection = client.product_collections.update(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
            body={},
        )
        assert product_collection.is_closed
        assert product_collection.json() == {"foo": "bar"}
        assert cast(Any, product_collection.is_closed) is True
        assert isinstance(product_collection, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        product_collection = client.product_collections.with_raw_response.update(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
            body={},
        )

        assert product_collection.is_closed is True
        assert product_collection.http_request.headers.get("X-Stainless-Lang") == "python"
        assert product_collection.json() == {"foo": "bar"}
        assert isinstance(product_collection, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.product_collections.with_streaming_response.update(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
            body={},
        ) as product_collection:
            assert not product_collection.is_closed
            assert product_collection.http_request.headers.get("X-Stainless-Lang") == "python"

            assert product_collection.json() == {"foo": "bar"}
            assert cast(Any, product_collection.is_closed) is True
            assert isinstance(product_collection, StreamedBinaryAPIResponse)

        assert cast(Any, product_collection.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.product_collections.with_raw_response.update(
                collection_code="COLLECTION_CODE",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_code` but received ''"):
            client.product_collections.with_raw_response.update(
                collection_code="",
                bank_id="BANK_ID",
                body={},
            )


class TestAsyncProductCollections:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        product_collection = await async_client.product_collections.retrieve(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
        )
        assert product_collection.is_closed
        assert await product_collection.json() == {"foo": "bar"}
        assert cast(Any, product_collection.is_closed) is True
        assert isinstance(product_collection, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        product_collection = await async_client.product_collections.with_raw_response.retrieve(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
        )

        assert product_collection.is_closed is True
        assert product_collection.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await product_collection.json() == {"foo": "bar"}
        assert isinstance(product_collection, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.product_collections.with_streaming_response.retrieve(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
        ) as product_collection:
            assert not product_collection.is_closed
            assert product_collection.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await product_collection.json() == {"foo": "bar"}
            assert cast(Any, product_collection.is_closed) is True
            assert isinstance(product_collection, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, product_collection.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.product_collections.with_raw_response.retrieve(
                collection_code="COLLECTION_CODE",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_code` but received ''"):
            await async_client.product_collections.with_raw_response.retrieve(
                collection_code="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        product_collection = await async_client.product_collections.update(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
            body={},
        )
        assert product_collection.is_closed
        assert await product_collection.json() == {"foo": "bar"}
        assert cast(Any, product_collection.is_closed) is True
        assert isinstance(product_collection, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        product_collection = await async_client.product_collections.with_raw_response.update(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
            body={},
        )

        assert product_collection.is_closed is True
        assert product_collection.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await product_collection.json() == {"foo": "bar"}
        assert isinstance(product_collection, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/product-collections/COLLECTION_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.product_collections.with_streaming_response.update(
            collection_code="COLLECTION_CODE",
            bank_id="BANK_ID",
            body={},
        ) as product_collection:
            assert not product_collection.is_closed
            assert product_collection.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await product_collection.json() == {"foo": "bar"}
            assert cast(Any, product_collection.is_closed) is True
            assert isinstance(product_collection, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, product_collection.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.product_collections.with_raw_response.update(
                collection_code="COLLECTION_CODE",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_code` but received ''"):
            await async_client.product_collections.with_raw_response.update(
                collection_code="",
                bank_id="BANK_ID",
                body={},
            )
