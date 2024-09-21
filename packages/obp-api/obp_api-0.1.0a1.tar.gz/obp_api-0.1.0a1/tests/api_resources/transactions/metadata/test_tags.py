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


class TestTags:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        tag = client.transactions.metadata.tags.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert tag.is_closed
        assert tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        tag = client.transactions.metadata.tags.with_raw_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert tag.json() == {"foo": "bar"}
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.tags.with_streaming_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, StreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.create(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        tag = client.transactions.metadata.tags.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert tag.is_closed
        assert tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        tag = client.transactions.metadata.tags.with_raw_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert tag.json() == {"foo": "bar"}
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.tags.with_streaming_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, StreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.list(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags/TAG_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        tag = client.transactions.metadata.tags.delete(
            tag_id="TAG_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )
        assert tag.is_closed
        assert tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags/TAG_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        tag = client.transactions.metadata.tags.with_raw_response.delete(
            tag_id="TAG_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert tag.json() == {"foo": "bar"}
        assert isinstance(tag, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags/TAG_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.tags.with_streaming_response.delete(
            tag_id="TAG_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        ) as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, StreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.delete(
                tag_id="TAG_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.delete(
                tag_id="TAG_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.delete(
                tag_id="TAG_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.delete(
                tag_id="TAG_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tag_id` but received ''"):
            client.transactions.metadata.tags.with_raw_response.delete(
                tag_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )


class TestAsyncTags:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        tag = await async_client.transactions.metadata.tags.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert tag.is_closed
        assert await tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        tag = await async_client.transactions.metadata.tags.with_raw_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await tag.json() == {"foo": "bar"}
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.tags.with_streaming_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.create(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        tag = await async_client.transactions.metadata.tags.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert tag.is_closed
        assert await tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        tag = await async_client.transactions.metadata.tags.with_raw_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await tag.json() == {"foo": "bar"}
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.tags.with_streaming_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.list(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags/TAG_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        tag = await async_client.transactions.metadata.tags.delete(
            tag_id="TAG_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )
        assert tag.is_closed
        assert await tag.json() == {"foo": "bar"}
        assert cast(Any, tag.is_closed) is True
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags/TAG_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        tag = await async_client.transactions.metadata.tags.with_raw_response.delete(
            tag_id="TAG_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )

        assert tag.is_closed is True
        assert tag.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await tag.json() == {"foo": "bar"}
        assert isinstance(tag, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/tags/TAG_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.tags.with_streaming_response.delete(
            tag_id="TAG_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        ) as tag:
            assert not tag.is_closed
            assert tag.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await tag.json() == {"foo": "bar"}
            assert cast(Any, tag.is_closed) is True
            assert isinstance(tag, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, tag.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.delete(
                tag_id="TAG_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.delete(
                tag_id="TAG_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.delete(
                tag_id="TAG_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.delete(
                tag_id="TAG_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tag_id` but received ''"):
            await async_client.transactions.metadata.tags.with_raw_response.delete(
                tag_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )
