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


class TestTransactionRequests:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests/TRANSACTION_REQUEST_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        transaction_request = client.banks.accounts.views.transaction_requests.retrieve(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert transaction_request.is_closed
        assert transaction_request.json() == {"foo": "bar"}
        assert cast(Any, transaction_request.is_closed) is True
        assert isinstance(transaction_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests/TRANSACTION_REQUEST_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        transaction_request = client.banks.accounts.views.transaction_requests.with_raw_response.retrieve(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert transaction_request.is_closed is True
        assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert transaction_request.json() == {"foo": "bar"}
        assert isinstance(transaction_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests/TRANSACTION_REQUEST_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.accounts.views.transaction_requests.with_streaming_response.retrieve(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as transaction_request:
            assert not transaction_request.is_closed
            assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert transaction_request.json() == {"foo": "bar"}
            assert cast(Any, transaction_request.is_closed) is True
            assert isinstance(transaction_request, StreamedBinaryAPIResponse)

        assert cast(Any, transaction_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.views.transaction_requests.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.views.transaction_requests.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.views.transaction_requests.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `transaction_request_id` but received ''"
        ):
            client.banks.accounts.views.transaction_requests.with_raw_response.retrieve(
                transaction_request_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        transaction_request = client.banks.accounts.views.transaction_requests.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert transaction_request.is_closed
        assert transaction_request.json() == {"foo": "bar"}
        assert cast(Any, transaction_request.is_closed) is True
        assert isinstance(transaction_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        transaction_request = client.banks.accounts.views.transaction_requests.with_raw_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert transaction_request.is_closed is True
        assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert transaction_request.json() == {"foo": "bar"}
        assert isinstance(transaction_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.accounts.views.transaction_requests.with_streaming_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as transaction_request:
            assert not transaction_request.is_closed
            assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert transaction_request.json() == {"foo": "bar"}
            assert cast(Any, transaction_request.is_closed) is True
            assert isinstance(transaction_request, StreamedBinaryAPIResponse)

        assert cast(Any, transaction_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.views.transaction_requests.with_raw_response.list(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.views.transaction_requests.with_raw_response.list(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.views.transaction_requests.with_raw_response.list(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )


class TestAsyncTransactionRequests:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests/TRANSACTION_REQUEST_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        transaction_request = await async_client.banks.accounts.views.transaction_requests.retrieve(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert transaction_request.is_closed
        assert await transaction_request.json() == {"foo": "bar"}
        assert cast(Any, transaction_request.is_closed) is True
        assert isinstance(transaction_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests/TRANSACTION_REQUEST_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        transaction_request = await async_client.banks.accounts.views.transaction_requests.with_raw_response.retrieve(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert transaction_request.is_closed is True
        assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await transaction_request.json() == {"foo": "bar"}
        assert isinstance(transaction_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests/TRANSACTION_REQUEST_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.accounts.views.transaction_requests.with_streaming_response.retrieve(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as transaction_request:
            assert not transaction_request.is_closed
            assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await transaction_request.json() == {"foo": "bar"}
            assert cast(Any, transaction_request.is_closed) is True
            assert isinstance(transaction_request, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, transaction_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.views.transaction_requests.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.views.transaction_requests.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.views.transaction_requests.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `transaction_request_id` but received ''"
        ):
            await async_client.banks.accounts.views.transaction_requests.with_raw_response.retrieve(
                transaction_request_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        transaction_request = await async_client.banks.accounts.views.transaction_requests.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert transaction_request.is_closed
        assert await transaction_request.json() == {"foo": "bar"}
        assert cast(Any, transaction_request.is_closed) is True
        assert isinstance(transaction_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        transaction_request = await async_client.banks.accounts.views.transaction_requests.with_raw_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert transaction_request.is_closed is True
        assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await transaction_request.json() == {"foo": "bar"}
        assert isinstance(transaction_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transaction-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.accounts.views.transaction_requests.with_streaming_response.list(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as transaction_request:
            assert not transaction_request.is_closed
            assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await transaction_request.json() == {"foo": "bar"}
            assert cast(Any, transaction_request.is_closed) is True
            assert isinstance(transaction_request, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, transaction_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.views.transaction_requests.with_raw_response.list(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.views.transaction_requests.with_raw_response.list(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.views.transaction_requests.with_raw_response.list(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )
