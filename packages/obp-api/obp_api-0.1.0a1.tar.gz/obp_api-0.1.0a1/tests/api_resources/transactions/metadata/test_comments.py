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


class TestComments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        comment = client.transactions.metadata.comments.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert comment.is_closed
        assert comment.json() == {"foo": "bar"}
        assert cast(Any, comment.is_closed) is True
        assert isinstance(comment, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        comment = client.transactions.metadata.comments.with_raw_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert comment.is_closed is True
        assert comment.http_request.headers.get("X-Stainless-Lang") == "python"
        assert comment.json() == {"foo": "bar"}
        assert isinstance(comment, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.comments.with_streaming_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as comment:
            assert not comment.is_closed
            assert comment.http_request.headers.get("X-Stainless-Lang") == "python"

            assert comment.json() == {"foo": "bar"}
            assert cast(Any, comment.is_closed) is True
            assert isinstance(comment, StreamedBinaryAPIResponse)

        assert cast(Any, comment.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.create(
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
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        comment = client.transactions.metadata.comments.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert comment.is_closed
        assert comment.json() == {"foo": "bar"}
        assert cast(Any, comment.is_closed) is True
        assert isinstance(comment, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        comment = client.transactions.metadata.comments.with_raw_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert comment.is_closed is True
        assert comment.http_request.headers.get("X-Stainless-Lang") == "python"
        assert comment.json() == {"foo": "bar"}
        assert isinstance(comment, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.comments.with_streaming_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as comment:
            assert not comment.is_closed
            assert comment.http_request.headers.get("X-Stainless-Lang") == "python"

            assert comment.json() == {"foo": "bar"}
            assert cast(Any, comment.is_closed) is True
            assert isinstance(comment, StreamedBinaryAPIResponse)

        assert cast(Any, comment.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.list(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments/COMMENT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        comment = client.transactions.metadata.comments.delete(
            comment_id="COMMENT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )
        assert comment.is_closed
        assert comment.json() == {"foo": "bar"}
        assert cast(Any, comment.is_closed) is True
        assert isinstance(comment, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments/COMMENT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        comment = client.transactions.metadata.comments.with_raw_response.delete(
            comment_id="COMMENT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )

        assert comment.is_closed is True
        assert comment.http_request.headers.get("X-Stainless-Lang") == "python"
        assert comment.json() == {"foo": "bar"}
        assert isinstance(comment, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments/COMMENT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.comments.with_streaming_response.delete(
            comment_id="COMMENT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        ) as comment:
            assert not comment.is_closed
            assert comment.http_request.headers.get("X-Stainless-Lang") == "python"

            assert comment.json() == {"foo": "bar"}
            assert cast(Any, comment.is_closed) is True
            assert isinstance(comment, StreamedBinaryAPIResponse)

        assert cast(Any, comment.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.delete(
                comment_id="COMMENT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.delete(
                comment_id="COMMENT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.delete(
                comment_id="COMMENT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.delete(
                comment_id="COMMENT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `comment_id` but received ''"):
            client.transactions.metadata.comments.with_raw_response.delete(
                comment_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )


class TestAsyncComments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        comment = await async_client.transactions.metadata.comments.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert comment.is_closed
        assert await comment.json() == {"foo": "bar"}
        assert cast(Any, comment.is_closed) is True
        assert isinstance(comment, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        comment = await async_client.transactions.metadata.comments.with_raw_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert comment.is_closed is True
        assert comment.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await comment.json() == {"foo": "bar"}
        assert isinstance(comment, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.comments.with_streaming_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as comment:
            assert not comment.is_closed
            assert comment.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await comment.json() == {"foo": "bar"}
            assert cast(Any, comment.is_closed) is True
            assert isinstance(comment, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, comment.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.create(
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
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        comment = await async_client.transactions.metadata.comments.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert comment.is_closed
        assert await comment.json() == {"foo": "bar"}
        assert cast(Any, comment.is_closed) is True
        assert isinstance(comment, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        comment = await async_client.transactions.metadata.comments.with_raw_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert comment.is_closed is True
        assert comment.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await comment.json() == {"foo": "bar"}
        assert isinstance(comment, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.comments.with_streaming_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as comment:
            assert not comment.is_closed
            assert comment.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await comment.json() == {"foo": "bar"}
            assert cast(Any, comment.is_closed) is True
            assert isinstance(comment, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, comment.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.list(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments/COMMENT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        comment = await async_client.transactions.metadata.comments.delete(
            comment_id="COMMENT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )
        assert comment.is_closed
        assert await comment.json() == {"foo": "bar"}
        assert cast(Any, comment.is_closed) is True
        assert isinstance(comment, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments/COMMENT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        comment = await async_client.transactions.metadata.comments.with_raw_response.delete(
            comment_id="COMMENT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )

        assert comment.is_closed is True
        assert comment.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await comment.json() == {"foo": "bar"}
        assert isinstance(comment, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/comments/COMMENT_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.comments.with_streaming_response.delete(
            comment_id="COMMENT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        ) as comment:
            assert not comment.is_closed
            assert comment.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await comment.json() == {"foo": "bar"}
            assert cast(Any, comment.is_closed) is True
            assert isinstance(comment, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, comment.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.delete(
                comment_id="COMMENT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.delete(
                comment_id="COMMENT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.delete(
                comment_id="COMMENT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.delete(
                comment_id="COMMENT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `comment_id` but received ''"):
            await async_client.transactions.metadata.comments.with_raw_response.delete(
                comment_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )
