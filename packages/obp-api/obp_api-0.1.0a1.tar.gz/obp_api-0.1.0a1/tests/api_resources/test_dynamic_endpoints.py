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


class TestDynamicEndpoints:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_endpoint = client.dynamic_endpoints.create(
            body={},
        )
        assert dynamic_endpoint.is_closed
        assert dynamic_endpoint.json() == {"foo": "bar"}
        assert cast(Any, dynamic_endpoint.is_closed) is True
        assert isinstance(dynamic_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_endpoint = client.dynamic_endpoints.with_raw_response.create(
            body={},
        )

        assert dynamic_endpoint.is_closed is True
        assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert dynamic_endpoint.json() == {"foo": "bar"}
        assert isinstance(dynamic_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.dynamic_endpoints.with_streaming_response.create(
            body={},
        ) as dynamic_endpoint:
            assert not dynamic_endpoint.is_closed
            assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert dynamic_endpoint.json() == {"foo": "bar"}
            assert cast(Any, dynamic_endpoint.is_closed) is True
            assert isinstance(dynamic_endpoint, StreamedBinaryAPIResponse)

        assert cast(Any, dynamic_endpoint.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-endpoints/DYNAMIC_ENDPOINT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_endpoint = client.dynamic_endpoints.retrieve()
        assert dynamic_endpoint.is_closed
        assert dynamic_endpoint.json() == {"foo": "bar"}
        assert cast(Any, dynamic_endpoint.is_closed) is True
        assert isinstance(dynamic_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-endpoints/DYNAMIC_ENDPOINT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_endpoint = client.dynamic_endpoints.with_raw_response.retrieve()

        assert dynamic_endpoint.is_closed is True
        assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert dynamic_endpoint.json() == {"foo": "bar"}
        assert isinstance(dynamic_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-endpoints/DYNAMIC_ENDPOINT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.dynamic_endpoints.with_streaming_response.retrieve() as dynamic_endpoint:
            assert not dynamic_endpoint.is_closed
            assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert dynamic_endpoint.json() == {"foo": "bar"}
            assert cast(Any, dynamic_endpoint.is_closed) is True
            assert isinstance(dynamic_endpoint, StreamedBinaryAPIResponse)

        assert cast(Any, dynamic_endpoint.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-endpoints").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        dynamic_endpoint = client.dynamic_endpoints.list()
        assert dynamic_endpoint.is_closed
        assert dynamic_endpoint.json() == {"foo": "bar"}
        assert cast(Any, dynamic_endpoint.is_closed) is True
        assert isinstance(dynamic_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-endpoints").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        dynamic_endpoint = client.dynamic_endpoints.with_raw_response.list()

        assert dynamic_endpoint.is_closed is True
        assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert dynamic_endpoint.json() == {"foo": "bar"}
        assert isinstance(dynamic_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-endpoints").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.dynamic_endpoints.with_streaming_response.list() as dynamic_endpoint:
            assert not dynamic_endpoint.is_closed
            assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert dynamic_endpoint.json() == {"foo": "bar"}
            assert cast(Any, dynamic_endpoint.is_closed) is True
            assert isinstance(dynamic_endpoint, StreamedBinaryAPIResponse)

        assert cast(Any, dynamic_endpoint.is_closed) is True

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        dynamic_endpoint = client.dynamic_endpoints.delete()
        assert dynamic_endpoint is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.dynamic_endpoints.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dynamic_endpoint = response.parse()
        assert dynamic_endpoint is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.dynamic_endpoints.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dynamic_endpoint = response.parse()
            assert dynamic_endpoint is None

        assert cast(Any, response.is_closed) is True


class TestAsyncDynamicEndpoints:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_endpoint = await async_client.dynamic_endpoints.create(
            body={},
        )
        assert dynamic_endpoint.is_closed
        assert await dynamic_endpoint.json() == {"foo": "bar"}
        assert cast(Any, dynamic_endpoint.is_closed) is True
        assert isinstance(dynamic_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_endpoint = await async_client.dynamic_endpoints.with_raw_response.create(
            body={},
        )

        assert dynamic_endpoint.is_closed is True
        assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await dynamic_endpoint.json() == {"foo": "bar"}
        assert isinstance(dynamic_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.dynamic_endpoints.with_streaming_response.create(
            body={},
        ) as dynamic_endpoint:
            assert not dynamic_endpoint.is_closed
            assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await dynamic_endpoint.json() == {"foo": "bar"}
            assert cast(Any, dynamic_endpoint.is_closed) is True
            assert isinstance(dynamic_endpoint, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, dynamic_endpoint.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-endpoints/DYNAMIC_ENDPOINT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_endpoint = await async_client.dynamic_endpoints.retrieve()
        assert dynamic_endpoint.is_closed
        assert await dynamic_endpoint.json() == {"foo": "bar"}
        assert cast(Any, dynamic_endpoint.is_closed) is True
        assert isinstance(dynamic_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-endpoints/DYNAMIC_ENDPOINT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_endpoint = await async_client.dynamic_endpoints.with_raw_response.retrieve()

        assert dynamic_endpoint.is_closed is True
        assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await dynamic_endpoint.json() == {"foo": "bar"}
        assert isinstance(dynamic_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-endpoints/DYNAMIC_ENDPOINT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.dynamic_endpoints.with_streaming_response.retrieve() as dynamic_endpoint:
            assert not dynamic_endpoint.is_closed
            assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await dynamic_endpoint.json() == {"foo": "bar"}
            assert cast(Any, dynamic_endpoint.is_closed) is True
            assert isinstance(dynamic_endpoint, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, dynamic_endpoint.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-endpoints").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        dynamic_endpoint = await async_client.dynamic_endpoints.list()
        assert dynamic_endpoint.is_closed
        assert await dynamic_endpoint.json() == {"foo": "bar"}
        assert cast(Any, dynamic_endpoint.is_closed) is True
        assert isinstance(dynamic_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-endpoints").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        dynamic_endpoint = await async_client.dynamic_endpoints.with_raw_response.list()

        assert dynamic_endpoint.is_closed is True
        assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await dynamic_endpoint.json() == {"foo": "bar"}
        assert isinstance(dynamic_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-endpoints").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.dynamic_endpoints.with_streaming_response.list() as dynamic_endpoint:
            assert not dynamic_endpoint.is_closed
            assert dynamic_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await dynamic_endpoint.json() == {"foo": "bar"}
            assert cast(Any, dynamic_endpoint.is_closed) is True
            assert isinstance(dynamic_endpoint, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, dynamic_endpoint.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        dynamic_endpoint = await async_client.dynamic_endpoints.delete()
        assert dynamic_endpoint is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.dynamic_endpoints.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dynamic_endpoint = await response.parse()
        assert dynamic_endpoint is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.dynamic_endpoints.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dynamic_endpoint = await response.parse()
            assert dynamic_endpoint is None

        assert cast(Any, response.is_closed) is True
