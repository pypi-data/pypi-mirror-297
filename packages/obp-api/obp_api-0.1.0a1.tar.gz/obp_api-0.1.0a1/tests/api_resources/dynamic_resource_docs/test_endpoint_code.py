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


class TestEndpointCode:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs/endpoint-code").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_code = client.dynamic_resource_docs.endpoint_code.create(
            body={},
        )
        assert endpoint_code.is_closed
        assert endpoint_code.json() == {"foo": "bar"}
        assert cast(Any, endpoint_code.is_closed) is True
        assert isinstance(endpoint_code, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs/endpoint-code").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_code = client.dynamic_resource_docs.endpoint_code.with_raw_response.create(
            body={},
        )

        assert endpoint_code.is_closed is True
        assert endpoint_code.http_request.headers.get("X-Stainless-Lang") == "python"
        assert endpoint_code.json() == {"foo": "bar"}
        assert isinstance(endpoint_code, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs/endpoint-code").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.dynamic_resource_docs.endpoint_code.with_streaming_response.create(
            body={},
        ) as endpoint_code:
            assert not endpoint_code.is_closed
            assert endpoint_code.http_request.headers.get("X-Stainless-Lang") == "python"

            assert endpoint_code.json() == {"foo": "bar"}
            assert cast(Any, endpoint_code.is_closed) is True
            assert isinstance(endpoint_code, StreamedBinaryAPIResponse)

        assert cast(Any, endpoint_code.is_closed) is True


class TestAsyncEndpointCode:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs/endpoint-code").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_code = await async_client.dynamic_resource_docs.endpoint_code.create(
            body={},
        )
        assert endpoint_code.is_closed
        assert await endpoint_code.json() == {"foo": "bar"}
        assert cast(Any, endpoint_code.is_closed) is True
        assert isinstance(endpoint_code, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs/endpoint-code").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_code = await async_client.dynamic_resource_docs.endpoint_code.with_raw_response.create(
            body={},
        )

        assert endpoint_code.is_closed is True
        assert endpoint_code.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await endpoint_code.json() == {"foo": "bar"}
        assert isinstance(endpoint_code, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs/endpoint-code").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.dynamic_resource_docs.endpoint_code.with_streaming_response.create(
            body={},
        ) as endpoint_code:
            assert not endpoint_code.is_closed
            assert endpoint_code.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await endpoint_code.json() == {"foo": "bar"}
            assert cast(Any, endpoint_code.is_closed) is True
            assert isinstance(endpoint_code, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, endpoint_code.is_closed) is True
