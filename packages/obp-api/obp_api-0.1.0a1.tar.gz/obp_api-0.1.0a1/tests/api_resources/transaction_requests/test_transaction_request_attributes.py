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


class TestTransactionRequestAttributes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attribute"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        transaction_request_attribute = client.transaction_requests.transaction_request_attributes.create(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert transaction_request_attribute.is_closed
        assert transaction_request_attribute.json() == {"foo": "bar"}
        assert cast(Any, transaction_request_attribute.is_closed) is True
        assert isinstance(transaction_request_attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attribute"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        transaction_request_attribute = (
            client.transaction_requests.transaction_request_attributes.with_raw_response.create(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )
        )

        assert transaction_request_attribute.is_closed is True
        assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert transaction_request_attribute.json() == {"foo": "bar"}
        assert isinstance(transaction_request_attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attribute"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transaction_requests.transaction_request_attributes.with_streaming_response.create(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as transaction_request_attribute:
            assert not transaction_request_attribute.is_closed
            assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert transaction_request_attribute.json() == {"foo": "bar"}
            assert cast(Any, transaction_request_attribute.is_closed) is True
            assert isinstance(transaction_request_attribute, StreamedBinaryAPIResponse)

        assert cast(Any, transaction_request_attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transaction_requests.transaction_request_attributes.with_raw_response.create(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transaction_requests.transaction_request_attributes.with_raw_response.create(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `transaction_request_id` but received ''"
        ):
            client.transaction_requests.transaction_request_attributes.with_raw_response.create(
                transaction_request_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        transaction_request_attribute = client.transaction_requests.transaction_request_attributes.retrieve(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert transaction_request_attribute.is_closed
        assert transaction_request_attribute.json() == {"foo": "bar"}
        assert cast(Any, transaction_request_attribute.is_closed) is True
        assert isinstance(transaction_request_attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        transaction_request_attribute = (
            client.transaction_requests.transaction_request_attributes.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )
        )

        assert transaction_request_attribute.is_closed is True
        assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert transaction_request_attribute.json() == {"foo": "bar"}
        assert isinstance(transaction_request_attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transaction_requests.transaction_request_attributes.with_streaming_response.retrieve(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as transaction_request_attribute:
            assert not transaction_request_attribute.is_closed
            assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert transaction_request_attribute.json() == {"foo": "bar"}
            assert cast(Any, transaction_request_attribute.is_closed) is True
            assert isinstance(transaction_request_attribute, StreamedBinaryAPIResponse)

        assert cast(Any, transaction_request_attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transaction_requests.transaction_request_attributes.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transaction_requests.transaction_request_attributes.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `transaction_request_id` but received ''"
        ):
            client.transaction_requests.transaction_request_attributes.with_raw_response.retrieve(
                transaction_request_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        transaction_request_attribute = client.transaction_requests.transaction_request_attributes.update(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert transaction_request_attribute.is_closed
        assert transaction_request_attribute.json() == {"foo": "bar"}
        assert cast(Any, transaction_request_attribute.is_closed) is True
        assert isinstance(transaction_request_attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        transaction_request_attribute = (
            client.transaction_requests.transaction_request_attributes.with_raw_response.update(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )
        )

        assert transaction_request_attribute.is_closed is True
        assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert transaction_request_attribute.json() == {"foo": "bar"}
        assert isinstance(transaction_request_attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transaction_requests.transaction_request_attributes.with_streaming_response.update(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as transaction_request_attribute:
            assert not transaction_request_attribute.is_closed
            assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert transaction_request_attribute.json() == {"foo": "bar"}
            assert cast(Any, transaction_request_attribute.is_closed) is True
            assert isinstance(transaction_request_attribute, StreamedBinaryAPIResponse)

        assert cast(Any, transaction_request_attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transaction_requests.transaction_request_attributes.with_raw_response.update(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transaction_requests.transaction_request_attributes.with_raw_response.update(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `transaction_request_id` but received ''"
        ):
            client.transaction_requests.transaction_request_attributes.with_raw_response.update(
                transaction_request_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        transaction_request_attribute = client.transaction_requests.transaction_request_attributes.list(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert transaction_request_attribute.is_closed
        assert transaction_request_attribute.json() == {"foo": "bar"}
        assert cast(Any, transaction_request_attribute.is_closed) is True
        assert isinstance(transaction_request_attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        transaction_request_attribute = (
            client.transaction_requests.transaction_request_attributes.with_raw_response.list(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )
        )

        assert transaction_request_attribute.is_closed is True
        assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert transaction_request_attribute.json() == {"foo": "bar"}
        assert isinstance(transaction_request_attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.transaction_requests.transaction_request_attributes.with_streaming_response.list(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as transaction_request_attribute:
            assert not transaction_request_attribute.is_closed
            assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert transaction_request_attribute.json() == {"foo": "bar"}
            assert cast(Any, transaction_request_attribute.is_closed) is True
            assert isinstance(transaction_request_attribute, StreamedBinaryAPIResponse)

        assert cast(Any, transaction_request_attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.transaction_requests.transaction_request_attributes.with_raw_response.list(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.transaction_requests.transaction_request_attributes.with_raw_response.list(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `transaction_request_id` but received ''"
        ):
            client.transaction_requests.transaction_request_attributes.with_raw_response.list(
                transaction_request_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )


class TestAsyncTransactionRequestAttributes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attribute"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        transaction_request_attribute = await async_client.transaction_requests.transaction_request_attributes.create(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert transaction_request_attribute.is_closed
        assert await transaction_request_attribute.json() == {"foo": "bar"}
        assert cast(Any, transaction_request_attribute.is_closed) is True
        assert isinstance(transaction_request_attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attribute"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        transaction_request_attribute = (
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.create(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )
        )

        assert transaction_request_attribute.is_closed is True
        assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await transaction_request_attribute.json() == {"foo": "bar"}
        assert isinstance(transaction_request_attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attribute"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transaction_requests.transaction_request_attributes.with_streaming_response.create(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as transaction_request_attribute:
            assert not transaction_request_attribute.is_closed
            assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await transaction_request_attribute.json() == {"foo": "bar"}
            assert cast(Any, transaction_request_attribute.is_closed) is True
            assert isinstance(transaction_request_attribute, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, transaction_request_attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.create(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.create(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `transaction_request_id` but received ''"
        ):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.create(
                transaction_request_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        transaction_request_attribute = await async_client.transaction_requests.transaction_request_attributes.retrieve(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert transaction_request_attribute.is_closed
        assert await transaction_request_attribute.json() == {"foo": "bar"}
        assert cast(Any, transaction_request_attribute.is_closed) is True
        assert isinstance(transaction_request_attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        transaction_request_attribute = (
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )
        )

        assert transaction_request_attribute.is_closed is True
        assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await transaction_request_attribute.json() == {"foo": "bar"}
        assert isinstance(transaction_request_attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transaction_requests.transaction_request_attributes.with_streaming_response.retrieve(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as transaction_request_attribute:
            assert not transaction_request_attribute.is_closed
            assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await transaction_request_attribute.json() == {"foo": "bar"}
            assert cast(Any, transaction_request_attribute.is_closed) is True
            assert isinstance(transaction_request_attribute, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, transaction_request_attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.retrieve(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `transaction_request_id` but received ''"
        ):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.retrieve(
                transaction_request_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        transaction_request_attribute = await async_client.transaction_requests.transaction_request_attributes.update(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert transaction_request_attribute.is_closed
        assert await transaction_request_attribute.json() == {"foo": "bar"}
        assert cast(Any, transaction_request_attribute.is_closed) is True
        assert isinstance(transaction_request_attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        transaction_request_attribute = (
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.update(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )
        )

        assert transaction_request_attribute.is_closed is True
        assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await transaction_request_attribute.json() == {"foo": "bar"}
        assert isinstance(transaction_request_attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transaction_requests.transaction_request_attributes.with_streaming_response.update(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as transaction_request_attribute:
            assert not transaction_request_attribute.is_closed
            assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await transaction_request_attribute.json() == {"foo": "bar"}
            assert cast(Any, transaction_request_attribute.is_closed) is True
            assert isinstance(transaction_request_attribute, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, transaction_request_attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.update(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.update(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `transaction_request_id` but received ''"
        ):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.update(
                transaction_request_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        transaction_request_attribute = await async_client.transaction_requests.transaction_request_attributes.list(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert transaction_request_attribute.is_closed
        assert await transaction_request_attribute.json() == {"foo": "bar"}
        assert cast(Any, transaction_request_attribute.is_closed) is True
        assert isinstance(transaction_request_attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        transaction_request_attribute = (
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.list(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )
        )

        assert transaction_request_attribute.is_closed is True
        assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await transaction_request_attribute.json() == {"foo": "bar"}
        assert isinstance(transaction_request_attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transaction-requests/TRANSACTION_REQUEST_ID/attributes"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.transaction_requests.transaction_request_attributes.with_streaming_response.list(
            transaction_request_id="TRANSACTION_REQUEST_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as transaction_request_attribute:
            assert not transaction_request_attribute.is_closed
            assert transaction_request_attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await transaction_request_attribute.json() == {"foo": "bar"}
            assert cast(Any, transaction_request_attribute.is_closed) is True
            assert isinstance(transaction_request_attribute, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, transaction_request_attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.list(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.list(
                transaction_request_id="TRANSACTION_REQUEST_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `transaction_request_id` but received ''"
        ):
            await async_client.transaction_requests.transaction_request_attributes.with_raw_response.list(
                transaction_request_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )
