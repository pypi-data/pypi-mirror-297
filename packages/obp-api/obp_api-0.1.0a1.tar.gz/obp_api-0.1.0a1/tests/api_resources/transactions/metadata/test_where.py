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


class TestWhere:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        where = client.transactions.metadata.where.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert where.is_closed
        assert where.json() == {"foo": "bar"}
        assert cast(Any, where.is_closed) is True
        assert isinstance(where, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        where = client.transactions.metadata.where.with_raw_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert where.is_closed is True
        assert where.http_request.headers.get("X-Stainless-Lang") == "python"
        assert where.json() == {"foo": "bar"}
        assert isinstance(where, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.where.with_streaming_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as where:
            assert not where.is_closed
            assert where.http_request.headers.get("X-Stainless-Lang") == "python"

            assert where.json() == {"foo": "bar"}
            assert cast(Any, where.is_closed) is True
            assert isinstance(where, StreamedBinaryAPIResponse)

        assert cast(Any, where.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.create(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        where = client.transactions.metadata.where.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert where.is_closed
        assert where.json() == {"foo": "bar"}
        assert cast(Any, where.is_closed) is True
        assert isinstance(where, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        where = client.transactions.metadata.where.with_raw_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert where.is_closed is True
        assert where.http_request.headers.get("X-Stainless-Lang") == "python"
        assert where.json() == {"foo": "bar"}
        assert isinstance(where, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.where.with_streaming_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as where:
            assert not where.is_closed
            assert where.http_request.headers.get("X-Stainless-Lang") == "python"

            assert where.json() == {"foo": "bar"}
            assert cast(Any, where.is_closed) is True
            assert isinstance(where, StreamedBinaryAPIResponse)

        assert cast(Any, where.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.retrieve(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        where = client.transactions.metadata.where.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert where.is_closed
        assert where.json() == {"foo": "bar"}
        assert cast(Any, where.is_closed) is True
        assert isinstance(where, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        where = client.transactions.metadata.where.with_raw_response.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert where.is_closed is True
        assert where.http_request.headers.get("X-Stainless-Lang") == "python"
        assert where.json() == {"foo": "bar"}
        assert isinstance(where, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.where.with_streaming_response.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as where:
            assert not where.is_closed
            assert where.http_request.headers.get("X-Stainless-Lang") == "python"

            assert where.json() == {"foo": "bar"}
            assert cast(Any, where.is_closed) is True
            assert isinstance(where, StreamedBinaryAPIResponse)

        assert cast(Any, where.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.update(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        where = client.transactions.metadata.where.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert where.is_closed
        assert where.json() == {"foo": "bar"}
        assert cast(Any, where.is_closed) is True
        assert isinstance(where, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        where = client.transactions.metadata.where.with_raw_response.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert where.is_closed is True
        assert where.http_request.headers.get("X-Stainless-Lang") == "python"
        assert where.json() == {"foo": "bar"}
        assert isinstance(where, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.where.with_streaming_response.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as where:
            assert not where.is_closed
            assert where.http_request.headers.get("X-Stainless-Lang") == "python"

            assert where.json() == {"foo": "bar"}
            assert cast(Any, where.is_closed) is True
            assert isinstance(where, StreamedBinaryAPIResponse)

        assert cast(Any, where.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.where.with_raw_response.delete(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )


class TestAsyncWhere:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        where = await async_client.transactions.metadata.where.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert where.is_closed
        assert await where.json() == {"foo": "bar"}
        assert cast(Any, where.is_closed) is True
        assert isinstance(where, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        where = await async_client.transactions.metadata.where.with_raw_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert where.is_closed is True
        assert where.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await where.json() == {"foo": "bar"}
        assert isinstance(where, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.where.with_streaming_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as where:
            assert not where.is_closed
            assert where.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await where.json() == {"foo": "bar"}
            assert cast(Any, where.is_closed) is True
            assert isinstance(where, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, where.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.create(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        where = await async_client.transactions.metadata.where.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert where.is_closed
        assert await where.json() == {"foo": "bar"}
        assert cast(Any, where.is_closed) is True
        assert isinstance(where, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        where = await async_client.transactions.metadata.where.with_raw_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert where.is_closed is True
        assert where.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await where.json() == {"foo": "bar"}
        assert isinstance(where, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.where.with_streaming_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as where:
            assert not where.is_closed
            assert where.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await where.json() == {"foo": "bar"}
            assert cast(Any, where.is_closed) is True
            assert isinstance(where, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, where.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.retrieve(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        where = await async_client.transactions.metadata.where.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert where.is_closed
        assert await where.json() == {"foo": "bar"}
        assert cast(Any, where.is_closed) is True
        assert isinstance(where, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        where = await async_client.transactions.metadata.where.with_raw_response.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert where.is_closed is True
        assert where.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await where.json() == {"foo": "bar"}
        assert isinstance(where, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.where.with_streaming_response.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as where:
            assert not where.is_closed
            assert where.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await where.json() == {"foo": "bar"}
            assert cast(Any, where.is_closed) is True
            assert isinstance(where, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, where.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.update(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        where = await async_client.transactions.metadata.where.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert where.is_closed
        assert await where.json() == {"foo": "bar"}
        assert cast(Any, where.is_closed) is True
        assert isinstance(where, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        where = await async_client.transactions.metadata.where.with_raw_response.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert where.is_closed is True
        assert where.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await where.json() == {"foo": "bar"}
        assert isinstance(where, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/where"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.where.with_streaming_response.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as where:
            assert not where.is_closed
            assert where.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await where.json() == {"foo": "bar"}
            assert cast(Any, where.is_closed) is True
            assert isinstance(where, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, where.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.where.with_raw_response.delete(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )
