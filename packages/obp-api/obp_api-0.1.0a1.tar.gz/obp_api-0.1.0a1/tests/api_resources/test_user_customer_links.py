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


class TestUserCustomerLinks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/user_customer_links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        user_customer_link = client.user_customer_links.create(
            bank_id="BANK_ID",
            body={},
        )
        assert user_customer_link.is_closed
        assert user_customer_link.json() == {"foo": "bar"}
        assert cast(Any, user_customer_link.is_closed) is True
        assert isinstance(user_customer_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/user_customer_links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        user_customer_link = client.user_customer_links.with_raw_response.create(
            bank_id="BANK_ID",
            body={},
        )

        assert user_customer_link.is_closed is True
        assert user_customer_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert user_customer_link.json() == {"foo": "bar"}
        assert isinstance(user_customer_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/user_customer_links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.user_customer_links.with_streaming_response.create(
            bank_id="BANK_ID",
            body={},
        ) as user_customer_link:
            assert not user_customer_link.is_closed
            assert user_customer_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert user_customer_link.json() == {"foo": "bar"}
            assert cast(Any, user_customer_link.is_closed) is True
            assert isinstance(user_customer_link, StreamedBinaryAPIResponse)

        assert cast(Any, user_customer_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.user_customer_links.with_raw_response.create(
                bank_id="",
                body={},
            )

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        user_customer_link = client.user_customer_links.delete(
            "BANK_ID",
        )
        assert user_customer_link is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.user_customer_links.with_raw_response.delete(
            "BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_customer_link = response.parse()
        assert user_customer_link is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.user_customer_links.with_streaming_response.delete(
            "BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_customer_link = response.parse()
            assert user_customer_link is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.user_customer_links.with_raw_response.delete(
                "",
            )


class TestAsyncUserCustomerLinks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/user_customer_links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        user_customer_link = await async_client.user_customer_links.create(
            bank_id="BANK_ID",
            body={},
        )
        assert user_customer_link.is_closed
        assert await user_customer_link.json() == {"foo": "bar"}
        assert cast(Any, user_customer_link.is_closed) is True
        assert isinstance(user_customer_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/user_customer_links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        user_customer_link = await async_client.user_customer_links.with_raw_response.create(
            bank_id="BANK_ID",
            body={},
        )

        assert user_customer_link.is_closed is True
        assert user_customer_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await user_customer_link.json() == {"foo": "bar"}
        assert isinstance(user_customer_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/user_customer_links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.user_customer_links.with_streaming_response.create(
            bank_id="BANK_ID",
            body={},
        ) as user_customer_link:
            assert not user_customer_link.is_closed
            assert user_customer_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await user_customer_link.json() == {"foo": "bar"}
            assert cast(Any, user_customer_link.is_closed) is True
            assert isinstance(user_customer_link, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, user_customer_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.user_customer_links.with_raw_response.create(
                bank_id="",
                body={},
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        user_customer_link = await async_client.user_customer_links.delete(
            "BANK_ID",
        )
        assert user_customer_link is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.user_customer_links.with_raw_response.delete(
            "BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_customer_link = await response.parse()
        assert user_customer_link is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.user_customer_links.with_streaming_response.delete(
            "BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_customer_link = await response.parse()
            assert user_customer_link is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.user_customer_links.with_raw_response.delete(
                "",
            )
