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


class TestConnectorMethods:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        connector_method = client.connector_methods.create(
            body={},
        )
        assert connector_method.is_closed
        assert connector_method.json() == {"foo": "bar"}
        assert cast(Any, connector_method.is_closed) is True
        assert isinstance(connector_method, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        connector_method = client.connector_methods.with_raw_response.create(
            body={},
        )

        assert connector_method.is_closed is True
        assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"
        assert connector_method.json() == {"foo": "bar"}
        assert isinstance(connector_method, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.connector_methods.with_streaming_response.create(
            body={},
        ) as connector_method:
            assert not connector_method.is_closed
            assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"

            assert connector_method.json() == {"foo": "bar"}
            assert cast(Any, connector_method.is_closed) is True
            assert isinstance(connector_method, StreamedBinaryAPIResponse)

        assert cast(Any, connector_method.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        connector_method = client.connector_methods.retrieve()
        assert connector_method.is_closed
        assert connector_method.json() == {"foo": "bar"}
        assert cast(Any, connector_method.is_closed) is True
        assert isinstance(connector_method, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        connector_method = client.connector_methods.with_raw_response.retrieve()

        assert connector_method.is_closed is True
        assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"
        assert connector_method.json() == {"foo": "bar"}
        assert isinstance(connector_method, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.connector_methods.with_streaming_response.retrieve() as connector_method:
            assert not connector_method.is_closed
            assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"

            assert connector_method.json() == {"foo": "bar"}
            assert cast(Any, connector_method.is_closed) is True
            assert isinstance(connector_method, StreamedBinaryAPIResponse)

        assert cast(Any, connector_method.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        connector_method = client.connector_methods.update(
            body={},
        )
        assert connector_method.is_closed
        assert connector_method.json() == {"foo": "bar"}
        assert cast(Any, connector_method.is_closed) is True
        assert isinstance(connector_method, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        connector_method = client.connector_methods.with_raw_response.update(
            body={},
        )

        assert connector_method.is_closed is True
        assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"
        assert connector_method.json() == {"foo": "bar"}
        assert isinstance(connector_method, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.connector_methods.with_streaming_response.update(
            body={},
        ) as connector_method:
            assert not connector_method.is_closed
            assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"

            assert connector_method.json() == {"foo": "bar"}
            assert cast(Any, connector_method.is_closed) is True
            assert isinstance(connector_method, StreamedBinaryAPIResponse)

        assert cast(Any, connector_method.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        connector_method = client.connector_methods.list()
        assert connector_method.is_closed
        assert connector_method.json() == {"foo": "bar"}
        assert cast(Any, connector_method.is_closed) is True
        assert isinstance(connector_method, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        connector_method = client.connector_methods.with_raw_response.list()

        assert connector_method.is_closed is True
        assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"
        assert connector_method.json() == {"foo": "bar"}
        assert isinstance(connector_method, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.connector_methods.with_streaming_response.list() as connector_method:
            assert not connector_method.is_closed
            assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"

            assert connector_method.json() == {"foo": "bar"}
            assert cast(Any, connector_method.is_closed) is True
            assert isinstance(connector_method, StreamedBinaryAPIResponse)

        assert cast(Any, connector_method.is_closed) is True


class TestAsyncConnectorMethods:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        connector_method = await async_client.connector_methods.create(
            body={},
        )
        assert connector_method.is_closed
        assert await connector_method.json() == {"foo": "bar"}
        assert cast(Any, connector_method.is_closed) is True
        assert isinstance(connector_method, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        connector_method = await async_client.connector_methods.with_raw_response.create(
            body={},
        )

        assert connector_method.is_closed is True
        assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await connector_method.json() == {"foo": "bar"}
        assert isinstance(connector_method, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.connector_methods.with_streaming_response.create(
            body={},
        ) as connector_method:
            assert not connector_method.is_closed
            assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await connector_method.json() == {"foo": "bar"}
            assert cast(Any, connector_method.is_closed) is True
            assert isinstance(connector_method, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, connector_method.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        connector_method = await async_client.connector_methods.retrieve()
        assert connector_method.is_closed
        assert await connector_method.json() == {"foo": "bar"}
        assert cast(Any, connector_method.is_closed) is True
        assert isinstance(connector_method, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        connector_method = await async_client.connector_methods.with_raw_response.retrieve()

        assert connector_method.is_closed is True
        assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await connector_method.json() == {"foo": "bar"}
        assert isinstance(connector_method, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.connector_methods.with_streaming_response.retrieve() as connector_method:
            assert not connector_method.is_closed
            assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await connector_method.json() == {"foo": "bar"}
            assert cast(Any, connector_method.is_closed) is True
            assert isinstance(connector_method, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, connector_method.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        connector_method = await async_client.connector_methods.update(
            body={},
        )
        assert connector_method.is_closed
        assert await connector_method.json() == {"foo": "bar"}
        assert cast(Any, connector_method.is_closed) is True
        assert isinstance(connector_method, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        connector_method = await async_client.connector_methods.with_raw_response.update(
            body={},
        )

        assert connector_method.is_closed is True
        assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await connector_method.json() == {"foo": "bar"}
        assert isinstance(connector_method, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.connector_methods.with_streaming_response.update(
            body={},
        ) as connector_method:
            assert not connector_method.is_closed
            assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await connector_method.json() == {"foo": "bar"}
            assert cast(Any, connector_method.is_closed) is True
            assert isinstance(connector_method, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, connector_method.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        connector_method = await async_client.connector_methods.list()
        assert connector_method.is_closed
        assert await connector_method.json() == {"foo": "bar"}
        assert cast(Any, connector_method.is_closed) is True
        assert isinstance(connector_method, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        connector_method = await async_client.connector_methods.with_raw_response.list()

        assert connector_method.is_closed is True
        assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await connector_method.json() == {"foo": "bar"}
        assert isinstance(connector_method, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/connector-methods").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.connector_methods.with_streaming_response.list() as connector_method:
            assert not connector_method.is_closed
            assert connector_method.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await connector_method.json() == {"foo": "bar"}
            assert cast(Any, connector_method.is_closed) is True
            assert isinstance(connector_method, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, connector_method.is_closed) is True
