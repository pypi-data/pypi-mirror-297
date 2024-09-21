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


class TestKYCChecks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_check/KYC_CHECK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        kyc_check = client.customers.kyc_checks.update(
            kyc_check_id="KYC_CHECK_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        )
        assert kyc_check.is_closed
        assert kyc_check.json() == {"foo": "bar"}
        assert cast(Any, kyc_check.is_closed) is True
        assert isinstance(kyc_check, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_check/KYC_CHECK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        kyc_check = client.customers.kyc_checks.with_raw_response.update(
            kyc_check_id="KYC_CHECK_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        )

        assert kyc_check.is_closed is True
        assert kyc_check.http_request.headers.get("X-Stainless-Lang") == "python"
        assert kyc_check.json() == {"foo": "bar"}
        assert isinstance(kyc_check, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_check/KYC_CHECK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.kyc_checks.with_streaming_response.update(
            kyc_check_id="KYC_CHECK_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        ) as kyc_check:
            assert not kyc_check.is_closed
            assert kyc_check.http_request.headers.get("X-Stainless-Lang") == "python"

            assert kyc_check.json() == {"foo": "bar"}
            assert cast(Any, kyc_check.is_closed) is True
            assert isinstance(kyc_check, StreamedBinaryAPIResponse)

        assert cast(Any, kyc_check.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.kyc_checks.with_raw_response.update(
                kyc_check_id="KYC_CHECK_ID",
                bank_id="",
                customer_id="CUSTOMER_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.kyc_checks.with_raw_response.update(
                kyc_check_id="KYC_CHECK_ID",
                bank_id="BANK_ID",
                customer_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kyc_check_id` but received ''"):
            client.customers.kyc_checks.with_raw_response.update(
                kyc_check_id="",
                bank_id="BANK_ID",
                customer_id="CUSTOMER_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_checks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        kyc_check = client.customers.kyc_checks.list(
            "CUSTOMER_ID",
        )
        assert kyc_check.is_closed
        assert kyc_check.json() == {"foo": "bar"}
        assert cast(Any, kyc_check.is_closed) is True
        assert isinstance(kyc_check, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_checks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        kyc_check = client.customers.kyc_checks.with_raw_response.list(
            "CUSTOMER_ID",
        )

        assert kyc_check.is_closed is True
        assert kyc_check.http_request.headers.get("X-Stainless-Lang") == "python"
        assert kyc_check.json() == {"foo": "bar"}
        assert isinstance(kyc_check, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_checks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.kyc_checks.with_streaming_response.list(
            "CUSTOMER_ID",
        ) as kyc_check:
            assert not kyc_check.is_closed
            assert kyc_check.http_request.headers.get("X-Stainless-Lang") == "python"

            assert kyc_check.json() == {"foo": "bar"}
            assert cast(Any, kyc_check.is_closed) is True
            assert isinstance(kyc_check, StreamedBinaryAPIResponse)

        assert cast(Any, kyc_check.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.kyc_checks.with_raw_response.list(
                "",
            )


class TestAsyncKYCChecks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_check/KYC_CHECK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        kyc_check = await async_client.customers.kyc_checks.update(
            kyc_check_id="KYC_CHECK_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        )
        assert kyc_check.is_closed
        assert await kyc_check.json() == {"foo": "bar"}
        assert cast(Any, kyc_check.is_closed) is True
        assert isinstance(kyc_check, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_check/KYC_CHECK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        kyc_check = await async_client.customers.kyc_checks.with_raw_response.update(
            kyc_check_id="KYC_CHECK_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        )

        assert kyc_check.is_closed is True
        assert kyc_check.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await kyc_check.json() == {"foo": "bar"}
        assert isinstance(kyc_check, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/kyc_check/KYC_CHECK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.kyc_checks.with_streaming_response.update(
            kyc_check_id="KYC_CHECK_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        ) as kyc_check:
            assert not kyc_check.is_closed
            assert kyc_check.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await kyc_check.json() == {"foo": "bar"}
            assert cast(Any, kyc_check.is_closed) is True
            assert isinstance(kyc_check, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, kyc_check.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.kyc_checks.with_raw_response.update(
                kyc_check_id="KYC_CHECK_ID",
                bank_id="",
                customer_id="CUSTOMER_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.kyc_checks.with_raw_response.update(
                kyc_check_id="KYC_CHECK_ID",
                bank_id="BANK_ID",
                customer_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kyc_check_id` but received ''"):
            await async_client.customers.kyc_checks.with_raw_response.update(
                kyc_check_id="",
                bank_id="BANK_ID",
                customer_id="CUSTOMER_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_checks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        kyc_check = await async_client.customers.kyc_checks.list(
            "CUSTOMER_ID",
        )
        assert kyc_check.is_closed
        assert await kyc_check.json() == {"foo": "bar"}
        assert cast(Any, kyc_check.is_closed) is True
        assert isinstance(kyc_check, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_checks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        kyc_check = await async_client.customers.kyc_checks.with_raw_response.list(
            "CUSTOMER_ID",
        )

        assert kyc_check.is_closed is True
        assert kyc_check.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await kyc_check.json() == {"foo": "bar"}
        assert isinstance(kyc_check, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/customers/CUSTOMER_ID/kyc_checks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.kyc_checks.with_streaming_response.list(
            "CUSTOMER_ID",
        ) as kyc_check:
            assert not kyc_check.is_closed
            assert kyc_check.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await kyc_check.json() == {"foo": "bar"}
            assert cast(Any, kyc_check.is_closed) is True
            assert isinstance(kyc_check, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, kyc_check.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.kyc_checks.with_raw_response.list(
                "",
            )
