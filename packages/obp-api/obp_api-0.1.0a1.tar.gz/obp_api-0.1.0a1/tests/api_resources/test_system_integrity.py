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


class TestSystemIntegrity:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_account_access_unique_index_1_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/account-access-unique-index-1-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_integrity = client.system_integrity.account_access_unique_index_1_check()
        assert system_integrity.is_closed
        assert system_integrity.json() == {"foo": "bar"}
        assert cast(Any, system_integrity.is_closed) is True
        assert isinstance(system_integrity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_account_access_unique_index_1_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/account-access-unique-index-1-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_integrity = client.system_integrity.with_raw_response.account_access_unique_index_1_check()

        assert system_integrity.is_closed is True
        assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert system_integrity.json() == {"foo": "bar"}
        assert isinstance(system_integrity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_account_access_unique_index_1_check(
        self, client: ObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/account-access-unique-index-1-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.system_integrity.with_streaming_response.account_access_unique_index_1_check() as system_integrity:
            assert not system_integrity.is_closed
            assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert system_integrity.json() == {"foo": "bar"}
            assert cast(Any, system_integrity.is_closed) is True
            assert isinstance(system_integrity, StreamedBinaryAPIResponse)

        assert cast(Any, system_integrity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_custom_view_names_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/custom-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_integrity = client.system_integrity.custom_view_names_check()
        assert system_integrity.is_closed
        assert system_integrity.json() == {"foo": "bar"}
        assert cast(Any, system_integrity.is_closed) is True
        assert isinstance(system_integrity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_custom_view_names_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/custom-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_integrity = client.system_integrity.with_raw_response.custom_view_names_check()

        assert system_integrity.is_closed is True
        assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert system_integrity.json() == {"foo": "bar"}
        assert isinstance(system_integrity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_custom_view_names_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/custom-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.system_integrity.with_streaming_response.custom_view_names_check() as system_integrity:
            assert not system_integrity.is_closed
            assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert system_integrity.json() == {"foo": "bar"}
            assert cast(Any, system_integrity.is_closed) is True
            assert isinstance(system_integrity, StreamedBinaryAPIResponse)

        assert cast(Any, system_integrity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_system_view_names_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/system-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_integrity = client.system_integrity.system_view_names_check()
        assert system_integrity.is_closed
        assert system_integrity.json() == {"foo": "bar"}
        assert cast(Any, system_integrity.is_closed) is True
        assert isinstance(system_integrity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_system_view_names_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/system-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_integrity = client.system_integrity.with_raw_response.system_view_names_check()

        assert system_integrity.is_closed is True
        assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert system_integrity.json() == {"foo": "bar"}
        assert isinstance(system_integrity, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_system_view_names_check(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/system-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.system_integrity.with_streaming_response.system_view_names_check() as system_integrity:
            assert not system_integrity.is_closed
            assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert system_integrity.json() == {"foo": "bar"}
            assert cast(Any, system_integrity.is_closed) is True
            assert isinstance(system_integrity, StreamedBinaryAPIResponse)

        assert cast(Any, system_integrity.is_closed) is True


class TestAsyncSystemIntegrity:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_account_access_unique_index_1_check(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/account-access-unique-index-1-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_integrity = await async_client.system_integrity.account_access_unique_index_1_check()
        assert system_integrity.is_closed
        assert await system_integrity.json() == {"foo": "bar"}
        assert cast(Any, system_integrity.is_closed) is True
        assert isinstance(system_integrity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_account_access_unique_index_1_check(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/account-access-unique-index-1-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_integrity = await async_client.system_integrity.with_raw_response.account_access_unique_index_1_check()

        assert system_integrity.is_closed is True
        assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await system_integrity.json() == {"foo": "bar"}
        assert isinstance(system_integrity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_account_access_unique_index_1_check(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/account-access-unique-index-1-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.system_integrity.with_streaming_response.account_access_unique_index_1_check() as system_integrity:
            assert not system_integrity.is_closed
            assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await system_integrity.json() == {"foo": "bar"}
            assert cast(Any, system_integrity.is_closed) is True
            assert isinstance(system_integrity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, system_integrity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_custom_view_names_check(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/custom-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_integrity = await async_client.system_integrity.custom_view_names_check()
        assert system_integrity.is_closed
        assert await system_integrity.json() == {"foo": "bar"}
        assert cast(Any, system_integrity.is_closed) is True
        assert isinstance(system_integrity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_custom_view_names_check(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/custom-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_integrity = await async_client.system_integrity.with_raw_response.custom_view_names_check()

        assert system_integrity.is_closed is True
        assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await system_integrity.json() == {"foo": "bar"}
        assert isinstance(system_integrity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_custom_view_names_check(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/custom-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.system_integrity.with_streaming_response.custom_view_names_check() as system_integrity:
            assert not system_integrity.is_closed
            assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await system_integrity.json() == {"foo": "bar"}
            assert cast(Any, system_integrity.is_closed) is True
            assert isinstance(system_integrity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, system_integrity.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_system_view_names_check(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/system-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        system_integrity = await async_client.system_integrity.system_view_names_check()
        assert system_integrity.is_closed
        assert await system_integrity.json() == {"foo": "bar"}
        assert cast(Any, system_integrity.is_closed) is True
        assert isinstance(system_integrity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_system_view_names_check(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/system-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        system_integrity = await async_client.system_integrity.with_raw_response.system_view_names_check()

        assert system_integrity.is_closed is True
        assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await system_integrity.json() == {"foo": "bar"}
        assert isinstance(system_integrity, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_system_view_names_check(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/obp/v5.1.0/management/system/integrity/system-view-names-check").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.system_integrity.with_streaming_response.system_view_names_check() as system_integrity:
            assert not system_integrity.is_closed
            assert system_integrity.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await system_integrity.json() == {"foo": "bar"}
            assert cast(Any, system_integrity.is_closed) is True
            assert isinstance(system_integrity, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, system_integrity.is_closed) is True
