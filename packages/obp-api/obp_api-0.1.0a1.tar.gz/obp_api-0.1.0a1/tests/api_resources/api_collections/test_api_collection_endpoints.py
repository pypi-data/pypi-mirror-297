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


class TestAPICollectionEndpoints:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        api_collection_endpoint = client.api_collections.api_collection_endpoints.create(
            body={},
        )
        assert api_collection_endpoint.is_closed
        assert api_collection_endpoint.json() == {"foo": "bar"}
        assert cast(Any, api_collection_endpoint.is_closed) is True
        assert isinstance(api_collection_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        api_collection_endpoint = client.api_collections.api_collection_endpoints.with_raw_response.create(
            body={},
        )

        assert api_collection_endpoint.is_closed is True
        assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert api_collection_endpoint.json() == {"foo": "bar"}
        assert isinstance(api_collection_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.api_collections.api_collection_endpoints.with_streaming_response.create(
            body={},
        ) as api_collection_endpoint:
            assert not api_collection_endpoint.is_closed
            assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert api_collection_endpoint.json() == {"foo": "bar"}
            assert cast(Any, api_collection_endpoint.is_closed) is True
            assert isinstance(api_collection_endpoint, StreamedBinaryAPIResponse)

        assert cast(Any, api_collection_endpoint.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        api_collection_endpoint = client.api_collections.api_collection_endpoints.retrieve()
        assert api_collection_endpoint.is_closed
        assert api_collection_endpoint.json() == {"foo": "bar"}
        assert cast(Any, api_collection_endpoint.is_closed) is True
        assert isinstance(api_collection_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        api_collection_endpoint = client.api_collections.api_collection_endpoints.with_raw_response.retrieve()

        assert api_collection_endpoint.is_closed is True
        assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert api_collection_endpoint.json() == {"foo": "bar"}
        assert isinstance(api_collection_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.api_collections.api_collection_endpoints.with_streaming_response.retrieve() as api_collection_endpoint:
            assert not api_collection_endpoint.is_closed
            assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert api_collection_endpoint.json() == {"foo": "bar"}
            assert cast(Any, api_collection_endpoint.is_closed) is True
            assert isinstance(api_collection_endpoint, StreamedBinaryAPIResponse)

        assert cast(Any, api_collection_endpoint.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/API_COLLECTION_ID/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        api_collection_endpoint = client.api_collections.api_collection_endpoints.list()
        assert api_collection_endpoint.is_closed
        assert api_collection_endpoint.json() == {"foo": "bar"}
        assert cast(Any, api_collection_endpoint.is_closed) is True
        assert isinstance(api_collection_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/API_COLLECTION_ID/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        api_collection_endpoint = client.api_collections.api_collection_endpoints.with_raw_response.list()

        assert api_collection_endpoint.is_closed is True
        assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert api_collection_endpoint.json() == {"foo": "bar"}
        assert isinstance(api_collection_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/API_COLLECTION_ID/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.api_collections.api_collection_endpoints.with_streaming_response.list() as api_collection_endpoint:
            assert not api_collection_endpoint.is_closed
            assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert api_collection_endpoint.json() == {"foo": "bar"}
            assert cast(Any, api_collection_endpoint.is_closed) is True
            assert isinstance(api_collection_endpoint, StreamedBinaryAPIResponse)

        assert cast(Any, api_collection_endpoint.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        api_collection_endpoint = client.api_collections.api_collection_endpoints.delete()
        assert api_collection_endpoint.is_closed
        assert api_collection_endpoint.json() == {"foo": "bar"}
        assert cast(Any, api_collection_endpoint.is_closed) is True
        assert isinstance(api_collection_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        api_collection_endpoint = client.api_collections.api_collection_endpoints.with_raw_response.delete()

        assert api_collection_endpoint.is_closed is True
        assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert api_collection_endpoint.json() == {"foo": "bar"}
        assert isinstance(api_collection_endpoint, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.api_collections.api_collection_endpoints.with_streaming_response.delete() as api_collection_endpoint:
            assert not api_collection_endpoint.is_closed
            assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert api_collection_endpoint.json() == {"foo": "bar"}
            assert cast(Any, api_collection_endpoint.is_closed) is True
            assert isinstance(api_collection_endpoint, StreamedBinaryAPIResponse)

        assert cast(Any, api_collection_endpoint.is_closed) is True


class TestAsyncAPICollectionEndpoints:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        api_collection_endpoint = await async_client.api_collections.api_collection_endpoints.create(
            body={},
        )
        assert api_collection_endpoint.is_closed
        assert await api_collection_endpoint.json() == {"foo": "bar"}
        assert cast(Any, api_collection_endpoint.is_closed) is True
        assert isinstance(api_collection_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        api_collection_endpoint = await async_client.api_collections.api_collection_endpoints.with_raw_response.create(
            body={},
        )

        assert api_collection_endpoint.is_closed is True
        assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await api_collection_endpoint.json() == {"foo": "bar"}
        assert isinstance(api_collection_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.api_collections.api_collection_endpoints.with_streaming_response.create(
            body={},
        ) as api_collection_endpoint:
            assert not api_collection_endpoint.is_closed
            assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await api_collection_endpoint.json() == {"foo": "bar"}
            assert cast(Any, api_collection_endpoint.is_closed) is True
            assert isinstance(api_collection_endpoint, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, api_collection_endpoint.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        api_collection_endpoint = await async_client.api_collections.api_collection_endpoints.retrieve()
        assert api_collection_endpoint.is_closed
        assert await api_collection_endpoint.json() == {"foo": "bar"}
        assert cast(Any, api_collection_endpoint.is_closed) is True
        assert isinstance(api_collection_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        api_collection_endpoint = (
            await async_client.api_collections.api_collection_endpoints.with_raw_response.retrieve()
        )

        assert api_collection_endpoint.is_closed is True
        assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await api_collection_endpoint.json() == {"foo": "bar"}
        assert isinstance(api_collection_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.api_collections.api_collection_endpoints.with_streaming_response.retrieve() as api_collection_endpoint:
            assert not api_collection_endpoint.is_closed
            assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await api_collection_endpoint.json() == {"foo": "bar"}
            assert cast(Any, api_collection_endpoint.is_closed) is True
            assert isinstance(api_collection_endpoint, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, api_collection_endpoint.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/API_COLLECTION_ID/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        api_collection_endpoint = await async_client.api_collections.api_collection_endpoints.list()
        assert api_collection_endpoint.is_closed
        assert await api_collection_endpoint.json() == {"foo": "bar"}
        assert cast(Any, api_collection_endpoint.is_closed) is True
        assert isinstance(api_collection_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/API_COLLECTION_ID/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        api_collection_endpoint = await async_client.api_collections.api_collection_endpoints.with_raw_response.list()

        assert api_collection_endpoint.is_closed is True
        assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await api_collection_endpoint.json() == {"foo": "bar"}
        assert isinstance(api_collection_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/api-collections/API_COLLECTION_ID/api-collection-endpoints").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.api_collections.api_collection_endpoints.with_streaming_response.list() as api_collection_endpoint:
            assert not api_collection_endpoint.is_closed
            assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await api_collection_endpoint.json() == {"foo": "bar"}
            assert cast(Any, api_collection_endpoint.is_closed) is True
            assert isinstance(api_collection_endpoint, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, api_collection_endpoint.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        api_collection_endpoint = await async_client.api_collections.api_collection_endpoints.delete()
        assert api_collection_endpoint.is_closed
        assert await api_collection_endpoint.json() == {"foo": "bar"}
        assert cast(Any, api_collection_endpoint.is_closed) is True
        assert isinstance(api_collection_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        api_collection_endpoint = await async_client.api_collections.api_collection_endpoints.with_raw_response.delete()

        assert api_collection_endpoint.is_closed is True
        assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await api_collection_endpoint.json() == {"foo": "bar"}
        assert isinstance(api_collection_endpoint, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.api_collections.api_collection_endpoints.with_streaming_response.delete() as api_collection_endpoint:
            assert not api_collection_endpoint.is_closed
            assert api_collection_endpoint.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await api_collection_endpoint.json() == {"foo": "bar"}
            assert cast(Any, api_collection_endpoint.is_closed) is True
            assert isinstance(api_collection_endpoint, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, api_collection_endpoint.is_closed) is True
