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


class TestKYCStatuses:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        kyc_status = client.customers.kyc_statuses.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert kyc_status.is_closed
        assert kyc_status.json() == {"foo": "bar"}
        assert cast(Any, kyc_status.is_closed) is True
        assert isinstance(kyc_status, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        kyc_status = client.customers.kyc_statuses.with_raw_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert kyc_status.is_closed is True
        assert kyc_status.http_request.headers.get("X-Stainless-Lang") == "python"
        assert kyc_status.json() == {"foo": "bar"}
        assert isinstance(kyc_status, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.kyc_statuses.with_streaming_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as kyc_status:
            assert not kyc_status.is_closed
            assert kyc_status.http_request.headers.get("X-Stainless-Lang") == "python"

            assert kyc_status.json() == {"foo": "bar"}
            assert cast(Any, kyc_status.is_closed) is True
            assert isinstance(kyc_status, StreamedBinaryAPIResponse)

        assert cast(Any, kyc_status.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.kyc_statuses.with_raw_response.update(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.kyc_statuses.with_raw_response.update(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        kyc_status = client.customers.kyc_statuses.list(
            "CUSTOMER_ID",
        )
        assert kyc_status.is_closed
        assert kyc_status.json() == {"foo": "bar"}
        assert cast(Any, kyc_status.is_closed) is True
        assert isinstance(kyc_status, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        kyc_status = client.customers.kyc_statuses.with_raw_response.list(
            "CUSTOMER_ID",
        )

        assert kyc_status.is_closed is True
        assert kyc_status.http_request.headers.get("X-Stainless-Lang") == "python"
        assert kyc_status.json() == {"foo": "bar"}
        assert isinstance(kyc_status, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.kyc_statuses.with_streaming_response.list(
            "CUSTOMER_ID",
        ) as kyc_status:
            assert not kyc_status.is_closed
            assert kyc_status.http_request.headers.get("X-Stainless-Lang") == "python"

            assert kyc_status.json() == {"foo": "bar"}
            assert cast(Any, kyc_status.is_closed) is True
            assert isinstance(kyc_status, StreamedBinaryAPIResponse)

        assert cast(Any, kyc_status.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.kyc_statuses.with_raw_response.list(
                "",
            )


class TestAsyncKYCStatuses:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        kyc_status = await async_client.customers.kyc_statuses.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert kyc_status.is_closed
        assert await kyc_status.json() == {"foo": "bar"}
        assert cast(Any, kyc_status.is_closed) is True
        assert isinstance(kyc_status, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        kyc_status = await async_client.customers.kyc_statuses.with_raw_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert kyc_status.is_closed is True
        assert kyc_status.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await kyc_status.json() == {"foo": "bar"}
        assert isinstance(kyc_status, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.kyc_statuses.with_streaming_response.update(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as kyc_status:
            assert not kyc_status.is_closed
            assert kyc_status.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await kyc_status.json() == {"foo": "bar"}
            assert cast(Any, kyc_status.is_closed) is True
            assert isinstance(kyc_status, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, kyc_status.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.kyc_statuses.with_raw_response.update(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.kyc_statuses.with_raw_response.update(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        kyc_status = await async_client.customers.kyc_statuses.list(
            "CUSTOMER_ID",
        )
        assert kyc_status.is_closed
        assert await kyc_status.json() == {"foo": "bar"}
        assert cast(Any, kyc_status.is_closed) is True
        assert isinstance(kyc_status, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        kyc_status = await async_client.customers.kyc_statuses.with_raw_response.list(
            "CUSTOMER_ID",
        )

        assert kyc_status.is_closed is True
        assert kyc_status.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await kyc_status.json() == {"foo": "bar"}
        assert isinstance(kyc_status, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_statuses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.kyc_statuses.with_streaming_response.list(
            "CUSTOMER_ID",
        ) as kyc_status:
            assert not kyc_status.is_closed
            assert kyc_status.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await kyc_status.json() == {"foo": "bar"}
            assert cast(Any, kyc_status.is_closed) is True
            assert isinstance(kyc_status, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, kyc_status.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.kyc_statuses.with_raw_response.list(
                "",
            )
