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


class TestAuthenticationTypeValidations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        authentication_type_validation = client.authentication_type_validations.create(
            body={},
        )
        assert authentication_type_validation.is_closed
        assert authentication_type_validation.json() == {"foo": "bar"}
        assert cast(Any, authentication_type_validation.is_closed) is True
        assert isinstance(authentication_type_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        authentication_type_validation = client.authentication_type_validations.with_raw_response.create(
            body={},
        )

        assert authentication_type_validation.is_closed is True
        assert authentication_type_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert authentication_type_validation.json() == {"foo": "bar"}
        assert isinstance(authentication_type_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.authentication_type_validations.with_streaming_response.create(
            body={},
        ) as authentication_type_validation:
            assert not authentication_type_validation.is_closed
            assert authentication_type_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert authentication_type_validation.json() == {"foo": "bar"}
            assert cast(Any, authentication_type_validation.is_closed) is True
            assert isinstance(authentication_type_validation, StreamedBinaryAPIResponse)

        assert cast(Any, authentication_type_validation.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        authentication_type_validation = client.authentication_type_validations.delete()
        assert authentication_type_validation.is_closed
        assert authentication_type_validation.json() == {"foo": "bar"}
        assert cast(Any, authentication_type_validation.is_closed) is True
        assert isinstance(authentication_type_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        authentication_type_validation = client.authentication_type_validations.with_raw_response.delete()

        assert authentication_type_validation.is_closed is True
        assert authentication_type_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert authentication_type_validation.json() == {"foo": "bar"}
        assert isinstance(authentication_type_validation, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.authentication_type_validations.with_streaming_response.delete() as authentication_type_validation:
            assert not authentication_type_validation.is_closed
            assert authentication_type_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert authentication_type_validation.json() == {"foo": "bar"}
            assert cast(Any, authentication_type_validation.is_closed) is True
            assert isinstance(authentication_type_validation, StreamedBinaryAPIResponse)

        assert cast(Any, authentication_type_validation.is_closed) is True


class TestAsyncAuthenticationTypeValidations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        authentication_type_validation = await async_client.authentication_type_validations.create(
            body={},
        )
        assert authentication_type_validation.is_closed
        assert await authentication_type_validation.json() == {"foo": "bar"}
        assert cast(Any, authentication_type_validation.is_closed) is True
        assert isinstance(authentication_type_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        authentication_type_validation = await async_client.authentication_type_validations.with_raw_response.create(
            body={},
        )

        assert authentication_type_validation.is_closed is True
        assert authentication_type_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await authentication_type_validation.json() == {"foo": "bar"}
        assert isinstance(authentication_type_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.authentication_type_validations.with_streaming_response.create(
            body={},
        ) as authentication_type_validation:
            assert not authentication_type_validation.is_closed
            assert authentication_type_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await authentication_type_validation.json() == {"foo": "bar"}
            assert cast(Any, authentication_type_validation.is_closed) is True
            assert isinstance(authentication_type_validation, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, authentication_type_validation.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        authentication_type_validation = await async_client.authentication_type_validations.delete()
        assert authentication_type_validation.is_closed
        assert await authentication_type_validation.json() == {"foo": "bar"}
        assert cast(Any, authentication_type_validation.is_closed) is True
        assert isinstance(authentication_type_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        authentication_type_validation = await async_client.authentication_type_validations.with_raw_response.delete()

        assert authentication_type_validation.is_closed is True
        assert authentication_type_validation.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await authentication_type_validation.json() == {"foo": "bar"}
        assert isinstance(authentication_type_validation, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/management/authentication-type-validations/OPERATION_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.authentication_type_validations.with_streaming_response.delete() as authentication_type_validation:
            assert not authentication_type_validation.is_closed
            assert authentication_type_validation.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await authentication_type_validation.json() == {"foo": "bar"}
            assert cast(Any, authentication_type_validation.is_closed) is True
            assert isinstance(authentication_type_validation, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, authentication_type_validation.is_closed) is True
