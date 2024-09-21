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


class TestAccounts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_account_routing_query(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account = client.management.accounts.account_routing_query(
            body={},
        )
        assert account.is_closed
        assert account.json() == {"foo": "bar"}
        assert cast(Any, account.is_closed) is True
        assert isinstance(account, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_account_routing_query(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account = client.management.accounts.with_raw_response.account_routing_query(
            body={},
        )

        assert account.is_closed is True
        assert account.http_request.headers.get("X-Stainless-Lang") == "python"
        assert account.json() == {"foo": "bar"}
        assert isinstance(account, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_account_routing_query(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.management.accounts.with_streaming_response.account_routing_query(
            body={},
        ) as account:
            assert not account.is_closed
            assert account.http_request.headers.get("X-Stainless-Lang") == "python"

            assert account.json() == {"foo": "bar"}
            assert cast(Any, account.is_closed) is True
            assert isinstance(account, StreamedBinaryAPIResponse)

        assert cast(Any, account.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_account_routing_regex_query(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-regex-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account = client.management.accounts.account_routing_regex_query(
            body={},
        )
        assert account.is_closed
        assert account.json() == {"foo": "bar"}
        assert cast(Any, account.is_closed) is True
        assert isinstance(account, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_account_routing_regex_query(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-regex-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account = client.management.accounts.with_raw_response.account_routing_regex_query(
            body={},
        )

        assert account.is_closed is True
        assert account.http_request.headers.get("X-Stainless-Lang") == "python"
        assert account.json() == {"foo": "bar"}
        assert isinstance(account, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_account_routing_regex_query(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-regex-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.management.accounts.with_streaming_response.account_routing_regex_query(
            body={},
        ) as account:
            assert not account.is_closed
            assert account.http_request.headers.get("X-Stainless-Lang") == "python"

            assert account.json() == {"foo": "bar"}
            assert cast(Any, account.is_closed) is True
            assert isinstance(account, StreamedBinaryAPIResponse)

        assert cast(Any, account.is_closed) is True


class TestAsyncAccounts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_account_routing_query(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account = await async_client.management.accounts.account_routing_query(
            body={},
        )
        assert account.is_closed
        assert await account.json() == {"foo": "bar"}
        assert cast(Any, account.is_closed) is True
        assert isinstance(account, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_account_routing_query(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account = await async_client.management.accounts.with_raw_response.account_routing_query(
            body={},
        )

        assert account.is_closed is True
        assert account.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await account.json() == {"foo": "bar"}
        assert isinstance(account, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_account_routing_query(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.management.accounts.with_streaming_response.account_routing_query(
            body={},
        ) as account:
            assert not account.is_closed
            assert account.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await account.json() == {"foo": "bar"}
            assert cast(Any, account.is_closed) is True
            assert isinstance(account, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, account.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_account_routing_regex_query(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-regex-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        account = await async_client.management.accounts.account_routing_regex_query(
            body={},
        )
        assert account.is_closed
        assert await account.json() == {"foo": "bar"}
        assert cast(Any, account.is_closed) is True
        assert isinstance(account, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_account_routing_regex_query(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-regex-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        account = await async_client.management.accounts.with_raw_response.account_routing_regex_query(
            body={},
        )

        assert account.is_closed is True
        assert account.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await account.json() == {"foo": "bar"}
        assert isinstance(account, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_account_routing_regex_query(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/obp/v5.1.0/management/accounts/account-routing-regex-query").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.management.accounts.with_streaming_response.account_routing_regex_query(
            body={},
        ) as account:
            assert not account.is_closed
            assert account.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await account.json() == {"foo": "bar"}
            assert cast(Any, account.is_closed) is True
            assert isinstance(account, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, account.is_closed) is True
