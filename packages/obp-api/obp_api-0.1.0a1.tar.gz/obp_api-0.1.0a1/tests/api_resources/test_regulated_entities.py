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


class TestRegulatedEntities:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        regulated_entity = client.regulated_entities.create(
            body={},
        )
        assert regulated_entity.is_closed
        assert regulated_entity.json() == {"foo": "bar"}
        assert cast(Any, regulated_entity.is_closed) is True
        assert isinstance(regulated_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        regulated_entity = client.regulated_entities.with_raw_response.create(
            body={},
        )

        assert regulated_entity.is_closed is True
        assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert regulated_entity.json() == {"foo": "bar"}
        assert isinstance(regulated_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.regulated_entities.with_streaming_response.create(
            body={},
        ) as regulated_entity:
            assert not regulated_entity.is_closed
            assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert regulated_entity.json() == {"foo": "bar"}
            assert cast(Any, regulated_entity.is_closed) is True
            assert isinstance(regulated_entity, StreamedBinaryAPIResponse)

        assert cast(Any, regulated_entity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities/REGULATED_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        regulated_entity = client.regulated_entities.retrieve()
        assert regulated_entity.is_closed
        assert regulated_entity.json() == {"foo": "bar"}
        assert cast(Any, regulated_entity.is_closed) is True
        assert isinstance(regulated_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities/REGULATED_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        regulated_entity = client.regulated_entities.with_raw_response.retrieve()

        assert regulated_entity.is_closed is True
        assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert regulated_entity.json() == {"foo": "bar"}
        assert isinstance(regulated_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities/REGULATED_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.regulated_entities.with_streaming_response.retrieve() as regulated_entity:
            assert not regulated_entity.is_closed
            assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert regulated_entity.json() == {"foo": "bar"}
            assert cast(Any, regulated_entity.is_closed) is True
            assert isinstance(regulated_entity, StreamedBinaryAPIResponse)

        assert cast(Any, regulated_entity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        regulated_entity = client.regulated_entities.list()
        assert regulated_entity.is_closed
        assert regulated_entity.json() == {"foo": "bar"}
        assert cast(Any, regulated_entity.is_closed) is True
        assert isinstance(regulated_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        regulated_entity = client.regulated_entities.with_raw_response.list()

        assert regulated_entity.is_closed is True
        assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert regulated_entity.json() == {"foo": "bar"}
        assert isinstance(regulated_entity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.regulated_entities.with_streaming_response.list() as regulated_entity:
            assert not regulated_entity.is_closed
            assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert regulated_entity.json() == {"foo": "bar"}
            assert cast(Any, regulated_entity.is_closed) is True
            assert isinstance(regulated_entity, StreamedBinaryAPIResponse)

        assert cast(Any, regulated_entity.is_closed) is True

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        regulated_entity = client.regulated_entities.delete()
        assert regulated_entity is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.regulated_entities.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        regulated_entity = response.parse()
        assert regulated_entity is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.regulated_entities.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            regulated_entity = response.parse()
            assert regulated_entity is None

        assert cast(Any, response.is_closed) is True


class TestAsyncRegulatedEntities:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        regulated_entity = await async_client.regulated_entities.create(
            body={},
        )
        assert regulated_entity.is_closed
        assert await regulated_entity.json() == {"foo": "bar"}
        assert cast(Any, regulated_entity.is_closed) is True
        assert isinstance(regulated_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        regulated_entity = await async_client.regulated_entities.with_raw_response.create(
            body={},
        )

        assert regulated_entity.is_closed is True
        assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await regulated_entity.json() == {"foo": "bar"}
        assert isinstance(regulated_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.regulated_entities.with_streaming_response.create(
            body={},
        ) as regulated_entity:
            assert not regulated_entity.is_closed
            assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await regulated_entity.json() == {"foo": "bar"}
            assert cast(Any, regulated_entity.is_closed) is True
            assert isinstance(regulated_entity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, regulated_entity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities/REGULATED_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        regulated_entity = await async_client.regulated_entities.retrieve()
        assert regulated_entity.is_closed
        assert await regulated_entity.json() == {"foo": "bar"}
        assert cast(Any, regulated_entity.is_closed) is True
        assert isinstance(regulated_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities/REGULATED_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        regulated_entity = await async_client.regulated_entities.with_raw_response.retrieve()

        assert regulated_entity.is_closed is True
        assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await regulated_entity.json() == {"foo": "bar"}
        assert isinstance(regulated_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities/REGULATED_ENTITY_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.regulated_entities.with_streaming_response.retrieve() as regulated_entity:
            assert not regulated_entity.is_closed
            assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await regulated_entity.json() == {"foo": "bar"}
            assert cast(Any, regulated_entity.is_closed) is True
            assert isinstance(regulated_entity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, regulated_entity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        regulated_entity = await async_client.regulated_entities.list()
        assert regulated_entity.is_closed
        assert await regulated_entity.json() == {"foo": "bar"}
        assert cast(Any, regulated_entity.is_closed) is True
        assert isinstance(regulated_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        regulated_entity = await async_client.regulated_entities.with_raw_response.list()

        assert regulated_entity.is_closed is True
        assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await regulated_entity.json() == {"foo": "bar"}
        assert isinstance(regulated_entity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/regulated-entities").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.regulated_entities.with_streaming_response.list() as regulated_entity:
            assert not regulated_entity.is_closed
            assert regulated_entity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await regulated_entity.json() == {"foo": "bar"}
            assert cast(Any, regulated_entity.is_closed) is True
            assert isinstance(regulated_entity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, regulated_entity.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        regulated_entity = await async_client.regulated_entities.delete()
        assert regulated_entity is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.regulated_entities.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        regulated_entity = await response.parse()
        assert regulated_entity is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.regulated_entities.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            regulated_entity = await response.parse()
            assert regulated_entity is None

        assert cast(Any, response.is_closed) is True
