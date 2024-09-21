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


class TestMetadata:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        metadata = client.accounts.views.counterparties.metadata.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert metadata.is_closed
        assert metadata.json() == {"foo": "bar"}
        assert cast(Any, metadata.is_closed) is True
        assert isinstance(metadata, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        metadata = client.accounts.views.counterparties.metadata.with_raw_response.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert metadata.is_closed is True
        assert metadata.http_request.headers.get("X-Stainless-Lang") == "python"
        assert metadata.json() == {"foo": "bar"}
        assert isinstance(metadata, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.accounts.views.counterparties.metadata.with_streaming_response.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as metadata:
            assert not metadata.is_closed
            assert metadata.http_request.headers.get("X-Stainless-Lang") == "python"

            assert metadata.json() == {"foo": "bar"}
            assert cast(Any, metadata.is_closed) is True
            assert isinstance(metadata, StreamedBinaryAPIResponse)

        assert cast(Any, metadata.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.counterparties.metadata.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.counterparties.metadata.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.counterparties.metadata.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            client.accounts.views.counterparties.metadata.with_raw_response.retrieve(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/corporate_location"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        metadata = client.accounts.views.counterparties.metadata.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert metadata.is_closed
        assert metadata.json() == {"foo": "bar"}
        assert cast(Any, metadata.is_closed) is True
        assert isinstance(metadata, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/corporate_location"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        metadata = client.accounts.views.counterparties.metadata.with_raw_response.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert metadata.is_closed is True
        assert metadata.http_request.headers.get("X-Stainless-Lang") == "python"
        assert metadata.json() == {"foo": "bar"}
        assert isinstance(metadata, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/corporate_location"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.accounts.views.counterparties.metadata.with_streaming_response.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as metadata:
            assert not metadata.is_closed
            assert metadata.http_request.headers.get("X-Stainless-Lang") == "python"

            assert metadata.json() == {"foo": "bar"}
            assert cast(Any, metadata.is_closed) is True
            assert isinstance(metadata, StreamedBinaryAPIResponse)

        assert cast(Any, metadata.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.counterparties.metadata.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.counterparties.metadata.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.counterparties.metadata.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            client.accounts.views.counterparties.metadata.with_raw_response.update(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )


class TestAsyncMetadata:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        metadata = await async_client.accounts.views.counterparties.metadata.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert metadata.is_closed
        assert await metadata.json() == {"foo": "bar"}
        assert cast(Any, metadata.is_closed) is True
        assert isinstance(metadata, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        metadata = await async_client.accounts.views.counterparties.metadata.with_raw_response.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert metadata.is_closed is True
        assert metadata.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await metadata.json() == {"foo": "bar"}
        assert isinstance(metadata, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.accounts.views.counterparties.metadata.with_streaming_response.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as metadata:
            assert not metadata.is_closed
            assert metadata.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await metadata.json() == {"foo": "bar"}
            assert cast(Any, metadata.is_closed) is True
            assert isinstance(metadata, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, metadata.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.counterparties.metadata.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.counterparties.metadata.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.counterparties.metadata.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            await async_client.accounts.views.counterparties.metadata.with_raw_response.retrieve(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/corporate_location"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        metadata = await async_client.accounts.views.counterparties.metadata.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert metadata.is_closed
        assert await metadata.json() == {"foo": "bar"}
        assert cast(Any, metadata.is_closed) is True
        assert isinstance(metadata, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/corporate_location"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        metadata = await async_client.accounts.views.counterparties.metadata.with_raw_response.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert metadata.is_closed is True
        assert metadata.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await metadata.json() == {"foo": "bar"}
        assert isinstance(metadata, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/metadata/corporate_location"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.accounts.views.counterparties.metadata.with_streaming_response.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as metadata:
            assert not metadata.is_closed
            assert metadata.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await metadata.json() == {"foo": "bar"}
            assert cast(Any, metadata.is_closed) is True
            assert isinstance(metadata, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, metadata.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.counterparties.metadata.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.counterparties.metadata.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.counterparties.metadata.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            await async_client.accounts.views.counterparties.metadata.with_raw_response.update(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )
