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


class TestFees:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fee").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fee = client.products.fees.create(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        )
        assert fee.is_closed
        assert fee.json() == {"foo": "bar"}
        assert cast(Any, fee.is_closed) is True
        assert isinstance(fee, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fee").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fee = client.products.fees.with_raw_response.create(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        )

        assert fee.is_closed is True
        assert fee.http_request.headers.get("X-Stainless-Lang") == "python"
        assert fee.json() == {"foo": "bar"}
        assert isinstance(fee, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fee").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.products.fees.with_streaming_response.create(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        ) as fee:
            assert not fee.is_closed
            assert fee.http_request.headers.get("X-Stainless-Lang") == "python"

            assert fee.json() == {"foo": "bar"}
            assert cast(Any, fee.is_closed) is True
            assert isinstance(fee, StreamedBinaryAPIResponse)

        assert cast(Any, fee.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.products.fees.with_raw_response.create(
                product_code="PRODUCT_CODE",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `product_code` but received ''"):
            client.products.fees.with_raw_response.create(
                product_code="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fee = client.products.fees.retrieve(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )
        assert fee.is_closed
        assert fee.json() == {"foo": "bar"}
        assert cast(Any, fee.is_closed) is True
        assert isinstance(fee, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fee = client.products.fees.with_raw_response.retrieve(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )

        assert fee.is_closed is True
        assert fee.http_request.headers.get("X-Stainless-Lang") == "python"
        assert fee.json() == {"foo": "bar"}
        assert isinstance(fee, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.products.fees.with_streaming_response.retrieve(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        ) as fee:
            assert not fee.is_closed
            assert fee.http_request.headers.get("X-Stainless-Lang") == "python"

            assert fee.json() == {"foo": "bar"}
            assert cast(Any, fee.is_closed) is True
            assert isinstance(fee, StreamedBinaryAPIResponse)

        assert cast(Any, fee.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.products.fees.with_raw_response.retrieve(
                product_code="PRODUCT_CODE",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `product_code` but received ''"):
            client.products.fees.with_raw_response.retrieve(
                product_code="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fee = client.products.fees.update(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        )
        assert fee.is_closed
        assert fee.json() == {"foo": "bar"}
        assert cast(Any, fee.is_closed) is True
        assert isinstance(fee, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fee = client.products.fees.with_raw_response.update(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        )

        assert fee.is_closed is True
        assert fee.http_request.headers.get("X-Stainless-Lang") == "python"
        assert fee.json() == {"foo": "bar"}
        assert isinstance(fee, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.products.fees.with_streaming_response.update(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        ) as fee:
            assert not fee.is_closed
            assert fee.http_request.headers.get("X-Stainless-Lang") == "python"

            assert fee.json() == {"foo": "bar"}
            assert cast(Any, fee.is_closed) is True
            assert isinstance(fee, StreamedBinaryAPIResponse)

        assert cast(Any, fee.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.products.fees.with_raw_response.update(
                product_code="PRODUCT_CODE",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `product_code` but received ''"):
            client.products.fees.with_raw_response.update(
                product_code="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fee = client.products.fees.list(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )
        assert fee.is_closed
        assert fee.json() == {"foo": "bar"}
        assert cast(Any, fee.is_closed) is True
        assert isinstance(fee, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fee = client.products.fees.with_raw_response.list(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )

        assert fee.is_closed is True
        assert fee.http_request.headers.get("X-Stainless-Lang") == "python"
        assert fee.json() == {"foo": "bar"}
        assert isinstance(fee, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.products.fees.with_streaming_response.list(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        ) as fee:
            assert not fee.is_closed
            assert fee.http_request.headers.get("X-Stainless-Lang") == "python"

            assert fee.json() == {"foo": "bar"}
            assert cast(Any, fee.is_closed) is True
            assert isinstance(fee, StreamedBinaryAPIResponse)

        assert cast(Any, fee.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.products.fees.with_raw_response.list(
                product_code="PRODUCT_CODE",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `product_code` but received ''"):
            client.products.fees.with_raw_response.list(
                product_code="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fee = client.products.fees.delete(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )
        assert fee.is_closed
        assert fee.json() == {"foo": "bar"}
        assert cast(Any, fee.is_closed) is True
        assert isinstance(fee, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fee = client.products.fees.with_raw_response.delete(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )

        assert fee.is_closed is True
        assert fee.http_request.headers.get("X-Stainless-Lang") == "python"
        assert fee.json() == {"foo": "bar"}
        assert isinstance(fee, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.products.fees.with_streaming_response.delete(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        ) as fee:
            assert not fee.is_closed
            assert fee.http_request.headers.get("X-Stainless-Lang") == "python"

            assert fee.json() == {"foo": "bar"}
            assert cast(Any, fee.is_closed) is True
            assert isinstance(fee, StreamedBinaryAPIResponse)

        assert cast(Any, fee.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.products.fees.with_raw_response.delete(
                product_code="PRODUCT_CODE",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `product_code` but received ''"):
            client.products.fees.with_raw_response.delete(
                product_code="",
                bank_id="BANK_ID",
            )


class TestAsyncFees:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fee").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fee = await async_client.products.fees.create(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        )
        assert fee.is_closed
        assert await fee.json() == {"foo": "bar"}
        assert cast(Any, fee.is_closed) is True
        assert isinstance(fee, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fee").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fee = await async_client.products.fees.with_raw_response.create(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        )

        assert fee.is_closed is True
        assert fee.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await fee.json() == {"foo": "bar"}
        assert isinstance(fee, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fee").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.products.fees.with_streaming_response.create(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        ) as fee:
            assert not fee.is_closed
            assert fee.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await fee.json() == {"foo": "bar"}
            assert cast(Any, fee.is_closed) is True
            assert isinstance(fee, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, fee.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.products.fees.with_raw_response.create(
                product_code="PRODUCT_CODE",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `product_code` but received ''"):
            await async_client.products.fees.with_raw_response.create(
                product_code="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fee = await async_client.products.fees.retrieve(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )
        assert fee.is_closed
        assert await fee.json() == {"foo": "bar"}
        assert cast(Any, fee.is_closed) is True
        assert isinstance(fee, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fee = await async_client.products.fees.with_raw_response.retrieve(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )

        assert fee.is_closed is True
        assert fee.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await fee.json() == {"foo": "bar"}
        assert isinstance(fee, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.products.fees.with_streaming_response.retrieve(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        ) as fee:
            assert not fee.is_closed
            assert fee.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await fee.json() == {"foo": "bar"}
            assert cast(Any, fee.is_closed) is True
            assert isinstance(fee, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, fee.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.products.fees.with_raw_response.retrieve(
                product_code="PRODUCT_CODE",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `product_code` but received ''"):
            await async_client.products.fees.with_raw_response.retrieve(
                product_code="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fee = await async_client.products.fees.update(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        )
        assert fee.is_closed
        assert await fee.json() == {"foo": "bar"}
        assert cast(Any, fee.is_closed) is True
        assert isinstance(fee, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fee = await async_client.products.fees.with_raw_response.update(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        )

        assert fee.is_closed is True
        assert fee.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await fee.json() == {"foo": "bar"}
        assert isinstance(fee, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.products.fees.with_streaming_response.update(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
            body={},
        ) as fee:
            assert not fee.is_closed
            assert fee.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await fee.json() == {"foo": "bar"}
            assert cast(Any, fee.is_closed) is True
            assert isinstance(fee, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, fee.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.products.fees.with_raw_response.update(
                product_code="PRODUCT_CODE",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `product_code` but received ''"):
            await async_client.products.fees.with_raw_response.update(
                product_code="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fee = await async_client.products.fees.list(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )
        assert fee.is_closed
        assert await fee.json() == {"foo": "bar"}
        assert cast(Any, fee.is_closed) is True
        assert isinstance(fee, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fee = await async_client.products.fees.with_raw_response.list(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )

        assert fee.is_closed is True
        assert fee.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await fee.json() == {"foo": "bar"}
        assert isinstance(fee, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.products.fees.with_streaming_response.list(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        ) as fee:
            assert not fee.is_closed
            assert fee.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await fee.json() == {"foo": "bar"}
            assert cast(Any, fee.is_closed) is True
            assert isinstance(fee, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, fee.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.products.fees.with_raw_response.list(
                product_code="PRODUCT_CODE",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `product_code` but received ''"):
            await async_client.products.fees.with_raw_response.list(
                product_code="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fee = await async_client.products.fees.delete(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )
        assert fee.is_closed
        assert await fee.json() == {"foo": "bar"}
        assert cast(Any, fee.is_closed) is True
        assert isinstance(fee, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fee = await async_client.products.fees.with_raw_response.delete(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        )

        assert fee.is_closed is True
        assert fee.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await fee.json() == {"foo": "bar"}
        assert isinstance(fee, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/products/PRODUCT_CODE/fees/PRODUCT_FEE_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.products.fees.with_streaming_response.delete(
            product_code="PRODUCT_CODE",
            bank_id="BANK_ID",
        ) as fee:
            assert not fee.is_closed
            assert fee.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await fee.json() == {"foo": "bar"}
            assert cast(Any, fee.is_closed) is True
            assert isinstance(fee, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, fee.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.products.fees.with_raw_response.delete(
                product_code="PRODUCT_CODE",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `product_code` but received ''"):
            await async_client.products.fees.with_raw_response.delete(
                product_code="",
                bank_id="BANK_ID",
            )
