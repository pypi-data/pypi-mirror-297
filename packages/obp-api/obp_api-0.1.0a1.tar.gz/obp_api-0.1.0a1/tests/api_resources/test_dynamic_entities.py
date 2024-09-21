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


class TestDynamicEntities:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/my/dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_entity = client.dynamic_entities.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        )
        assert dynamic_entity.is_closed
        assert dynamic_entity.json() == {"foo": "bar"}
        assert cast(Any, dynamic_entity.is_closed) is True
        assert isinstance(dynamic_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/my/dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_entity = client.dynamic_entities.with_raw_response.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        )

        assert dynamic_entity.is_closed is True
        assert dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert dynamic_entity.json() == {"foo": "bar"}
        assert isinstance(dynamic_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/my/dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.dynamic_entities.with_streaming_response.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        ) as dynamic_entity:
            assert not dynamic_entity.is_closed
            assert dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert dynamic_entity.json() == {"foo": "bar"}
            assert cast(Any, dynamic_entity.is_closed) is True
            assert isinstance(dynamic_entity, StreamedBinaryAPIResponse)

        assert cast(Any, dynamic_entity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dynamic_entity_id` but received ''"):
            client.dynamic_entities.with_raw_response.update(
                dynamic_entity_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        dynamic_entity = client.dynamic_entities.list()
        assert dynamic_entity.is_closed
        assert dynamic_entity.json() == {"foo": "bar"}
        assert cast(Any, dynamic_entity.is_closed) is True
        assert isinstance(dynamic_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        dynamic_entity = client.dynamic_entities.with_raw_response.list()

        assert dynamic_entity.is_closed is True
        assert dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert dynamic_entity.json() == {"foo": "bar"}
        assert isinstance(dynamic_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.dynamic_entities.with_streaming_response.list() as dynamic_entity:
            assert not dynamic_entity.is_closed
            assert dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert dynamic_entity.json() == {"foo": "bar"}
            assert cast(Any, dynamic_entity.is_closed) is True
            assert isinstance(dynamic_entity, StreamedBinaryAPIResponse)

        assert cast(Any, dynamic_entity.is_closed) is True

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        dynamic_entity = client.dynamic_entities.delete(
            "DYNAMIC_ENTITY_ID",
        )
        assert dynamic_entity is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.dynamic_entities.with_raw_response.delete(
            "DYNAMIC_ENTITY_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dynamic_entity = response.parse()
        assert dynamic_entity is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.dynamic_entities.with_streaming_response.delete(
            "DYNAMIC_ENTITY_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dynamic_entity = response.parse()
            assert dynamic_entity is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dynamic_entity_id` but received ''"):
            client.dynamic_entities.with_raw_response.delete(
                "",
            )


class TestAsyncDynamicEntities:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/my/dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        dynamic_entity = await async_client.dynamic_entities.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        )
        assert dynamic_entity.is_closed
        assert await dynamic_entity.json() == {"foo": "bar"}
        assert cast(Any, dynamic_entity.is_closed) is True
        assert isinstance(dynamic_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/my/dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        dynamic_entity = await async_client.dynamic_entities.with_raw_response.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        )

        assert dynamic_entity.is_closed is True
        assert dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await dynamic_entity.json() == {"foo": "bar"}
        assert isinstance(dynamic_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/my/dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.dynamic_entities.with_streaming_response.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        ) as dynamic_entity:
            assert not dynamic_entity.is_closed
            assert dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await dynamic_entity.json() == {"foo": "bar"}
            assert cast(Any, dynamic_entity.is_closed) is True
            assert isinstance(dynamic_entity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, dynamic_entity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dynamic_entity_id` but received ''"):
            await async_client.dynamic_entities.with_raw_response.update(
                dynamic_entity_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        dynamic_entity = await async_client.dynamic_entities.list()
        assert dynamic_entity.is_closed
        assert await dynamic_entity.json() == {"foo": "bar"}
        assert cast(Any, dynamic_entity.is_closed) is True
        assert isinstance(dynamic_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        dynamic_entity = await async_client.dynamic_entities.with_raw_response.list()

        assert dynamic_entity.is_closed is True
        assert dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await dynamic_entity.json() == {"foo": "bar"}
        assert isinstance(dynamic_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/dynamic-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.dynamic_entities.with_streaming_response.list() as dynamic_entity:
            assert not dynamic_entity.is_closed
            assert dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await dynamic_entity.json() == {"foo": "bar"}
            assert cast(Any, dynamic_entity.is_closed) is True
            assert isinstance(dynamic_entity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, dynamic_entity.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        dynamic_entity = await async_client.dynamic_entities.delete(
            "DYNAMIC_ENTITY_ID",
        )
        assert dynamic_entity is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.dynamic_entities.with_raw_response.delete(
            "DYNAMIC_ENTITY_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dynamic_entity = await response.parse()
        assert dynamic_entity is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.dynamic_entities.with_streaming_response.delete(
            "DYNAMIC_ENTITY_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dynamic_entity = await response.parse()
            assert dynamic_entity is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dynamic_entity_id` but received ''"):
            await async_client.dynamic_entities.with_raw_response.delete(
                "",
            )
