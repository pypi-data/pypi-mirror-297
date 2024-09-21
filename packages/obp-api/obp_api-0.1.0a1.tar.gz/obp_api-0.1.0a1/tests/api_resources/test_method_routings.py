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


class TestMethodRoutings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        method_routing = client.method_routings.create(
            body={},
        )
        assert method_routing.is_closed
        assert method_routing.json() == {"foo": "bar"}
        assert cast(Any, method_routing.is_closed) is True
        assert isinstance(method_routing, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        method_routing = client.method_routings.with_raw_response.create(
            body={},
        )

        assert method_routing.is_closed is True
        assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"
        assert method_routing.json() == {"foo": "bar"}
        assert isinstance(method_routing, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.method_routings.with_streaming_response.create(
            body={},
        ) as method_routing:
            assert not method_routing.is_closed
            assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"

            assert method_routing.json() == {"foo": "bar"}
            assert cast(Any, method_routing.is_closed) is True
            assert isinstance(method_routing, StreamedBinaryAPIResponse)

        assert cast(Any, method_routing.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/method_routings/METHOD_ROUTING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        method_routing = client.method_routings.update(
            method_routing_id="METHOD_ROUTING_ID",
            body={},
        )
        assert method_routing.is_closed
        assert method_routing.json() == {"foo": "bar"}
        assert cast(Any, method_routing.is_closed) is True
        assert isinstance(method_routing, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/method_routings/METHOD_ROUTING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        method_routing = client.method_routings.with_raw_response.update(
            method_routing_id="METHOD_ROUTING_ID",
            body={},
        )

        assert method_routing.is_closed is True
        assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"
        assert method_routing.json() == {"foo": "bar"}
        assert isinstance(method_routing, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/method_routings/METHOD_ROUTING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.method_routings.with_streaming_response.update(
            method_routing_id="METHOD_ROUTING_ID",
            body={},
        ) as method_routing:
            assert not method_routing.is_closed
            assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"

            assert method_routing.json() == {"foo": "bar"}
            assert cast(Any, method_routing.is_closed) is True
            assert isinstance(method_routing, StreamedBinaryAPIResponse)

        assert cast(Any, method_routing.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `method_routing_id` but received ''"):
            client.method_routings.with_raw_response.update(
                method_routing_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        method_routing = client.method_routings.list()
        assert method_routing.is_closed
        assert method_routing.json() == {"foo": "bar"}
        assert cast(Any, method_routing.is_closed) is True
        assert isinstance(method_routing, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        method_routing = client.method_routings.with_raw_response.list()

        assert method_routing.is_closed is True
        assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"
        assert method_routing.json() == {"foo": "bar"}
        assert isinstance(method_routing, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.method_routings.with_streaming_response.list() as method_routing:
            assert not method_routing.is_closed
            assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"

            assert method_routing.json() == {"foo": "bar"}
            assert cast(Any, method_routing.is_closed) is True
            assert isinstance(method_routing, StreamedBinaryAPIResponse)

        assert cast(Any, method_routing.is_closed) is True

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        method_routing = client.method_routings.delete(
            "METHOD_ROUTING_ID",
        )
        assert method_routing is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.method_routings.with_raw_response.delete(
            "METHOD_ROUTING_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        method_routing = response.parse()
        assert method_routing is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.method_routings.with_streaming_response.delete(
            "METHOD_ROUTING_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            method_routing = response.parse()
            assert method_routing is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `method_routing_id` but received ''"):
            client.method_routings.with_raw_response.delete(
                "",
            )


class TestAsyncMethodRoutings:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        method_routing = await async_client.method_routings.create(
            body={},
        )
        assert method_routing.is_closed
        assert await method_routing.json() == {"foo": "bar"}
        assert cast(Any, method_routing.is_closed) is True
        assert isinstance(method_routing, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        method_routing = await async_client.method_routings.with_raw_response.create(
            body={},
        )

        assert method_routing.is_closed is True
        assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await method_routing.json() == {"foo": "bar"}
        assert isinstance(method_routing, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.method_routings.with_streaming_response.create(
            body={},
        ) as method_routing:
            assert not method_routing.is_closed
            assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await method_routing.json() == {"foo": "bar"}
            assert cast(Any, method_routing.is_closed) is True
            assert isinstance(method_routing, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, method_routing.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/method_routings/METHOD_ROUTING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        method_routing = await async_client.method_routings.update(
            method_routing_id="METHOD_ROUTING_ID",
            body={},
        )
        assert method_routing.is_closed
        assert await method_routing.json() == {"foo": "bar"}
        assert cast(Any, method_routing.is_closed) is True
        assert isinstance(method_routing, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/method_routings/METHOD_ROUTING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        method_routing = await async_client.method_routings.with_raw_response.update(
            method_routing_id="METHOD_ROUTING_ID",
            body={},
        )

        assert method_routing.is_closed is True
        assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await method_routing.json() == {"foo": "bar"}
        assert isinstance(method_routing, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/method_routings/METHOD_ROUTING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.method_routings.with_streaming_response.update(
            method_routing_id="METHOD_ROUTING_ID",
            body={},
        ) as method_routing:
            assert not method_routing.is_closed
            assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await method_routing.json() == {"foo": "bar"}
            assert cast(Any, method_routing.is_closed) is True
            assert isinstance(method_routing, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, method_routing.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `method_routing_id` but received ''"):
            await async_client.method_routings.with_raw_response.update(
                method_routing_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        method_routing = await async_client.method_routings.list()
        assert method_routing.is_closed
        assert await method_routing.json() == {"foo": "bar"}
        assert cast(Any, method_routing.is_closed) is True
        assert isinstance(method_routing, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        method_routing = await async_client.method_routings.with_raw_response.list()

        assert method_routing.is_closed is True
        assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await method_routing.json() == {"foo": "bar"}
        assert isinstance(method_routing, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/method_routings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.method_routings.with_streaming_response.list() as method_routing:
            assert not method_routing.is_closed
            assert method_routing.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await method_routing.json() == {"foo": "bar"}
            assert cast(Any, method_routing.is_closed) is True
            assert isinstance(method_routing, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, method_routing.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        method_routing = await async_client.method_routings.delete(
            "METHOD_ROUTING_ID",
        )
        assert method_routing is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.method_routings.with_raw_response.delete(
            "METHOD_ROUTING_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        method_routing = await response.parse()
        assert method_routing is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.method_routings.with_streaming_response.delete(
            "METHOD_ROUTING_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            method_routing = await response.parse()
            assert method_routing is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `method_routing_id` but received ''"):
            await async_client.method_routings.with_raw_response.delete(
                "",
            )
