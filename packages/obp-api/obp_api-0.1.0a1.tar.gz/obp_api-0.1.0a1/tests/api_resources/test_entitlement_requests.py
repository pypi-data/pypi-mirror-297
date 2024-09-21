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


class TestEntitlementRequests:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/entitlement-requests").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        entitlement_request = client.entitlement_requests.create(
            body={},
        )
        assert entitlement_request.is_closed
        assert entitlement_request.json() == {"foo": "bar"}
        assert cast(Any, entitlement_request.is_closed) is True
        assert isinstance(entitlement_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/entitlement-requests").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        entitlement_request = client.entitlement_requests.with_raw_response.create(
            body={},
        )

        assert entitlement_request.is_closed is True
        assert entitlement_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert entitlement_request.json() == {"foo": "bar"}
        assert isinstance(entitlement_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/entitlement-requests").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.entitlement_requests.with_streaming_response.create(
            body={},
        ) as entitlement_request:
            assert not entitlement_request.is_closed
            assert entitlement_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert entitlement_request.json() == {"foo": "bar"}
            assert cast(Any, entitlement_request.is_closed) is True
            assert isinstance(entitlement_request, StreamedBinaryAPIResponse)

        assert cast(Any, entitlement_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/entitlement-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        entitlement_request = client.entitlement_requests.list()
        assert entitlement_request.is_closed
        assert entitlement_request.json() == {"foo": "bar"}
        assert cast(Any, entitlement_request.is_closed) is True
        assert isinstance(entitlement_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/entitlement-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        entitlement_request = client.entitlement_requests.with_raw_response.list()

        assert entitlement_request.is_closed is True
        assert entitlement_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert entitlement_request.json() == {"foo": "bar"}
        assert isinstance(entitlement_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/entitlement-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.entitlement_requests.with_streaming_response.list() as entitlement_request:
            assert not entitlement_request.is_closed
            assert entitlement_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert entitlement_request.json() == {"foo": "bar"}
            assert cast(Any, entitlement_request.is_closed) is True
            assert isinstance(entitlement_request, StreamedBinaryAPIResponse)

        assert cast(Any, entitlement_request.is_closed) is True

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        entitlement_request = client.entitlement_requests.delete(
            "ENTITLEMENT_REQUEST_ID",
        )
        assert entitlement_request is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.entitlement_requests.with_raw_response.delete(
            "ENTITLEMENT_REQUEST_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement_request = response.parse()
        assert entitlement_request is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.entitlement_requests.with_streaming_response.delete(
            "ENTITLEMENT_REQUEST_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement_request = response.parse()
            assert entitlement_request is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_request_id` but received ''"
        ):
            client.entitlement_requests.with_raw_response.delete(
                "",
            )


class TestAsyncEntitlementRequests:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/entitlement-requests").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        entitlement_request = await async_client.entitlement_requests.create(
            body={},
        )
        assert entitlement_request.is_closed
        assert await entitlement_request.json() == {"foo": "bar"}
        assert cast(Any, entitlement_request.is_closed) is True
        assert isinstance(entitlement_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/entitlement-requests").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        entitlement_request = await async_client.entitlement_requests.with_raw_response.create(
            body={},
        )

        assert entitlement_request.is_closed is True
        assert entitlement_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await entitlement_request.json() == {"foo": "bar"}
        assert isinstance(entitlement_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/entitlement-requests").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.entitlement_requests.with_streaming_response.create(
            body={},
        ) as entitlement_request:
            assert not entitlement_request.is_closed
            assert entitlement_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await entitlement_request.json() == {"foo": "bar"}
            assert cast(Any, entitlement_request.is_closed) is True
            assert isinstance(entitlement_request, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, entitlement_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/entitlement-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        entitlement_request = await async_client.entitlement_requests.list()
        assert entitlement_request.is_closed
        assert await entitlement_request.json() == {"foo": "bar"}
        assert cast(Any, entitlement_request.is_closed) is True
        assert isinstance(entitlement_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/entitlement-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        entitlement_request = await async_client.entitlement_requests.with_raw_response.list()

        assert entitlement_request.is_closed is True
        assert entitlement_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await entitlement_request.json() == {"foo": "bar"}
        assert isinstance(entitlement_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/my/entitlement-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.entitlement_requests.with_streaming_response.list() as entitlement_request:
            assert not entitlement_request.is_closed
            assert entitlement_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await entitlement_request.json() == {"foo": "bar"}
            assert cast(Any, entitlement_request.is_closed) is True
            assert isinstance(entitlement_request, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, entitlement_request.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        entitlement_request = await async_client.entitlement_requests.delete(
            "ENTITLEMENT_REQUEST_ID",
        )
        assert entitlement_request is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.entitlement_requests.with_raw_response.delete(
            "ENTITLEMENT_REQUEST_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement_request = await response.parse()
        assert entitlement_request is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.entitlement_requests.with_streaming_response.delete(
            "ENTITLEMENT_REQUEST_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement_request = await response.parse()
            assert entitlement_request is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_request_id` but received ''"
        ):
            await async_client.entitlement_requests.with_raw_response.delete(
                "",
            )
