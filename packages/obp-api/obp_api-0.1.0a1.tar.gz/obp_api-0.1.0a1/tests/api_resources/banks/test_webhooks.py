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


class TestWebhooks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/banks/BANK_ID/account-web-hooks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        webhook = client.banks.webhooks.list(
            "BANK_ID",
        )
        assert webhook.is_closed
        assert webhook.json() == {"foo": "bar"}
        assert cast(Any, webhook.is_closed) is True
        assert isinstance(webhook, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/banks/BANK_ID/account-web-hooks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        webhook = client.banks.webhooks.with_raw_response.list(
            "BANK_ID",
        )

        assert webhook.is_closed is True
        assert webhook.http_request.headers.get("X-Stainless-Lang") == "python"
        assert webhook.json() == {"foo": "bar"}
        assert isinstance(webhook, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/banks/BANK_ID/account-web-hooks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.webhooks.with_streaming_response.list(
            "BANK_ID",
        ) as webhook:
            assert not webhook.is_closed
            assert webhook.http_request.headers.get("X-Stainless-Lang") == "python"

            assert webhook.json() == {"foo": "bar"}
            assert cast(Any, webhook.is_closed) is True
            assert isinstance(webhook, StreamedBinaryAPIResponse)

        assert cast(Any, webhook.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.webhooks.with_raw_response.list(
                "",
            )


class TestAsyncWebhooks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/banks/BANK_ID/account-web-hooks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        webhook = await async_client.banks.webhooks.list(
            "BANK_ID",
        )
        assert webhook.is_closed
        assert await webhook.json() == {"foo": "bar"}
        assert cast(Any, webhook.is_closed) is True
        assert isinstance(webhook, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/banks/BANK_ID/account-web-hooks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        webhook = await async_client.banks.webhooks.with_raw_response.list(
            "BANK_ID",
        )

        assert webhook.is_closed is True
        assert webhook.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await webhook.json() == {"foo": "bar"}
        assert isinstance(webhook, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/banks/BANK_ID/account-web-hooks").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.webhooks.with_streaming_response.list(
            "BANK_ID",
        ) as webhook:
            assert not webhook.is_closed
            assert webhook.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await webhook.json() == {"foo": "bar"}
            assert cast(Any, webhook.is_closed) is True
            assert isinstance(webhook, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, webhook.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.webhooks.with_raw_response.list(
                "",
            )
