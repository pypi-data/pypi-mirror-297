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


class TestMyConsents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        my_consent = client.banks.my_consents.list(
            "BANK_ID",
        )
        assert my_consent.is_closed
        assert my_consent.json() == {"foo": "bar"}
        assert cast(Any, my_consent.is_closed) is True
        assert isinstance(my_consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        my_consent = client.banks.my_consents.with_raw_response.list(
            "BANK_ID",
        )

        assert my_consent.is_closed is True
        assert my_consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert my_consent.json() == {"foo": "bar"}
        assert isinstance(my_consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.my_consents.with_streaming_response.list(
            "BANK_ID",
        ) as my_consent:
            assert not my_consent.is_closed
            assert my_consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert my_consent.json() == {"foo": "bar"}
            assert cast(Any, my_consent.is_closed) is True
            assert isinstance(my_consent, StreamedBinaryAPIResponse)

        assert cast(Any, my_consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.my_consents.with_raw_response.list(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_revoke(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents/CONSENT_ID/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        my_consent = client.banks.my_consents.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        )
        assert my_consent.is_closed
        assert my_consent.json() == {"foo": "bar"}
        assert cast(Any, my_consent.is_closed) is True
        assert isinstance(my_consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_revoke(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents/CONSENT_ID/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        my_consent = client.banks.my_consents.with_raw_response.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        )

        assert my_consent.is_closed is True
        assert my_consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert my_consent.json() == {"foo": "bar"}
        assert isinstance(my_consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_revoke(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents/CONSENT_ID/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.my_consents.with_streaming_response.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        ) as my_consent:
            assert not my_consent.is_closed
            assert my_consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert my_consent.json() == {"foo": "bar"}
            assert cast(Any, my_consent.is_closed) is True
            assert isinstance(my_consent, StreamedBinaryAPIResponse)

        assert cast(Any, my_consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_revoke(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.my_consents.with_raw_response.revoke(
                consent_id="CONSENT_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            client.banks.my_consents.with_raw_response.revoke(
                consent_id="",
                bank_id="BANK_ID",
            )


class TestAsyncMyConsents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        my_consent = await async_client.banks.my_consents.list(
            "BANK_ID",
        )
        assert my_consent.is_closed
        assert await my_consent.json() == {"foo": "bar"}
        assert cast(Any, my_consent.is_closed) is True
        assert isinstance(my_consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        my_consent = await async_client.banks.my_consents.with_raw_response.list(
            "BANK_ID",
        )

        assert my_consent.is_closed is True
        assert my_consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await my_consent.json() == {"foo": "bar"}
        assert isinstance(my_consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.my_consents.with_streaming_response.list(
            "BANK_ID",
        ) as my_consent:
            assert not my_consent.is_closed
            assert my_consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await my_consent.json() == {"foo": "bar"}
            assert cast(Any, my_consent.is_closed) is True
            assert isinstance(my_consent, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, my_consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.my_consents.with_raw_response.list(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_revoke(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents/CONSENT_ID/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        my_consent = await async_client.banks.my_consents.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        )
        assert my_consent.is_closed
        assert await my_consent.json() == {"foo": "bar"}
        assert cast(Any, my_consent.is_closed) is True
        assert isinstance(my_consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_revoke(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents/CONSENT_ID/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        my_consent = await async_client.banks.my_consents.with_raw_response.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        )

        assert my_consent.is_closed is True
        assert my_consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await my_consent.json() == {"foo": "bar"}
        assert isinstance(my_consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_revoke(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/my/consents/CONSENT_ID/revoke").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.my_consents.with_streaming_response.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        ) as my_consent:
            assert not my_consent.is_closed
            assert my_consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await my_consent.json() == {"foo": "bar"}
            assert cast(Any, my_consent.is_closed) is True
            assert isinstance(my_consent, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, my_consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_revoke(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.my_consents.with_raw_response.revoke(
                consent_id="CONSENT_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            await async_client.banks.my_consents.with_raw_response.revoke(
                consent_id="",
                bank_id="BANK_ID",
            )
