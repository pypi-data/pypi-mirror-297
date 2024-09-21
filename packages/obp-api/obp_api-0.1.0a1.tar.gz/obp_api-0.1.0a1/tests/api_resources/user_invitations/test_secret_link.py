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


class TestSecretLink:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user-invitations/SECRET_LINK").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        secret_link = client.user_invitations.secret_link.retrieve(
            "BANK_ID",
        )
        assert secret_link.is_closed
        assert secret_link.json() == {"foo": "bar"}
        assert cast(Any, secret_link.is_closed) is True
        assert isinstance(secret_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user-invitations/SECRET_LINK").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        secret_link = client.user_invitations.secret_link.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert secret_link.is_closed is True
        assert secret_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert secret_link.json() == {"foo": "bar"}
        assert isinstance(secret_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user-invitations/SECRET_LINK").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.user_invitations.secret_link.with_streaming_response.retrieve(
            "BANK_ID",
        ) as secret_link:
            assert not secret_link.is_closed
            assert secret_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert secret_link.json() == {"foo": "bar"}
            assert cast(Any, secret_link.is_closed) is True
            assert isinstance(secret_link, StreamedBinaryAPIResponse)

        assert cast(Any, secret_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.user_invitations.secret_link.with_raw_response.retrieve(
                "",
            )


class TestAsyncSecretLink:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user-invitations/SECRET_LINK").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        secret_link = await async_client.user_invitations.secret_link.retrieve(
            "BANK_ID",
        )
        assert secret_link.is_closed
        assert await secret_link.json() == {"foo": "bar"}
        assert cast(Any, secret_link.is_closed) is True
        assert isinstance(secret_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user-invitations/SECRET_LINK").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        secret_link = await async_client.user_invitations.secret_link.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert secret_link.is_closed is True
        assert secret_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await secret_link.json() == {"foo": "bar"}
        assert isinstance(secret_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/user-invitations/SECRET_LINK").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.user_invitations.secret_link.with_streaming_response.retrieve(
            "BANK_ID",
        ) as secret_link:
            assert not secret_link.is_closed
            assert secret_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await secret_link.json() == {"foo": "bar"}
            assert cast(Any, secret_link.is_closed) is True
            assert isinstance(secret_link, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, secret_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.user_invitations.secret_link.with_raw_response.retrieve(
                "",
            )
