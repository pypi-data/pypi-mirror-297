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


class TestPermissions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions/PROVIDER/PROVIDER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        permission = client.permissions.retrieve(
            provider_id="PROVIDER_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            provider="PROVIDER",
        )
        assert permission.is_closed
        assert permission.json() == {"foo": "bar"}
        assert cast(Any, permission.is_closed) is True
        assert isinstance(permission, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions/PROVIDER/PROVIDER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        permission = client.permissions.with_raw_response.retrieve(
            provider_id="PROVIDER_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            provider="PROVIDER",
        )

        assert permission.is_closed is True
        assert permission.http_request.headers.get("X-Stainless-Lang") == "python"
        assert permission.json() == {"foo": "bar"}
        assert isinstance(permission, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions/PROVIDER/PROVIDER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.permissions.with_streaming_response.retrieve(
            provider_id="PROVIDER_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            provider="PROVIDER",
        ) as permission:
            assert not permission.is_closed
            assert permission.http_request.headers.get("X-Stainless-Lang") == "python"

            assert permission.json() == {"foo": "bar"}
            assert cast(Any, permission.is_closed) is True
            assert isinstance(permission, StreamedBinaryAPIResponse)

        assert cast(Any, permission.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.permissions.with_raw_response.retrieve(
                provider_id="PROVIDER_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                provider="PROVIDER",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.permissions.with_raw_response.retrieve(
                provider_id="PROVIDER_ID",
                bank_id="BANK_ID",
                account_id="",
                provider="PROVIDER",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider` but received ''"):
            client.permissions.with_raw_response.retrieve(
                provider_id="PROVIDER_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                provider="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider_id` but received ''"):
            client.permissions.with_raw_response.retrieve(
                provider_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                provider="PROVIDER",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        permission = client.permissions.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        )
        assert permission.is_closed
        assert permission.json() == {"foo": "bar"}
        assert cast(Any, permission.is_closed) is True
        assert isinstance(permission, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        permission = client.permissions.with_raw_response.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        )

        assert permission.is_closed is True
        assert permission.http_request.headers.get("X-Stainless-Lang") == "python"
        assert permission.json() == {"foo": "bar"}
        assert isinstance(permission, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.permissions.with_streaming_response.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        ) as permission:
            assert not permission.is_closed
            assert permission.http_request.headers.get("X-Stainless-Lang") == "python"

            assert permission.json() == {"foo": "bar"}
            assert cast(Any, permission.is_closed) is True
            assert isinstance(permission, StreamedBinaryAPIResponse)

        assert cast(Any, permission.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.permissions.with_raw_response.list(
                account_id="ACCOUNT_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.permissions.with_raw_response.list(
                account_id="",
                bank_id="BANK_ID",
            )


class TestAsyncPermissions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions/PROVIDER/PROVIDER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        permission = await async_client.permissions.retrieve(
            provider_id="PROVIDER_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            provider="PROVIDER",
        )
        assert permission.is_closed
        assert await permission.json() == {"foo": "bar"}
        assert cast(Any, permission.is_closed) is True
        assert isinstance(permission, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions/PROVIDER/PROVIDER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        permission = await async_client.permissions.with_raw_response.retrieve(
            provider_id="PROVIDER_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            provider="PROVIDER",
        )

        assert permission.is_closed is True
        assert permission.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await permission.json() == {"foo": "bar"}
        assert isinstance(permission, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions/PROVIDER/PROVIDER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.permissions.with_streaming_response.retrieve(
            provider_id="PROVIDER_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            provider="PROVIDER",
        ) as permission:
            assert not permission.is_closed
            assert permission.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await permission.json() == {"foo": "bar"}
            assert cast(Any, permission.is_closed) is True
            assert isinstance(permission, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, permission.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.permissions.with_raw_response.retrieve(
                provider_id="PROVIDER_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                provider="PROVIDER",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.permissions.with_raw_response.retrieve(
                provider_id="PROVIDER_ID",
                bank_id="BANK_ID",
                account_id="",
                provider="PROVIDER",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider` but received ''"):
            await async_client.permissions.with_raw_response.retrieve(
                provider_id="PROVIDER_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                provider="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider_id` but received ''"):
            await async_client.permissions.with_raw_response.retrieve(
                provider_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                provider="PROVIDER",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        permission = await async_client.permissions.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        )
        assert permission.is_closed
        assert await permission.json() == {"foo": "bar"}
        assert cast(Any, permission.is_closed) is True
        assert isinstance(permission, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        permission = await async_client.permissions.with_raw_response.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        )

        assert permission.is_closed is True
        assert permission.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await permission.json() == {"foo": "bar"}
        assert isinstance(permission, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/permissions").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.permissions.with_streaming_response.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        ) as permission:
            assert not permission.is_closed
            assert permission.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await permission.json() == {"foo": "bar"}
            assert cast(Any, permission.is_closed) is True
            assert isinstance(permission, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, permission.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.permissions.with_raw_response.list(
                account_id="ACCOUNT_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.permissions.with_raw_response.list(
                account_id="",
                bank_id="BANK_ID",
            )
