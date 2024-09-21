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


class TestAPIEndpoints:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collection-ids/API_COLLECTION_ID/api-collection-endpoint-ids/API_COLLECTION_ENDPOINT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        api_endpoint = client.api_collections.api_endpoints.delete()
        assert api_endpoint.is_closed
        assert api_endpoint.json() == {"foo": "bar"}
        assert cast(Any, api_endpoint.is_closed) is True
        assert isinstance(api_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collection-ids/API_COLLECTION_ID/api-collection-endpoint-ids/API_COLLECTION_ENDPOINT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        api_endpoint = client.api_collections.api_endpoints.with_raw_response.delete()

        assert api_endpoint.is_closed is True
        assert api_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert api_endpoint.json() == {"foo": "bar"}
        assert isinstance(api_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collection-ids/API_COLLECTION_ID/api-collection-endpoint-ids/API_COLLECTION_ENDPOINT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.api_collections.api_endpoints.with_streaming_response.delete() as api_endpoint:
            assert not api_endpoint.is_closed
            assert api_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert api_endpoint.json() == {"foo": "bar"}
            assert cast(Any, api_endpoint.is_closed) is True
            assert isinstance(api_endpoint, StreamedBinaryAPIResponse)

        assert cast(Any, api_endpoint.is_closed) is True


class TestAsyncAPIEndpoints:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collection-ids/API_COLLECTION_ID/api-collection-endpoint-ids/API_COLLECTION_ENDPOINT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        api_endpoint = await async_client.api_collections.api_endpoints.delete()
        assert api_endpoint.is_closed
        assert await api_endpoint.json() == {"foo": "bar"}
        assert cast(Any, api_endpoint.is_closed) is True
        assert isinstance(api_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collection-ids/API_COLLECTION_ID/api-collection-endpoint-ids/API_COLLECTION_ENDPOINT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        api_endpoint = await async_client.api_collections.api_endpoints.with_raw_response.delete()

        assert api_endpoint.is_closed is True
        assert api_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await api_endpoint.json() == {"foo": "bar"}
        assert isinstance(api_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collection-ids/API_COLLECTION_ID/api-collection-endpoint-ids/API_COLLECTION_ENDPOINT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.api_collections.api_endpoints.with_streaming_response.delete() as api_endpoint:
            assert not api_endpoint.is_closed
            assert api_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await api_endpoint.json() == {"foo": "bar"}
            assert cast(Any, api_endpoint.is_closed) is True
            assert isinstance(api_endpoint, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, api_endpoint.is_closed) is True
