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


class TestJsonSchemaValidations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        json_schema_validation = client.json_schema_validations.create(
            body={},
        )
        assert json_schema_validation.is_closed
        assert json_schema_validation.json() == {"foo": "bar"}
        assert cast(Any, json_schema_validation.is_closed) is True
        assert isinstance(json_schema_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        json_schema_validation = client.json_schema_validations.with_raw_response.create(
            body={},
        )

        assert json_schema_validation.is_closed is True
        assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert json_schema_validation.json() == {"foo": "bar"}
        assert isinstance(json_schema_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.json_schema_validations.with_streaming_response.create(
            body={},
        ) as json_schema_validation:
            assert not json_schema_validation.is_closed
            assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert json_schema_validation.json() == {"foo": "bar"}
            assert cast(Any, json_schema_validation.is_closed) is True
            assert isinstance(json_schema_validation, StreamedBinaryAPIResponse)

        assert cast(Any, json_schema_validation.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        json_schema_validation = client.json_schema_validations.retrieve()
        assert json_schema_validation.is_closed
        assert json_schema_validation.json() == {"foo": "bar"}
        assert cast(Any, json_schema_validation.is_closed) is True
        assert isinstance(json_schema_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        json_schema_validation = client.json_schema_validations.with_raw_response.retrieve()

        assert json_schema_validation.is_closed is True
        assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert json_schema_validation.json() == {"foo": "bar"}
        assert isinstance(json_schema_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.json_schema_validations.with_streaming_response.retrieve() as json_schema_validation:
            assert not json_schema_validation.is_closed
            assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert json_schema_validation.json() == {"foo": "bar"}
            assert cast(Any, json_schema_validation.is_closed) is True
            assert isinstance(json_schema_validation, StreamedBinaryAPIResponse)

        assert cast(Any, json_schema_validation.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        json_schema_validation = client.json_schema_validations.update(
            body={},
        )
        assert json_schema_validation.is_closed
        assert json_schema_validation.json() == {"foo": "bar"}
        assert cast(Any, json_schema_validation.is_closed) is True
        assert isinstance(json_schema_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        json_schema_validation = client.json_schema_validations.with_raw_response.update(
            body={},
        )

        assert json_schema_validation.is_closed is True
        assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert json_schema_validation.json() == {"foo": "bar"}
        assert isinstance(json_schema_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.json_schema_validations.with_streaming_response.update(
            body={},
        ) as json_schema_validation:
            assert not json_schema_validation.is_closed
            assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert json_schema_validation.json() == {"foo": "bar"}
            assert cast(Any, json_schema_validation.is_closed) is True
            assert isinstance(json_schema_validation, StreamedBinaryAPIResponse)

        assert cast(Any, json_schema_validation.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        json_schema_validation = client.json_schema_validations.list()
        assert json_schema_validation.is_closed
        assert json_schema_validation.json() == {"foo": "bar"}
        assert cast(Any, json_schema_validation.is_closed) is True
        assert isinstance(json_schema_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        json_schema_validation = client.json_schema_validations.with_raw_response.list()

        assert json_schema_validation.is_closed is True
        assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert json_schema_validation.json() == {"foo": "bar"}
        assert isinstance(json_schema_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.json_schema_validations.with_streaming_response.list() as json_schema_validation:
            assert not json_schema_validation.is_closed
            assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert json_schema_validation.json() == {"foo": "bar"}
            assert cast(Any, json_schema_validation.is_closed) is True
            assert isinstance(json_schema_validation, StreamedBinaryAPIResponse)

        assert cast(Any, json_schema_validation.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        json_schema_validation = client.json_schema_validations.delete()
        assert json_schema_validation.is_closed
        assert json_schema_validation.json() == {"foo": "bar"}
        assert cast(Any, json_schema_validation.is_closed) is True
        assert isinstance(json_schema_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        json_schema_validation = client.json_schema_validations.with_raw_response.delete()

        assert json_schema_validation.is_closed is True
        assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert json_schema_validation.json() == {"foo": "bar"}
        assert isinstance(json_schema_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.json_schema_validations.with_streaming_response.delete() as json_schema_validation:
            assert not json_schema_validation.is_closed
            assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert json_schema_validation.json() == {"foo": "bar"}
            assert cast(Any, json_schema_validation.is_closed) is True
            assert isinstance(json_schema_validation, StreamedBinaryAPIResponse)

        assert cast(Any, json_schema_validation.is_closed) is True


class TestAsyncJsonSchemaValidations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        json_schema_validation = await async_client.json_schema_validations.create(
            body={},
        )
        assert json_schema_validation.is_closed
        assert await json_schema_validation.json() == {"foo": "bar"}
        assert cast(Any, json_schema_validation.is_closed) is True
        assert isinstance(json_schema_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        json_schema_validation = await async_client.json_schema_validations.with_raw_response.create(
            body={},
        )

        assert json_schema_validation.is_closed is True
        assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await json_schema_validation.json() == {"foo": "bar"}
        assert isinstance(json_schema_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.json_schema_validations.with_streaming_response.create(
            body={},
        ) as json_schema_validation:
            assert not json_schema_validation.is_closed
            assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await json_schema_validation.json() == {"foo": "bar"}
            assert cast(Any, json_schema_validation.is_closed) is True
            assert isinstance(json_schema_validation, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, json_schema_validation.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        json_schema_validation = await async_client.json_schema_validations.retrieve()
        assert json_schema_validation.is_closed
        assert await json_schema_validation.json() == {"foo": "bar"}
        assert cast(Any, json_schema_validation.is_closed) is True
        assert isinstance(json_schema_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        json_schema_validation = await async_client.json_schema_validations.with_raw_response.retrieve()

        assert json_schema_validation.is_closed is True
        assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await json_schema_validation.json() == {"foo": "bar"}
        assert isinstance(json_schema_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.json_schema_validations.with_streaming_response.retrieve() as json_schema_validation:
            assert not json_schema_validation.is_closed
            assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await json_schema_validation.json() == {"foo": "bar"}
            assert cast(Any, json_schema_validation.is_closed) is True
            assert isinstance(json_schema_validation, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, json_schema_validation.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        json_schema_validation = await async_client.json_schema_validations.update(
            body={},
        )
        assert json_schema_validation.is_closed
        assert await json_schema_validation.json() == {"foo": "bar"}
        assert cast(Any, json_schema_validation.is_closed) is True
        assert isinstance(json_schema_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        json_schema_validation = await async_client.json_schema_validations.with_raw_response.update(
            body={},
        )

        assert json_schema_validation.is_closed is True
        assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await json_schema_validation.json() == {"foo": "bar"}
        assert isinstance(json_schema_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.json_schema_validations.with_streaming_response.update(
            body={},
        ) as json_schema_validation:
            assert not json_schema_validation.is_closed
            assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await json_schema_validation.json() == {"foo": "bar"}
            assert cast(Any, json_schema_validation.is_closed) is True
            assert isinstance(json_schema_validation, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, json_schema_validation.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        json_schema_validation = await async_client.json_schema_validations.list()
        assert json_schema_validation.is_closed
        assert await json_schema_validation.json() == {"foo": "bar"}
        assert cast(Any, json_schema_validation.is_closed) is True
        assert isinstance(json_schema_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        json_schema_validation = await async_client.json_schema_validations.with_raw_response.list()

        assert json_schema_validation.is_closed is True
        assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await json_schema_validation.json() == {"foo": "bar"}
        assert isinstance(json_schema_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/json-schema-validations").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.json_schema_validations.with_streaming_response.list() as json_schema_validation:
            assert not json_schema_validation.is_closed
            assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await json_schema_validation.json() == {"foo": "bar"}
            assert cast(Any, json_schema_validation.is_closed) is True
            assert isinstance(json_schema_validation, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, json_schema_validation.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        json_schema_validation = await async_client.json_schema_validations.delete()
        assert json_schema_validation.is_closed
        assert await json_schema_validation.json() == {"foo": "bar"}
        assert cast(Any, json_schema_validation.is_closed) is True
        assert isinstance(json_schema_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        json_schema_validation = await async_client.json_schema_validations.with_raw_response.delete()

        assert json_schema_validation.is_closed is True
        assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await json_schema_validation.json() == {"foo": "bar"}
        assert isinstance(json_schema_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/json-schema-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.json_schema_validations.with_streaming_response.delete() as json_schema_validation:
            assert not json_schema_validation.is_closed
            assert json_schema_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await json_schema_validation.json() == {"foo": "bar"}
            assert cast(Any, json_schema_validation.is_closed) is True
            assert isinstance(json_schema_validation, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, json_schema_validation.is_closed) is True
