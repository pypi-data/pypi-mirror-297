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


class TestUsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        user = client.users.create(
            body={},
        )
        assert user.is_closed
        assert user.json() == {"foo": "bar"}
        assert cast(Any, user.is_closed) is True
        assert isinstance(user, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        user = client.users.with_raw_response.create(
            body={},
        )

        assert user.is_closed is True
        assert user.http_request.headers.get("X-Stainless-Lang") == "python"
        assert user.json() == {"foo": "bar"}
        assert isinstance(user, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.users.with_streaming_response.create(
            body={},
        ) as user:
            assert not user.is_closed
            assert user.http_request.headers.get("X-Stainless-Lang") == "python"

            assert user.json() == {"foo": "bar"}
            assert cast(Any, user.is_closed) is True
            assert isinstance(user, StreamedBinaryAPIResponse)

        assert cast(Any, user.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        user = client.users.list()
        assert user.is_closed
        assert user.json() == {"foo": "bar"}
        assert cast(Any, user.is_closed) is True
        assert isinstance(user, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        user = client.users.with_raw_response.list()

        assert user.is_closed is True
        assert user.http_request.headers.get("X-Stainless-Lang") == "python"
        assert user.json() == {"foo": "bar"}
        assert isinstance(user, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.users.with_streaming_response.list() as user:
            assert not user.is_closed
            assert user.http_request.headers.get("X-Stainless-Lang") == "python"

            assert user.json() == {"foo": "bar"}
            assert cast(Any, user.is_closed) is True
            assert isinstance(user, StreamedBinaryAPIResponse)

        assert cast(Any, user.is_closed) is True

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        user = client.users.delete(
            "USER_ID",
        )
        assert user is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.users.with_raw_response.delete(
            "USER_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert user is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.users.with_streaming_response.delete(
            "USER_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert user is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.with_raw_response.delete(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_reset_password_url(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/user/reset-password-url").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        user = client.users.reset_password_url(
            body={},
        )
        assert user.is_closed
        assert user.json() == {"foo": "bar"}
        assert cast(Any, user.is_closed) is True
        assert isinstance(user, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_reset_password_url(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/user/reset-password-url").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        user = client.users.with_raw_response.reset_password_url(
            body={},
        )

        assert user.is_closed is True
        assert user.http_request.headers.get("X-Stainless-Lang") == "python"
        assert user.json() == {"foo": "bar"}
        assert isinstance(user, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_reset_password_url(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/user/reset-password-url").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.users.with_streaming_response.reset_password_url(
            body={},
        ) as user:
            assert not user.is_closed
            assert user.http_request.headers.get("X-Stainless-Lang") == "python"

            assert user.json() == {"foo": "bar"}
            assert cast(Any, user.is_closed) is True
            assert isinstance(user, StreamedBinaryAPIResponse)

        assert cast(Any, user.is_closed) is True


class TestAsyncUsers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        user = await async_client.users.create(
            body={},
        )
        assert user.is_closed
        assert await user.json() == {"foo": "bar"}
        assert cast(Any, user.is_closed) is True
        assert isinstance(user, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        user = await async_client.users.with_raw_response.create(
            body={},
        )

        assert user.is_closed is True
        assert user.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await user.json() == {"foo": "bar"}
        assert isinstance(user, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.users.with_streaming_response.create(
            body={},
        ) as user:
            assert not user.is_closed
            assert user.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await user.json() == {"foo": "bar"}
            assert cast(Any, user.is_closed) is True
            assert isinstance(user, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, user.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        user = await async_client.users.list()
        assert user.is_closed
        assert await user.json() == {"foo": "bar"}
        assert cast(Any, user.is_closed) is True
        assert isinstance(user, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        user = await async_client.users.with_raw_response.list()

        assert user.is_closed is True
        assert user.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await user.json() == {"foo": "bar"}
        assert isinstance(user, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/users").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.users.with_streaming_response.list() as user:
            assert not user.is_closed
            assert user.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await user.json() == {"foo": "bar"}
            assert cast(Any, user.is_closed) is True
            assert isinstance(user, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, user.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        user = await async_client.users.delete(
            "USER_ID",
        )
        assert user is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.users.with_raw_response.delete(
            "USER_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert user is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.users.with_streaming_response.delete(
            "USER_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert user is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.with_raw_response.delete(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_reset_password_url(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/user/reset-password-url").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        user = await async_client.users.reset_password_url(
            body={},
        )
        assert user.is_closed
        assert await user.json() == {"foo": "bar"}
        assert cast(Any, user.is_closed) is True
        assert isinstance(user, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_reset_password_url(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/user/reset-password-url").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        user = await async_client.users.with_raw_response.reset_password_url(
            body={},
        )

        assert user.is_closed is True
        assert user.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await user.json() == {"foo": "bar"}
        assert isinstance(user, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_reset_password_url(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/obp/v5.1.0/management/user/reset-password-url").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.users.with_streaming_response.reset_password_url(
            body={},
        ) as user:
            assert not user.is_closed
            assert user.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await user.json() == {"foo": "bar"}
            assert cast(Any, user.is_closed) is True
            assert isinstance(user, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, user.is_closed) is True
