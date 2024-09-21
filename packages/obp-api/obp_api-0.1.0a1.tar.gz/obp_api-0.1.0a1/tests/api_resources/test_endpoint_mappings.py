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


class TestEndpointMappings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_mapping = client.endpoint_mappings.create(
            body={},
        )
        assert endpoint_mapping.is_closed
        assert endpoint_mapping.json() == {"foo": "bar"}
        assert cast(Any, endpoint_mapping.is_closed) is True
        assert isinstance(endpoint_mapping, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_mapping = client.endpoint_mappings.with_raw_response.create(
            body={},
        )

        assert endpoint_mapping.is_closed is True
        assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"
        assert endpoint_mapping.json() == {"foo": "bar"}
        assert isinstance(endpoint_mapping, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.endpoint_mappings.with_streaming_response.create(
            body={},
        ) as endpoint_mapping:
            assert not endpoint_mapping.is_closed
            assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"

            assert endpoint_mapping.json() == {"foo": "bar"}
            assert cast(Any, endpoint_mapping.is_closed) is True
            assert isinstance(endpoint_mapping, StreamedBinaryAPIResponse)

        assert cast(Any, endpoint_mapping.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_mapping = client.endpoint_mappings.retrieve()
        assert endpoint_mapping.is_closed
        assert endpoint_mapping.json() == {"foo": "bar"}
        assert cast(Any, endpoint_mapping.is_closed) is True
        assert isinstance(endpoint_mapping, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_mapping = client.endpoint_mappings.with_raw_response.retrieve()

        assert endpoint_mapping.is_closed is True
        assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"
        assert endpoint_mapping.json() == {"foo": "bar"}
        assert isinstance(endpoint_mapping, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.endpoint_mappings.with_streaming_response.retrieve() as endpoint_mapping:
            assert not endpoint_mapping.is_closed
            assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"

            assert endpoint_mapping.json() == {"foo": "bar"}
            assert cast(Any, endpoint_mapping.is_closed) is True
            assert isinstance(endpoint_mapping, StreamedBinaryAPIResponse)

        assert cast(Any, endpoint_mapping.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_mapping = client.endpoint_mappings.update(
            body={},
        )
        assert endpoint_mapping.is_closed
        assert endpoint_mapping.json() == {"foo": "bar"}
        assert cast(Any, endpoint_mapping.is_closed) is True
        assert isinstance(endpoint_mapping, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_mapping = client.endpoint_mappings.with_raw_response.update(
            body={},
        )

        assert endpoint_mapping.is_closed is True
        assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"
        assert endpoint_mapping.json() == {"foo": "bar"}
        assert isinstance(endpoint_mapping, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.endpoint_mappings.with_streaming_response.update(
            body={},
        ) as endpoint_mapping:
            assert not endpoint_mapping.is_closed
            assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"

            assert endpoint_mapping.json() == {"foo": "bar"}
            assert cast(Any, endpoint_mapping.is_closed) is True
            assert isinstance(endpoint_mapping, StreamedBinaryAPIResponse)

        assert cast(Any, endpoint_mapping.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_mapping = client.endpoint_mappings.list()
        assert endpoint_mapping.is_closed
        assert endpoint_mapping.json() == {"foo": "bar"}
        assert cast(Any, endpoint_mapping.is_closed) is True
        assert isinstance(endpoint_mapping, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_mapping = client.endpoint_mappings.with_raw_response.list()

        assert endpoint_mapping.is_closed is True
        assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"
        assert endpoint_mapping.json() == {"foo": "bar"}
        assert isinstance(endpoint_mapping, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.endpoint_mappings.with_streaming_response.list() as endpoint_mapping:
            assert not endpoint_mapping.is_closed
            assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"

            assert endpoint_mapping.json() == {"foo": "bar"}
            assert cast(Any, endpoint_mapping.is_closed) is True
            assert isinstance(endpoint_mapping, StreamedBinaryAPIResponse)

        assert cast(Any, endpoint_mapping.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_mapping = client.endpoint_mappings.delete()
        assert endpoint_mapping.is_closed
        assert endpoint_mapping.json() == {"foo": "bar"}
        assert cast(Any, endpoint_mapping.is_closed) is True
        assert isinstance(endpoint_mapping, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_mapping = client.endpoint_mappings.with_raw_response.delete()

        assert endpoint_mapping.is_closed is True
        assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"
        assert endpoint_mapping.json() == {"foo": "bar"}
        assert isinstance(endpoint_mapping, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.endpoint_mappings.with_streaming_response.delete() as endpoint_mapping:
            assert not endpoint_mapping.is_closed
            assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"

            assert endpoint_mapping.json() == {"foo": "bar"}
            assert cast(Any, endpoint_mapping.is_closed) is True
            assert isinstance(endpoint_mapping, StreamedBinaryAPIResponse)

        assert cast(Any, endpoint_mapping.is_closed) is True


class TestAsyncEndpointMappings:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_mapping = await async_client.endpoint_mappings.create(
            body={},
        )
        assert endpoint_mapping.is_closed
        assert await endpoint_mapping.json() == {"foo": "bar"}
        assert cast(Any, endpoint_mapping.is_closed) is True
        assert isinstance(endpoint_mapping, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_mapping = await async_client.endpoint_mappings.with_raw_response.create(
            body={},
        )

        assert endpoint_mapping.is_closed is True
        assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await endpoint_mapping.json() == {"foo": "bar"}
        assert isinstance(endpoint_mapping, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.endpoint_mappings.with_streaming_response.create(
            body={},
        ) as endpoint_mapping:
            assert not endpoint_mapping.is_closed
            assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await endpoint_mapping.json() == {"foo": "bar"}
            assert cast(Any, endpoint_mapping.is_closed) is True
            assert isinstance(endpoint_mapping, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, endpoint_mapping.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_mapping = await async_client.endpoint_mappings.retrieve()
        assert endpoint_mapping.is_closed
        assert await endpoint_mapping.json() == {"foo": "bar"}
        assert cast(Any, endpoint_mapping.is_closed) is True
        assert isinstance(endpoint_mapping, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_mapping = await async_client.endpoint_mappings.with_raw_response.retrieve()

        assert endpoint_mapping.is_closed is True
        assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await endpoint_mapping.json() == {"foo": "bar"}
        assert isinstance(endpoint_mapping, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.endpoint_mappings.with_streaming_response.retrieve() as endpoint_mapping:
            assert not endpoint_mapping.is_closed
            assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await endpoint_mapping.json() == {"foo": "bar"}
            assert cast(Any, endpoint_mapping.is_closed) is True
            assert isinstance(endpoint_mapping, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, endpoint_mapping.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_mapping = await async_client.endpoint_mappings.update(
            body={},
        )
        assert endpoint_mapping.is_closed
        assert await endpoint_mapping.json() == {"foo": "bar"}
        assert cast(Any, endpoint_mapping.is_closed) is True
        assert isinstance(endpoint_mapping, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_mapping = await async_client.endpoint_mappings.with_raw_response.update(
            body={},
        )

        assert endpoint_mapping.is_closed is True
        assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await endpoint_mapping.json() == {"foo": "bar"}
        assert isinstance(endpoint_mapping, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.endpoint_mappings.with_streaming_response.update(
            body={},
        ) as endpoint_mapping:
            assert not endpoint_mapping.is_closed
            assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await endpoint_mapping.json() == {"foo": "bar"}
            assert cast(Any, endpoint_mapping.is_closed) is True
            assert isinstance(endpoint_mapping, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, endpoint_mapping.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_mapping = await async_client.endpoint_mappings.list()
        assert endpoint_mapping.is_closed
        assert await endpoint_mapping.json() == {"foo": "bar"}
        assert cast(Any, endpoint_mapping.is_closed) is True
        assert isinstance(endpoint_mapping, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_mapping = await async_client.endpoint_mappings.with_raw_response.list()

        assert endpoint_mapping.is_closed is True
        assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await endpoint_mapping.json() == {"foo": "bar"}
        assert isinstance(endpoint_mapping, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoint-mappings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.endpoint_mappings.with_streaming_response.list() as endpoint_mapping:
            assert not endpoint_mapping.is_closed
            assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await endpoint_mapping.json() == {"foo": "bar"}
            assert cast(Any, endpoint_mapping.is_closed) is True
            assert isinstance(endpoint_mapping, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, endpoint_mapping.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        endpoint_mapping = await async_client.endpoint_mappings.delete()
        assert endpoint_mapping.is_closed
        assert await endpoint_mapping.json() == {"foo": "bar"}
        assert cast(Any, endpoint_mapping.is_closed) is True
        assert isinstance(endpoint_mapping, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        endpoint_mapping = await async_client.endpoint_mappings.with_raw_response.delete()

        assert endpoint_mapping.is_closed is True
        assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await endpoint_mapping.json() == {"foo": "bar"}
        assert isinstance(endpoint_mapping, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.endpoint_mappings.with_streaming_response.delete() as endpoint_mapping:
            assert not endpoint_mapping.is_closed
            assert endpoint_mapping.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await endpoint_mapping.json() == {"foo": "bar"}
            assert cast(Any, endpoint_mapping.is_closed) is True
            assert isinstance(endpoint_mapping, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, endpoint_mapping.is_closed) is True
