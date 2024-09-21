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


class TestSocialMediaHandles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        social_media_handle = client.customers.social_media_handles.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert social_media_handle.is_closed
        assert social_media_handle.json() == {"foo": "bar"}
        assert cast(Any, social_media_handle.is_closed) is True
        assert isinstance(social_media_handle, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        social_media_handle = client.customers.social_media_handles.with_raw_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert social_media_handle.is_closed is True
        assert social_media_handle.http_request.headers.get("X-Stainless-Lang") == "python"
        assert social_media_handle.json() == {"foo": "bar"}
        assert isinstance(social_media_handle, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.social_media_handles.with_streaming_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as social_media_handle:
            assert not social_media_handle.is_closed
            assert social_media_handle.http_request.headers.get("X-Stainless-Lang") == "python"

            assert social_media_handle.json() == {"foo": "bar"}
            assert cast(Any, social_media_handle.is_closed) is True
            assert isinstance(social_media_handle, StreamedBinaryAPIResponse)

        assert cast(Any, social_media_handle.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.social_media_handles.with_raw_response.create(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.social_media_handles.with_raw_response.create(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        social_media_handle = client.customers.social_media_handles.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert social_media_handle.is_closed
        assert social_media_handle.json() == {"foo": "bar"}
        assert cast(Any, social_media_handle.is_closed) is True
        assert isinstance(social_media_handle, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        social_media_handle = client.customers.social_media_handles.with_raw_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert social_media_handle.is_closed is True
        assert social_media_handle.http_request.headers.get("X-Stainless-Lang") == "python"
        assert social_media_handle.json() == {"foo": "bar"}
        assert isinstance(social_media_handle, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.social_media_handles.with_streaming_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as social_media_handle:
            assert not social_media_handle.is_closed
            assert social_media_handle.http_request.headers.get("X-Stainless-Lang") == "python"

            assert social_media_handle.json() == {"foo": "bar"}
            assert cast(Any, social_media_handle.is_closed) is True
            assert isinstance(social_media_handle, StreamedBinaryAPIResponse)

        assert cast(Any, social_media_handle.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.social_media_handles.with_raw_response.list(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.social_media_handles.with_raw_response.list(
                customer_id="",
                bank_id="BANK_ID",
            )


class TestAsyncSocialMediaHandles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        social_media_handle = await async_client.customers.social_media_handles.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert social_media_handle.is_closed
        assert await social_media_handle.json() == {"foo": "bar"}
        assert cast(Any, social_media_handle.is_closed) is True
        assert isinstance(social_media_handle, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        social_media_handle = await async_client.customers.social_media_handles.with_raw_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert social_media_handle.is_closed is True
        assert social_media_handle.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await social_media_handle.json() == {"foo": "bar"}
        assert isinstance(social_media_handle, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.social_media_handles.with_streaming_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as social_media_handle:
            assert not social_media_handle.is_closed
            assert social_media_handle.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await social_media_handle.json() == {"foo": "bar"}
            assert cast(Any, social_media_handle.is_closed) is True
            assert isinstance(social_media_handle, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, social_media_handle.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.social_media_handles.with_raw_response.create(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.social_media_handles.with_raw_response.create(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        social_media_handle = await async_client.customers.social_media_handles.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert social_media_handle.is_closed
        assert await social_media_handle.json() == {"foo": "bar"}
        assert cast(Any, social_media_handle.is_closed) is True
        assert isinstance(social_media_handle, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        social_media_handle = await async_client.customers.social_media_handles.with_raw_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert social_media_handle.is_closed is True
        assert social_media_handle.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await social_media_handle.json() == {"foo": "bar"}
        assert isinstance(social_media_handle, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/social_media_handles").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.social_media_handles.with_streaming_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as social_media_handle:
            assert not social_media_handle.is_closed
            assert social_media_handle.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await social_media_handle.json() == {"foo": "bar"}
            assert cast(Any, social_media_handle.is_closed) is True
            assert isinstance(social_media_handle, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, social_media_handle.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.social_media_handles.with_raw_response.list(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.social_media_handles.with_raw_response.list(
                customer_id="",
                bank_id="BANK_ID",
            )
