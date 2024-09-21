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


class TestScopes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        scope = client.consumers.scopes.create(
            consumer_id="CONSUMER_ID",
            body={},
        )
        assert scope.is_closed
        assert scope.json() == {"foo": "bar"}
        assert cast(Any, scope.is_closed) is True
        assert isinstance(scope, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        scope = client.consumers.scopes.with_raw_response.create(
            consumer_id="CONSUMER_ID",
            body={},
        )

        assert scope.is_closed is True
        assert scope.http_request.headers.get("X-Stainless-Lang") == "python"
        assert scope.json() == {"foo": "bar"}
        assert isinstance(scope, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consumers.scopes.with_streaming_response.create(
            consumer_id="CONSUMER_ID",
            body={},
        ) as scope:
            assert not scope.is_closed
            assert scope.http_request.headers.get("X-Stainless-Lang") == "python"

            assert scope.json() == {"foo": "bar"}
            assert cast(Any, scope.is_closed) is True
            assert isinstance(scope, StreamedBinaryAPIResponse)

        assert cast(Any, scope.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consumer_id` but received ''"):
            client.consumers.scopes.with_raw_response.create(
                consumer_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        scope = client.consumers.scopes.list(
            "CONSUMER_ID",
        )
        assert scope.is_closed
        assert scope.json() == {"foo": "bar"}
        assert cast(Any, scope.is_closed) is True
        assert isinstance(scope, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        scope = client.consumers.scopes.with_raw_response.list(
            "CONSUMER_ID",
        )

        assert scope.is_closed is True
        assert scope.http_request.headers.get("X-Stainless-Lang") == "python"
        assert scope.json() == {"foo": "bar"}
        assert isinstance(scope, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consumers.scopes.with_streaming_response.list(
            "CONSUMER_ID",
        ) as scope:
            assert not scope.is_closed
            assert scope.http_request.headers.get("X-Stainless-Lang") == "python"

            assert scope.json() == {"foo": "bar"}
            assert cast(Any, scope.is_closed) is True
            assert isinstance(scope, StreamedBinaryAPIResponse)

        assert cast(Any, scope.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consumer_id` but received ''"):
            client.consumers.scopes.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        scope = client.consumers.scopes.delete(
            scope_id="SCOPE_ID",
            consumer_id="CONSUMER_ID",
        )
        assert scope is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.consumers.scopes.with_raw_response.delete(
            scope_id="SCOPE_ID",
            consumer_id="CONSUMER_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = response.parse()
        assert scope is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.consumers.scopes.with_streaming_response.delete(
            scope_id="SCOPE_ID",
            consumer_id="CONSUMER_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = response.parse()
            assert scope is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consumer_id` but received ''"):
            client.consumers.scopes.with_raw_response.delete(
                scope_id="SCOPE_ID",
                consumer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.consumers.scopes.with_raw_response.delete(
                scope_id="",
                consumer_id="CONSUMER_ID",
            )


class TestAsyncScopes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        scope = await async_client.consumers.scopes.create(
            consumer_id="CONSUMER_ID",
            body={},
        )
        assert scope.is_closed
        assert await scope.json() == {"foo": "bar"}
        assert cast(Any, scope.is_closed) is True
        assert isinstance(scope, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        scope = await async_client.consumers.scopes.with_raw_response.create(
            consumer_id="CONSUMER_ID",
            body={},
        )

        assert scope.is_closed is True
        assert scope.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await scope.json() == {"foo": "bar"}
        assert isinstance(scope, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consumers.scopes.with_streaming_response.create(
            consumer_id="CONSUMER_ID",
            body={},
        ) as scope:
            assert not scope.is_closed
            assert scope.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await scope.json() == {"foo": "bar"}
            assert cast(Any, scope.is_closed) is True
            assert isinstance(scope, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, scope.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consumer_id` but received ''"):
            await async_client.consumers.scopes.with_raw_response.create(
                consumer_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        scope = await async_client.consumers.scopes.list(
            "CONSUMER_ID",
        )
        assert scope.is_closed
        assert await scope.json() == {"foo": "bar"}
        assert cast(Any, scope.is_closed) is True
        assert isinstance(scope, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        scope = await async_client.consumers.scopes.with_raw_response.list(
            "CONSUMER_ID",
        )

        assert scope.is_closed is True
        assert scope.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await scope.json() == {"foo": "bar"}
        assert isinstance(scope, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumers/CONSUMER_ID/scopes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consumers.scopes.with_streaming_response.list(
            "CONSUMER_ID",
        ) as scope:
            assert not scope.is_closed
            assert scope.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await scope.json() == {"foo": "bar"}
            assert cast(Any, scope.is_closed) is True
            assert isinstance(scope, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, scope.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consumer_id` but received ''"):
            await async_client.consumers.scopes.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        scope = await async_client.consumers.scopes.delete(
            scope_id="SCOPE_ID",
            consumer_id="CONSUMER_ID",
        )
        assert scope is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.consumers.scopes.with_raw_response.delete(
            scope_id="SCOPE_ID",
            consumer_id="CONSUMER_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = await response.parse()
        assert scope is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.consumers.scopes.with_streaming_response.delete(
            scope_id="SCOPE_ID",
            consumer_id="CONSUMER_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = await response.parse()
            assert scope is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consumer_id` but received ''"):
            await async_client.consumers.scopes.with_raw_response.delete(
                scope_id="SCOPE_ID",
                consumer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.consumers.scopes.with_raw_response.delete(
                scope_id="",
                consumer_id="CONSUMER_ID",
            )
