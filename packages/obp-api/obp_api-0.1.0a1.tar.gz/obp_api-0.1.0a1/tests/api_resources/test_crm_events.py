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


class TestCRMEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/crm-events").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        crm_event = client.crm_events.list(
            "BANK_ID",
        )
        assert crm_event.is_closed
        assert crm_event.json() == {"foo": "bar"}
        assert cast(Any, crm_event.is_closed) is True
        assert isinstance(crm_event, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/crm-events").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        crm_event = client.crm_events.with_raw_response.list(
            "BANK_ID",
        )

        assert crm_event.is_closed is True
        assert crm_event.http_request.headers.get("X-Stainless-Lang") == "python"
        assert crm_event.json() == {"foo": "bar"}
        assert isinstance(crm_event, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/crm-events").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.crm_events.with_streaming_response.list(
            "BANK_ID",
        ) as crm_event:
            assert not crm_event.is_closed
            assert crm_event.http_request.headers.get("X-Stainless-Lang") == "python"

            assert crm_event.json() == {"foo": "bar"}
            assert cast(Any, crm_event.is_closed) is True
            assert isinstance(crm_event, StreamedBinaryAPIResponse)

        assert cast(Any, crm_event.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.crm_events.with_raw_response.list(
                "",
            )


class TestAsyncCRMEvents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/crm-events").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        crm_event = await async_client.crm_events.list(
            "BANK_ID",
        )
        assert crm_event.is_closed
        assert await crm_event.json() == {"foo": "bar"}
        assert cast(Any, crm_event.is_closed) is True
        assert isinstance(crm_event, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/crm-events").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        crm_event = await async_client.crm_events.with_raw_response.list(
            "BANK_ID",
        )

        assert crm_event.is_closed is True
        assert crm_event.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await crm_event.json() == {"foo": "bar"}
        assert isinstance(crm_event, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/crm-events").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.crm_events.with_streaming_response.list(
            "BANK_ID",
        ) as crm_event:
            assert not crm_event.is_closed
            assert crm_event.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await crm_event.json() == {"foo": "bar"}
            assert cast(Any, crm_event.is_closed) is True
            assert isinstance(crm_event, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, crm_event.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.crm_events.with_raw_response.list(
                "",
            )
