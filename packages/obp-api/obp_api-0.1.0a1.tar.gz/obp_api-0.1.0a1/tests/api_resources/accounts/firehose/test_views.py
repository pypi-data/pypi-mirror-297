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


class TestViews:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/firehose/accounts/views/VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        view = client.accounts.firehose.views.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
        )
        assert view.is_closed
        assert view.json() == {"foo": "bar"}
        assert cast(Any, view.is_closed) is True
        assert isinstance(view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/firehose/accounts/views/VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        view = client.accounts.firehose.views.with_raw_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
        )

        assert view.is_closed is True
        assert view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert view.json() == {"foo": "bar"}
        assert isinstance(view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/firehose/accounts/views/VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.accounts.firehose.views.with_streaming_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
        ) as view:
            assert not view.is_closed
            assert view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert view.json() == {"foo": "bar"}
            assert cast(Any, view.is_closed) is True
            assert isinstance(view, StreamedBinaryAPIResponse)

        assert cast(Any, view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.firehose.views.with_raw_response.list(
                view_id="VIEW_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.firehose.views.with_raw_response.list(
                view_id="",
                bank_id="BANK_ID",
            )


class TestAsyncViews:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/firehose/accounts/views/VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        view = await async_client.accounts.firehose.views.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
        )
        assert view.is_closed
        assert await view.json() == {"foo": "bar"}
        assert cast(Any, view.is_closed) is True
        assert isinstance(view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/firehose/accounts/views/VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        view = await async_client.accounts.firehose.views.with_raw_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
        )

        assert view.is_closed is True
        assert view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await view.json() == {"foo": "bar"}
        assert isinstance(view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/firehose/accounts/views/VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.accounts.firehose.views.with_streaming_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
        ) as view:
            assert not view.is_closed
            assert view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await view.json() == {"foo": "bar"}
            assert cast(Any, view.is_closed) is True
            assert isinstance(view, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.firehose.views.with_raw_response.list(
                view_id="VIEW_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.firehose.views.with_raw_response.list(
                view_id="",
                bank_id="BANK_ID",
            )
