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


class TestDynamicResourceDocs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_resource_doc = client.dynamic_resource_docs.create(
            body={},
        )
        assert dynamic_resource_doc.is_closed
        assert dynamic_resource_doc.json() == {"foo": "bar"}
        assert cast(Any, dynamic_resource_doc.is_closed) is True
        assert isinstance(dynamic_resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_resource_doc = client.dynamic_resource_docs.with_raw_response.create(
            body={},
        )

        assert dynamic_resource_doc.is_closed is True
        assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert dynamic_resource_doc.json() == {"foo": "bar"}
        assert isinstance(dynamic_resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.dynamic_resource_docs.with_streaming_response.create(
            body={},
        ) as dynamic_resource_doc:
            assert not dynamic_resource_doc.is_closed
            assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert dynamic_resource_doc.json() == {"foo": "bar"}
            assert cast(Any, dynamic_resource_doc.is_closed) is True
            assert isinstance(dynamic_resource_doc, StreamedBinaryAPIResponse)

        assert cast(Any, dynamic_resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_resource_doc = client.dynamic_resource_docs.retrieve()
        assert dynamic_resource_doc.is_closed
        assert dynamic_resource_doc.json() == {"foo": "bar"}
        assert cast(Any, dynamic_resource_doc.is_closed) is True
        assert isinstance(dynamic_resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_resource_doc = client.dynamic_resource_docs.with_raw_response.retrieve()

        assert dynamic_resource_doc.is_closed is True
        assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert dynamic_resource_doc.json() == {"foo": "bar"}
        assert isinstance(dynamic_resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.dynamic_resource_docs.with_streaming_response.retrieve() as dynamic_resource_doc:
            assert not dynamic_resource_doc.is_closed
            assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert dynamic_resource_doc.json() == {"foo": "bar"}
            assert cast(Any, dynamic_resource_doc.is_closed) is True
            assert isinstance(dynamic_resource_doc, StreamedBinaryAPIResponse)

        assert cast(Any, dynamic_resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_resource_doc = client.dynamic_resource_docs.update(
            body={},
        )
        assert dynamic_resource_doc.is_closed
        assert dynamic_resource_doc.json() == {"foo": "bar"}
        assert cast(Any, dynamic_resource_doc.is_closed) is True
        assert isinstance(dynamic_resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_resource_doc = client.dynamic_resource_docs.with_raw_response.update(
            body={},
        )

        assert dynamic_resource_doc.is_closed is True
        assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert dynamic_resource_doc.json() == {"foo": "bar"}
        assert isinstance(dynamic_resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.dynamic_resource_docs.with_streaming_response.update(
            body={},
        ) as dynamic_resource_doc:
            assert not dynamic_resource_doc.is_closed
            assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert dynamic_resource_doc.json() == {"foo": "bar"}
            assert cast(Any, dynamic_resource_doc.is_closed) is True
            assert isinstance(dynamic_resource_doc, StreamedBinaryAPIResponse)

        assert cast(Any, dynamic_resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_resource_doc = client.dynamic_resource_docs.list()
        assert dynamic_resource_doc.is_closed
        assert dynamic_resource_doc.json() == {"foo": "bar"}
        assert cast(Any, dynamic_resource_doc.is_closed) is True
        assert isinstance(dynamic_resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_resource_doc = client.dynamic_resource_docs.with_raw_response.list()

        assert dynamic_resource_doc.is_closed is True
        assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert dynamic_resource_doc.json() == {"foo": "bar"}
        assert isinstance(dynamic_resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.dynamic_resource_docs.with_streaming_response.list() as dynamic_resource_doc:
            assert not dynamic_resource_doc.is_closed
            assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert dynamic_resource_doc.json() == {"foo": "bar"}
            assert cast(Any, dynamic_resource_doc.is_closed) is True
            assert isinstance(dynamic_resource_doc, StreamedBinaryAPIResponse)

        assert cast(Any, dynamic_resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_resource_doc = client.dynamic_resource_docs.delete()
        assert dynamic_resource_doc.is_closed
        assert dynamic_resource_doc.json() == {"foo": "bar"}
        assert cast(Any, dynamic_resource_doc.is_closed) is True
        assert isinstance(dynamic_resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_resource_doc = client.dynamic_resource_docs.with_raw_response.delete()

        assert dynamic_resource_doc.is_closed is True
        assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert dynamic_resource_doc.json() == {"foo": "bar"}
        assert isinstance(dynamic_resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.dynamic_resource_docs.with_streaming_response.delete() as dynamic_resource_doc:
            assert not dynamic_resource_doc.is_closed
            assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert dynamic_resource_doc.json() == {"foo": "bar"}
            assert cast(Any, dynamic_resource_doc.is_closed) is True
            assert isinstance(dynamic_resource_doc, StreamedBinaryAPIResponse)

        assert cast(Any, dynamic_resource_doc.is_closed) is True


class TestAsyncDynamicResourceDocs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_resource_doc = await async_client.dynamic_resource_docs.create(
            body={},
        )
        assert dynamic_resource_doc.is_closed
        assert await dynamic_resource_doc.json() == {"foo": "bar"}
        assert cast(Any, dynamic_resource_doc.is_closed) is True
        assert isinstance(dynamic_resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_resource_doc = await async_client.dynamic_resource_docs.with_raw_response.create(
            body={},
        )

        assert dynamic_resource_doc.is_closed is True
        assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await dynamic_resource_doc.json() == {"foo": "bar"}
        assert isinstance(dynamic_resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.dynamic_resource_docs.with_streaming_response.create(
            body={},
        ) as dynamic_resource_doc:
            assert not dynamic_resource_doc.is_closed
            assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await dynamic_resource_doc.json() == {"foo": "bar"}
            assert cast(Any, dynamic_resource_doc.is_closed) is True
            assert isinstance(dynamic_resource_doc, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, dynamic_resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_resource_doc = await async_client.dynamic_resource_docs.retrieve()
        assert dynamic_resource_doc.is_closed
        assert await dynamic_resource_doc.json() == {"foo": "bar"}
        assert cast(Any, dynamic_resource_doc.is_closed) is True
        assert isinstance(dynamic_resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_resource_doc = await async_client.dynamic_resource_docs.with_raw_response.retrieve()

        assert dynamic_resource_doc.is_closed is True
        assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await dynamic_resource_doc.json() == {"foo": "bar"}
        assert isinstance(dynamic_resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.dynamic_resource_docs.with_streaming_response.retrieve() as dynamic_resource_doc:
            assert not dynamic_resource_doc.is_closed
            assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await dynamic_resource_doc.json() == {"foo": "bar"}
            assert cast(Any, dynamic_resource_doc.is_closed) is True
            assert isinstance(dynamic_resource_doc, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, dynamic_resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_resource_doc = await async_client.dynamic_resource_docs.update(
            body={},
        )
        assert dynamic_resource_doc.is_closed
        assert await dynamic_resource_doc.json() == {"foo": "bar"}
        assert cast(Any, dynamic_resource_doc.is_closed) is True
        assert isinstance(dynamic_resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_resource_doc = await async_client.dynamic_resource_docs.with_raw_response.update(
            body={},
        )

        assert dynamic_resource_doc.is_closed is True
        assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await dynamic_resource_doc.json() == {"foo": "bar"}
        assert isinstance(dynamic_resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.dynamic_resource_docs.with_streaming_response.update(
            body={},
        ) as dynamic_resource_doc:
            assert not dynamic_resource_doc.is_closed
            assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await dynamic_resource_doc.json() == {"foo": "bar"}
            assert cast(Any, dynamic_resource_doc.is_closed) is True
            assert isinstance(dynamic_resource_doc, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, dynamic_resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_resource_doc = await async_client.dynamic_resource_docs.list()
        assert dynamic_resource_doc.is_closed
        assert await dynamic_resource_doc.json() == {"foo": "bar"}
        assert cast(Any, dynamic_resource_doc.is_closed) is True
        assert isinstance(dynamic_resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_resource_doc = await async_client.dynamic_resource_docs.with_raw_response.list()

        assert dynamic_resource_doc.is_closed is True
        assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await dynamic_resource_doc.json() == {"foo": "bar"}
        assert isinstance(dynamic_resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/dynamic-resource-docs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.dynamic_resource_docs.with_streaming_response.list() as dynamic_resource_doc:
            assert not dynamic_resource_doc.is_closed
            assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await dynamic_resource_doc.json() == {"foo": "bar"}
            assert cast(Any, dynamic_resource_doc.is_closed) is True
            assert isinstance(dynamic_resource_doc, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, dynamic_resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_resource_doc = await async_client.dynamic_resource_docs.delete()
        assert dynamic_resource_doc.is_closed
        assert await dynamic_resource_doc.json() == {"foo": "bar"}
        assert cast(Any, dynamic_resource_doc.is_closed) is True
        assert isinstance(dynamic_resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_resource_doc = await async_client.dynamic_resource_docs.with_raw_response.delete()

        assert dynamic_resource_doc.is_closed is True
        assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await dynamic_resource_doc.json() == {"foo": "bar"}
        assert isinstance(dynamic_resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.dynamic_resource_docs.with_streaming_response.delete() as dynamic_resource_doc:
            assert not dynamic_resource_doc.is_closed
            assert dynamic_resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await dynamic_resource_doc.json() == {"foo": "bar"}
            assert cast(Any, dynamic_resource_doc.is_closed) is True
            assert isinstance(dynamic_resource_doc, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, dynamic_resource_doc.is_closed) is True
