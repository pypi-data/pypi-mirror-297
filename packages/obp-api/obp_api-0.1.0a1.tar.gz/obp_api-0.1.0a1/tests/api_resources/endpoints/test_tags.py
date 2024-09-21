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


class TestTags:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tag = client.endpoints.tags.create(
            body={},
        )
        assert tag.is_closed
        assert tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tag = client.endpoints.tags.with_raw_response.create(
            body={},
        )

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert tag.json() == {"foo": "bar"}
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.endpoints.tags.with_streaming_response.create(
            body={},
        ) as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, StreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tag = client.endpoints.tags.update(
            body={},
        )
        assert tag.is_closed
        assert tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tag = client.endpoints.tags.with_raw_response.update(
            body={},
        )

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert tag.json() == {"foo": "bar"}
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.endpoints.tags.with_streaming_response.update(
            body={},
        ) as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, StreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tag = client.endpoints.tags.list()
        assert tag.is_closed
        assert tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tag = client.endpoints.tags.with_raw_response.list()

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert tag.json() == {"foo": "bar"}
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.endpoints.tags.with_streaming_response.list() as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, StreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tag = client.endpoints.tags.delete()
        assert tag.is_closed
        assert tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tag = client.endpoints.tags.with_raw_response.delete()

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert tag.json() == {"foo": "bar"}
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.endpoints.tags.with_streaming_response.delete() as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, StreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True


class TestAsyncTags:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tag = await async_client.endpoints.tags.create(
            body={},
        )
        assert tag.is_closed
        assert await tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tag = await async_client.endpoints.tags.with_raw_response.create(
            body={},
        )

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await tag.json() == {"foo": "bar"}
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.endpoints.tags.with_streaming_response.create(
            body={},
        ) as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tag = await async_client.endpoints.tags.update(
            body={},
        )
        assert tag.is_closed
        assert await tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tag = await async_client.endpoints.tags.with_raw_response.update(
            body={},
        )

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await tag.json() == {"foo": "bar"}
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.endpoints.tags.with_streaming_response.update(
            body={},
        ) as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tag = await async_client.endpoints.tags.list()
        assert tag.is_closed
        assert await tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tag = await async_client.endpoints.tags.with_raw_response.list()

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await tag.json() == {"foo": "bar"}
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.endpoints.tags.with_streaming_response.list() as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        tag = await async_client.endpoints.tags.delete()
        assert tag.is_closed
        assert await tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        tag = await async_client.endpoints.tags.with_raw_response.delete()

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await tag.json() == {"foo": "bar"}
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.endpoints.tags.with_streaming_response.delete() as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True
