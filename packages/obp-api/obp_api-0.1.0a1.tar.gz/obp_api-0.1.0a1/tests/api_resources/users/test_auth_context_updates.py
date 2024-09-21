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


class TestAuthContextUpdates:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/SCA_METHOD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        auth_context_update = client.users.auth_context_updates.create(
            sca_method="SCA_METHOD",
            bank_id="BANK_ID",
            body={},
        )
        assert auth_context_update.is_closed
        assert auth_context_update.json() == {"foo": "bar"}
        assert cast(Any, auth_context_update.is_closed) is True
        assert isinstance(auth_context_update, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/SCA_METHOD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        auth_context_update = client.users.auth_context_updates.with_raw_response.create(
            sca_method="SCA_METHOD",
            bank_id="BANK_ID",
            body={},
        )

        assert auth_context_update.is_closed is True
        assert auth_context_update.http_request.headers.get("X-Stainless-Lang") == "python"
        assert auth_context_update.json() == {"foo": "bar"}
        assert isinstance(auth_context_update, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/SCA_METHOD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.users.auth_context_updates.with_streaming_response.create(
            sca_method="SCA_METHOD",
            bank_id="BANK_ID",
            body={},
        ) as auth_context_update:
            assert not auth_context_update.is_closed
            assert auth_context_update.http_request.headers.get("X-Stainless-Lang") == "python"

            assert auth_context_update.json() == {"foo": "bar"}
            assert cast(Any, auth_context_update.is_closed) is True
            assert isinstance(auth_context_update, StreamedBinaryAPIResponse)

        assert cast(Any, auth_context_update.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.users.auth_context_updates.with_raw_response.create(
                sca_method="SCA_METHOD",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `sca_method` but received ''"):
            client.users.auth_context_updates.with_raw_response.create(
                sca_method="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_challenge(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/AUTH_CONTEXT_UPDATE_ID/challenge"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        auth_context_update = client.users.auth_context_updates.challenge(
            auth_context_update_id="AUTH_CONTEXT_UPDATE_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert auth_context_update.is_closed
        assert auth_context_update.json() == {"foo": "bar"}
        assert cast(Any, auth_context_update.is_closed) is True
        assert isinstance(auth_context_update, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_challenge(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/AUTH_CONTEXT_UPDATE_ID/challenge"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        auth_context_update = client.users.auth_context_updates.with_raw_response.challenge(
            auth_context_update_id="AUTH_CONTEXT_UPDATE_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert auth_context_update.is_closed is True
        assert auth_context_update.http_request.headers.get("X-Stainless-Lang") == "python"
        assert auth_context_update.json() == {"foo": "bar"}
        assert isinstance(auth_context_update, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_challenge(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/AUTH_CONTEXT_UPDATE_ID/challenge"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.users.auth_context_updates.with_streaming_response.challenge(
            auth_context_update_id="AUTH_CONTEXT_UPDATE_ID",
            bank_id="BANK_ID",
            body={},
        ) as auth_context_update:
            assert not auth_context_update.is_closed
            assert auth_context_update.http_request.headers.get("X-Stainless-Lang") == "python"

            assert auth_context_update.json() == {"foo": "bar"}
            assert cast(Any, auth_context_update.is_closed) is True
            assert isinstance(auth_context_update, StreamedBinaryAPIResponse)

        assert cast(Any, auth_context_update.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_challenge(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.users.auth_context_updates.with_raw_response.challenge(
                auth_context_update_id="AUTH_CONTEXT_UPDATE_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `auth_context_update_id` but received ''"
        ):
            client.users.auth_context_updates.with_raw_response.challenge(
                auth_context_update_id="",
                bank_id="BANK_ID",
                body={},
            )


class TestAsyncAuthContextUpdates:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/SCA_METHOD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        auth_context_update = await async_client.users.auth_context_updates.create(
            sca_method="SCA_METHOD",
            bank_id="BANK_ID",
            body={},
        )
        assert auth_context_update.is_closed
        assert await auth_context_update.json() == {"foo": "bar"}
        assert cast(Any, auth_context_update.is_closed) is True
        assert isinstance(auth_context_update, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/SCA_METHOD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        auth_context_update = await async_client.users.auth_context_updates.with_raw_response.create(
            sca_method="SCA_METHOD",
            bank_id="BANK_ID",
            body={},
        )

        assert auth_context_update.is_closed is True
        assert auth_context_update.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await auth_context_update.json() == {"foo": "bar"}
        assert isinstance(auth_context_update, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/SCA_METHOD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.users.auth_context_updates.with_streaming_response.create(
            sca_method="SCA_METHOD",
            bank_id="BANK_ID",
            body={},
        ) as auth_context_update:
            assert not auth_context_update.is_closed
            assert auth_context_update.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await auth_context_update.json() == {"foo": "bar"}
            assert cast(Any, auth_context_update.is_closed) is True
            assert isinstance(auth_context_update, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, auth_context_update.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.users.auth_context_updates.with_raw_response.create(
                sca_method="SCA_METHOD",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `sca_method` but received ''"):
            await async_client.users.auth_context_updates.with_raw_response.create(
                sca_method="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_challenge(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/AUTH_CONTEXT_UPDATE_ID/challenge"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        auth_context_update = await async_client.users.auth_context_updates.challenge(
            auth_context_update_id="AUTH_CONTEXT_UPDATE_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert auth_context_update.is_closed
        assert await auth_context_update.json() == {"foo": "bar"}
        assert cast(Any, auth_context_update.is_closed) is True
        assert isinstance(auth_context_update, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_challenge(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/AUTH_CONTEXT_UPDATE_ID/challenge"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        auth_context_update = await async_client.users.auth_context_updates.with_raw_response.challenge(
            auth_context_update_id="AUTH_CONTEXT_UPDATE_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert auth_context_update.is_closed is True
        assert auth_context_update.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await auth_context_update.json() == {"foo": "bar"}
        assert isinstance(auth_context_update, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_challenge(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/users/current/auth-context-updates/AUTH_CONTEXT_UPDATE_ID/challenge"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.users.auth_context_updates.with_streaming_response.challenge(
            auth_context_update_id="AUTH_CONTEXT_UPDATE_ID",
            bank_id="BANK_ID",
            body={},
        ) as auth_context_update:
            assert not auth_context_update.is_closed
            assert auth_context_update.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await auth_context_update.json() == {"foo": "bar"}
            assert cast(Any, auth_context_update.is_closed) is True
            assert isinstance(auth_context_update, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, auth_context_update.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_challenge(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.users.auth_context_updates.with_raw_response.challenge(
                auth_context_update_id="AUTH_CONTEXT_UPDATE_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `auth_context_update_id` but received ''"
        ):
            await async_client.users.auth_context_updates.with_raw_response.challenge(
                auth_context_update_id="",
                bank_id="BANK_ID",
                body={},
            )
