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


class TestHost:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/banks/BANK_ID/dynamic-endpoints/DYNAMIC_ENDPOINT_ID/host").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        host = client.banks.dynamic_endpoints.host.update(
            bank_id="BANK_ID",
            body={},
        )
        assert host.is_closed
        assert host.json() == {"foo": "bar"}
        assert cast(Any, host.is_closed) is True
        assert isinstance(host, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/banks/BANK_ID/dynamic-endpoints/DYNAMIC_ENDPOINT_ID/host").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        host = client.banks.dynamic_endpoints.host.with_raw_response.update(
            bank_id="BANK_ID",
            body={},
        )

        assert host.is_closed is True
        assert host.http_request.headers.get("X-Stainless-Lang") == "python"
        assert host.json() == {"foo": "bar"}
        assert isinstance(host, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/banks/BANK_ID/dynamic-endpoints/DYNAMIC_ENDPOINT_ID/host").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.dynamic_endpoints.host.with_streaming_response.update(
            bank_id="BANK_ID",
            body={},
        ) as host:
            assert not host.is_closed
            assert host.http_request.headers.get("X-Stainless-Lang") == "python"

            assert host.json() == {"foo": "bar"}
            assert cast(Any, host.is_closed) is True
            assert isinstance(host, StreamedBinaryAPIResponse)

        assert cast(Any, host.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.dynamic_endpoints.host.with_raw_response.update(
                bank_id="",
                body={},
            )


class TestAsyncHost:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/banks/BANK_ID/dynamic-endpoints/DYNAMIC_ENDPOINT_ID/host").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        host = await async_client.banks.dynamic_endpoints.host.update(
            bank_id="BANK_ID",
            body={},
        )
        assert host.is_closed
        assert await host.json() == {"foo": "bar"}
        assert cast(Any, host.is_closed) is True
        assert isinstance(host, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/banks/BANK_ID/dynamic-endpoints/DYNAMIC_ENDPOINT_ID/host").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        host = await async_client.banks.dynamic_endpoints.host.with_raw_response.update(
            bank_id="BANK_ID",
            body={},
        )

        assert host.is_closed is True
        assert host.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await host.json() == {"foo": "bar"}
        assert isinstance(host, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/banks/BANK_ID/dynamic-endpoints/DYNAMIC_ENDPOINT_ID/host").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.dynamic_endpoints.host.with_streaming_response.update(
            bank_id="BANK_ID",
            body={},
        ) as host:
            assert not host.is_closed
            assert host.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await host.json() == {"foo": "bar"}
            assert cast(Any, host.is_closed) is True
            assert isinstance(host, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, host.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.dynamic_endpoints.host.with_raw_response.update(
                bank_id="",
                body={},
            )
