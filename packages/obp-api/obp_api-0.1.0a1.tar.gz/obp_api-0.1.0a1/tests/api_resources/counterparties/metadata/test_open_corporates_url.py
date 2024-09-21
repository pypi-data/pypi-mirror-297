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


class TestOpenCorporatesURL:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/open_corporates_url"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        open_corporates_url = client.counterparties.metadata.open_corporates_url.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert open_corporates_url.is_closed
        assert open_corporates_url.json() == {"foo": "bar"}
        assert cast(Any, open_corporates_url.is_closed) is True
        assert isinstance(open_corporates_url, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/open_corporates_url"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        open_corporates_url = client.counterparties.metadata.open_corporates_url.with_raw_response.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert open_corporates_url.is_closed is True
        assert open_corporates_url.http_request.headers.get("X-Stainless-Lang") == "python"
        assert open_corporates_url.json() == {"foo": "bar"}
        assert isinstance(open_corporates_url, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/open_corporates_url"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.counterparties.metadata.open_corporates_url.with_streaming_response.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as open_corporates_url:
            assert not open_corporates_url.is_closed
            assert open_corporates_url.http_request.headers.get("X-Stainless-Lang") == "python"

            assert open_corporates_url.json() == {"foo": "bar"}
            assert cast(Any, open_corporates_url.is_closed) is True
            assert isinstance(open_corporates_url, StreamedBinaryAPIResponse)

        assert cast(Any, open_corporates_url.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.counterparties.metadata.open_corporates_url.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.counterparties.metadata.open_corporates_url.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.counterparties.metadata.open_corporates_url.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            client.counterparties.metadata.open_corporates_url.with_raw_response.delete(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )


class TestAsyncOpenCorporatesURL:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/open_corporates_url"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        open_corporates_url = await async_client.counterparties.metadata.open_corporates_url.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert open_corporates_url.is_closed
        assert await open_corporates_url.json() == {"foo": "bar"}
        assert cast(Any, open_corporates_url.is_closed) is True
        assert isinstance(open_corporates_url, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/open_corporates_url"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        open_corporates_url = await async_client.counterparties.metadata.open_corporates_url.with_raw_response.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert open_corporates_url.is_closed is True
        assert open_corporates_url.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await open_corporates_url.json() == {"foo": "bar"}
        assert isinstance(open_corporates_url, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/open_corporates_url"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.counterparties.metadata.open_corporates_url.with_streaming_response.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as open_corporates_url:
            assert not open_corporates_url.is_closed
            assert open_corporates_url.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await open_corporates_url.json() == {"foo": "bar"}
            assert cast(Any, open_corporates_url.is_closed) is True
            assert isinstance(open_corporates_url, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, open_corporates_url.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.counterparties.metadata.open_corporates_url.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.counterparties.metadata.open_corporates_url.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.counterparties.metadata.open_corporates_url.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            await async_client.counterparties.metadata.open_corporates_url.with_raw_response.delete(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )
