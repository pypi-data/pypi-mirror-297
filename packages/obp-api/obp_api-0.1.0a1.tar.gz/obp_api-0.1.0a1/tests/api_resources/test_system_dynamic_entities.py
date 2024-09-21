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


class TestSystemDynamicEntities:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_dynamic_entity = client.system_dynamic_entities.create(
            body={},
        )
        assert system_dynamic_entity.is_closed
        assert system_dynamic_entity.json() == {"foo": "bar"}
        assert cast(Any, system_dynamic_entity.is_closed) is True
        assert isinstance(system_dynamic_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_dynamic_entity = client.system_dynamic_entities.with_raw_response.create(
            body={},
        )

        assert system_dynamic_entity.is_closed is True
        assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert system_dynamic_entity.json() == {"foo": "bar"}
        assert isinstance(system_dynamic_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.system_dynamic_entities.with_streaming_response.create(
            body={},
        ) as system_dynamic_entity:
            assert not system_dynamic_entity.is_closed
            assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert system_dynamic_entity.json() == {"foo": "bar"}
            assert cast(Any, system_dynamic_entity.is_closed) is True
            assert isinstance(system_dynamic_entity, StreamedBinaryAPIResponse)

        assert cast(Any, system_dynamic_entity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/system-dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_dynamic_entity = client.system_dynamic_entities.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        )
        assert system_dynamic_entity.is_closed
        assert system_dynamic_entity.json() == {"foo": "bar"}
        assert cast(Any, system_dynamic_entity.is_closed) is True
        assert isinstance(system_dynamic_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/system-dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_dynamic_entity = client.system_dynamic_entities.with_raw_response.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        )

        assert system_dynamic_entity.is_closed is True
        assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert system_dynamic_entity.json() == {"foo": "bar"}
        assert isinstance(system_dynamic_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/system-dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.system_dynamic_entities.with_streaming_response.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        ) as system_dynamic_entity:
            assert not system_dynamic_entity.is_closed
            assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert system_dynamic_entity.json() == {"foo": "bar"}
            assert cast(Any, system_dynamic_entity.is_closed) is True
            assert isinstance(system_dynamic_entity, StreamedBinaryAPIResponse)

        assert cast(Any, system_dynamic_entity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dynamic_entity_id` but received ''"):
            client.system_dynamic_entities.with_raw_response.update(
                dynamic_entity_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_dynamic_entity = client.system_dynamic_entities.list()
        assert system_dynamic_entity.is_closed
        assert system_dynamic_entity.json() == {"foo": "bar"}
        assert cast(Any, system_dynamic_entity.is_closed) is True
        assert isinstance(system_dynamic_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_dynamic_entity = client.system_dynamic_entities.with_raw_response.list()

        assert system_dynamic_entity.is_closed is True
        assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert system_dynamic_entity.json() == {"foo": "bar"}
        assert isinstance(system_dynamic_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.system_dynamic_entities.with_streaming_response.list() as system_dynamic_entity:
            assert not system_dynamic_entity.is_closed
            assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert system_dynamic_entity.json() == {"foo": "bar"}
            assert cast(Any, system_dynamic_entity.is_closed) is True
            assert isinstance(system_dynamic_entity, StreamedBinaryAPIResponse)

        assert cast(Any, system_dynamic_entity.is_closed) is True

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        system_dynamic_entity = client.system_dynamic_entities.delete(
            "DYNAMIC_ENTITY_ID",
        )
        assert system_dynamic_entity is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.system_dynamic_entities.with_raw_response.delete(
            "DYNAMIC_ENTITY_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        system_dynamic_entity = response.parse()
        assert system_dynamic_entity is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.system_dynamic_entities.with_streaming_response.delete(
            "DYNAMIC_ENTITY_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            system_dynamic_entity = response.parse()
            assert system_dynamic_entity is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dynamic_entity_id` but received ''"):
            client.system_dynamic_entities.with_raw_response.delete(
                "",
            )


class TestAsyncSystemDynamicEntities:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_dynamic_entity = await async_client.system_dynamic_entities.create(
            body={},
        )
        assert system_dynamic_entity.is_closed
        assert await system_dynamic_entity.json() == {"foo": "bar"}
        assert cast(Any, system_dynamic_entity.is_closed) is True
        assert isinstance(system_dynamic_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_dynamic_entity = await async_client.system_dynamic_entities.with_raw_response.create(
            body={},
        )

        assert system_dynamic_entity.is_closed is True
        assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await system_dynamic_entity.json() == {"foo": "bar"}
        assert isinstance(system_dynamic_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.system_dynamic_entities.with_streaming_response.create(
            body={},
        ) as system_dynamic_entity:
            assert not system_dynamic_entity.is_closed
            assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await system_dynamic_entity.json() == {"foo": "bar"}
            assert cast(Any, system_dynamic_entity.is_closed) is True
            assert isinstance(system_dynamic_entity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, system_dynamic_entity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/system-dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_dynamic_entity = await async_client.system_dynamic_entities.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        )
        assert system_dynamic_entity.is_closed
        assert await system_dynamic_entity.json() == {"foo": "bar"}
        assert cast(Any, system_dynamic_entity.is_closed) is True
        assert isinstance(system_dynamic_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/system-dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_dynamic_entity = await async_client.system_dynamic_entities.with_raw_response.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        )

        assert system_dynamic_entity.is_closed is True
        assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await system_dynamic_entity.json() == {"foo": "bar"}
        assert isinstance(system_dynamic_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/system-dynamic-entities/DYNAMIC_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.system_dynamic_entities.with_streaming_response.update(
            dynamic_entity_id="DYNAMIC_ENTITY_ID",
            body={},
        ) as system_dynamic_entity:
            assert not system_dynamic_entity.is_closed
            assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await system_dynamic_entity.json() == {"foo": "bar"}
            assert cast(Any, system_dynamic_entity.is_closed) is True
            assert isinstance(system_dynamic_entity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, system_dynamic_entity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dynamic_entity_id` but received ''"):
            await async_client.system_dynamic_entities.with_raw_response.update(
                dynamic_entity_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_dynamic_entity = await async_client.system_dynamic_entities.list()
        assert system_dynamic_entity.is_closed
        assert await system_dynamic_entity.json() == {"foo": "bar"}
        assert cast(Any, system_dynamic_entity.is_closed) is True
        assert isinstance(system_dynamic_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_dynamic_entity = await async_client.system_dynamic_entities.with_raw_response.list()

        assert system_dynamic_entity.is_closed is True
        assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await system_dynamic_entity.json() == {"foo": "bar"}
        assert isinstance(system_dynamic_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system-dynamic-entities").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.system_dynamic_entities.with_streaming_response.list() as system_dynamic_entity:
            assert not system_dynamic_entity.is_closed
            assert system_dynamic_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await system_dynamic_entity.json() == {"foo": "bar"}
            assert cast(Any, system_dynamic_entity.is_closed) is True
            assert isinstance(system_dynamic_entity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, system_dynamic_entity.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        system_dynamic_entity = await async_client.system_dynamic_entities.delete(
            "DYNAMIC_ENTITY_ID",
        )
        assert system_dynamic_entity is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.system_dynamic_entities.with_raw_response.delete(
            "DYNAMIC_ENTITY_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        system_dynamic_entity = await response.parse()
        assert system_dynamic_entity is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.system_dynamic_entities.with_streaming_response.delete(
            "DYNAMIC_ENTITY_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            system_dynamic_entity = await response.parse()
            assert system_dynamic_entity is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dynamic_entity_id` but received ''"):
            await async_client.system_dynamic_entities.with_raw_response.delete(
                "",
            )
