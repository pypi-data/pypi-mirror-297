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


class TestNarrative:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        narrative = client.transactions.metadata.narrative.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert narrative.is_closed
        assert narrative.json() == {"foo": "bar"}
        assert cast(Any, narrative.is_closed) is True
        assert isinstance(narrative, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        narrative = client.transactions.metadata.narrative.with_raw_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert narrative.is_closed is True
        assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"
        assert narrative.json() == {"foo": "bar"}
        assert isinstance(narrative, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.narrative.with_streaming_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as narrative:
            assert not narrative.is_closed
            assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"

            assert narrative.json() == {"foo": "bar"}
            assert cast(Any, narrative.is_closed) is True
            assert isinstance(narrative, StreamedBinaryAPIResponse)

        assert cast(Any, narrative.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.create(
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
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        narrative = client.transactions.metadata.narrative.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert narrative.is_closed
        assert narrative.json() == {"foo": "bar"}
        assert cast(Any, narrative.is_closed) is True
        assert isinstance(narrative, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        narrative = client.transactions.metadata.narrative.with_raw_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert narrative.is_closed is True
        assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"
        assert narrative.json() == {"foo": "bar"}
        assert isinstance(narrative, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.narrative.with_streaming_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as narrative:
            assert not narrative.is_closed
            assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"

            assert narrative.json() == {"foo": "bar"}
            assert cast(Any, narrative.is_closed) is True
            assert isinstance(narrative, StreamedBinaryAPIResponse)

        assert cast(Any, narrative.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.retrieve(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        narrative = client.transactions.metadata.narrative.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert narrative.is_closed
        assert narrative.json() == {"foo": "bar"}
        assert cast(Any, narrative.is_closed) is True
        assert isinstance(narrative, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        narrative = client.transactions.metadata.narrative.with_raw_response.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert narrative.is_closed is True
        assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"
        assert narrative.json() == {"foo": "bar"}
        assert isinstance(narrative, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.narrative.with_streaming_response.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as narrative:
            assert not narrative.is_closed
            assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"

            assert narrative.json() == {"foo": "bar"}
            assert cast(Any, narrative.is_closed) is True
            assert isinstance(narrative, StreamedBinaryAPIResponse)

        assert cast(Any, narrative.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.update(
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
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        narrative = client.transactions.metadata.narrative.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert narrative.is_closed
        assert narrative.json() == {"foo": "bar"}
        assert cast(Any, narrative.is_closed) is True
        assert isinstance(narrative, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        narrative = client.transactions.metadata.narrative.with_raw_response.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert narrative.is_closed is True
        assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"
        assert narrative.json() == {"foo": "bar"}
        assert isinstance(narrative, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transactions.metadata.narrative.with_streaming_response.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as narrative:
            assert not narrative.is_closed
            assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"

            assert narrative.json() == {"foo": "bar"}
            assert cast(Any, narrative.is_closed) is True
            assert isinstance(narrative, StreamedBinaryAPIResponse)

        assert cast(Any, narrative.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.metadata.narrative.with_raw_response.delete(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )


class TestAsyncNarrative:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        narrative = await async_client.transactions.metadata.narrative.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert narrative.is_closed
        assert await narrative.json() == {"foo": "bar"}
        assert cast(Any, narrative.is_closed) is True
        assert isinstance(narrative, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        narrative = await async_client.transactions.metadata.narrative.with_raw_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert narrative.is_closed is True
        assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await narrative.json() == {"foo": "bar"}
        assert isinstance(narrative, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.narrative.with_streaming_response.create(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as narrative:
            assert not narrative.is_closed
            assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await narrative.json() == {"foo": "bar"}
            assert cast(Any, narrative.is_closed) is True
            assert isinstance(narrative, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, narrative.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.create(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.create(
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
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        narrative = await async_client.transactions.metadata.narrative.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert narrative.is_closed
        assert await narrative.json() == {"foo": "bar"}
        assert cast(Any, narrative.is_closed) is True
        assert isinstance(narrative, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        narrative = await async_client.transactions.metadata.narrative.with_raw_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert narrative.is_closed is True
        assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await narrative.json() == {"foo": "bar"}
        assert isinstance(narrative, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.narrative.with_streaming_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as narrative:
            assert not narrative.is_closed
            assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await narrative.json() == {"foo": "bar"}
            assert cast(Any, narrative.is_closed) is True
            assert isinstance(narrative, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, narrative.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.retrieve(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        narrative = await async_client.transactions.metadata.narrative.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert narrative.is_closed
        assert await narrative.json() == {"foo": "bar"}
        assert cast(Any, narrative.is_closed) is True
        assert isinstance(narrative, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        narrative = await async_client.transactions.metadata.narrative.with_raw_response.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert narrative.is_closed is True
        assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await narrative.json() == {"foo": "bar"}
        assert isinstance(narrative, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.narrative.with_streaming_response.update(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as narrative:
            assert not narrative.is_closed
            assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await narrative.json() == {"foo": "bar"}
            assert cast(Any, narrative.is_closed) is True
            assert isinstance(narrative, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, narrative.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.update(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.update(
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
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        narrative = await async_client.transactions.metadata.narrative.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert narrative.is_closed
        assert await narrative.json() == {"foo": "bar"}
        assert cast(Any, narrative.is_closed) is True
        assert isinstance(narrative, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        narrative = await async_client.transactions.metadata.narrative.with_raw_response.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert narrative.is_closed is True
        assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await narrative.json() == {"foo": "bar"}
        assert isinstance(narrative, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/transactions/TRANSACTION_ID/metadata/narrative"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transactions.metadata.narrative.with_streaming_response.delete(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as narrative:
            assert not narrative.is_closed
            assert narrative.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await narrative.json() == {"foo": "bar"}
            assert cast(Any, narrative.is_closed) is True
            assert isinstance(narrative, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, narrative.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.delete(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.metadata.narrative.with_raw_response.delete(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )
