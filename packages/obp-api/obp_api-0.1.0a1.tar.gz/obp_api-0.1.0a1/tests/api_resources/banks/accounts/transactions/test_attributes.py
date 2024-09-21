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


class TestAttributes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        attribute = client.banks.accounts.transactions.attributes.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert attribute.is_closed
        assert attribute.json() == {"foo": "bar"}
        assert cast(Any, attribute.is_closed) is True
        assert isinstance(attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        attribute = client.banks.accounts.transactions.attributes.with_raw_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert attribute.is_closed is True
        assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert attribute.json() == {"foo": "bar"}
        assert isinstance(attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.accounts.transactions.attributes.with_streaming_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as attribute:
            assert not attribute.is_closed
            assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert attribute.json() == {"foo": "bar"}
            assert cast(Any, attribute.is_closed) is True
            assert isinstance(attribute, StreamedBinaryAPIResponse)

        assert cast(Any, attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.transactions.attributes.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.transactions.attributes.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.banks.accounts.transactions.attributes.with_raw_response.retrieve(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ACCOUNT_ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        attribute = client.banks.accounts.transactions.attributes.update(
            account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )
        assert attribute.is_closed
        assert attribute.json() == {"foo": "bar"}
        assert cast(Any, attribute.is_closed) is True
        assert isinstance(attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ACCOUNT_ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        attribute = client.banks.accounts.transactions.attributes.with_raw_response.update(
            account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )

        assert attribute.is_closed is True
        assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert attribute.json() == {"foo": "bar"}
        assert isinstance(attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ACCOUNT_ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.accounts.transactions.attributes.with_streaming_response.update(
            account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        ) as attribute:
            assert not attribute.is_closed
            assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert attribute.json() == {"foo": "bar"}
            assert cast(Any, attribute.is_closed) is True
            assert isinstance(attribute, StreamedBinaryAPIResponse)

        assert cast(Any, attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.transactions.attributes.with_raw_response.update(
                account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.transactions.attributes.with_raw_response.update(
                account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
                bank_id="BANK_ID",
                account_id="",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.banks.accounts.transactions.attributes.with_raw_response.update(
                account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                transaction_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_attribute_id` but received ''"):
            client.banks.accounts.transactions.attributes.with_raw_response.update(
                account_attribute_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        attribute = client.banks.accounts.transactions.attributes.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert attribute.is_closed
        assert attribute.json() == {"foo": "bar"}
        assert cast(Any, attribute.is_closed) is True
        assert isinstance(attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        attribute = client.banks.accounts.transactions.attributes.with_raw_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert attribute.is_closed is True
        assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert attribute.json() == {"foo": "bar"}
        assert isinstance(attribute, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.accounts.transactions.attributes.with_streaming_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as attribute:
            assert not attribute.is_closed
            assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert attribute.json() == {"foo": "bar"}
            assert cast(Any, attribute.is_closed) is True
            assert isinstance(attribute, StreamedBinaryAPIResponse)

        assert cast(Any, attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.transactions.attributes.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.transactions.attributes.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.banks.accounts.transactions.attributes.with_raw_response.list(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )


class TestAsyncAttributes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        attribute = await async_client.banks.accounts.transactions.attributes.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert attribute.is_closed
        assert await attribute.json() == {"foo": "bar"}
        assert cast(Any, attribute.is_closed) is True
        assert isinstance(attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        attribute = await async_client.banks.accounts.transactions.attributes.with_raw_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert attribute.is_closed is True
        assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await attribute.json() == {"foo": "bar"}
        assert isinstance(attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.accounts.transactions.attributes.with_streaming_response.retrieve(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as attribute:
            assert not attribute.is_closed
            assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await attribute.json() == {"foo": "bar"}
            assert cast(Any, attribute.is_closed) is True
            assert isinstance(attribute, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.transactions.attributes.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.transactions.attributes.with_raw_response.retrieve(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.banks.accounts.transactions.attributes.with_raw_response.retrieve(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ACCOUNT_ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        attribute = await async_client.banks.accounts.transactions.attributes.update(
            account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )
        assert attribute.is_closed
        assert await attribute.json() == {"foo": "bar"}
        assert cast(Any, attribute.is_closed) is True
        assert isinstance(attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ACCOUNT_ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        attribute = await async_client.banks.accounts.transactions.attributes.with_raw_response.update(
            account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        )

        assert attribute.is_closed is True
        assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await attribute.json() == {"foo": "bar"}
        assert isinstance(attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes/ACCOUNT_ATTRIBUTE_ID"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.accounts.transactions.attributes.with_streaming_response.update(
            account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            transaction_id="TRANSACTION_ID",
            body={},
        ) as attribute:
            assert not attribute.is_closed
            assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await attribute.json() == {"foo": "bar"}
            assert cast(Any, attribute.is_closed) is True
            assert isinstance(attribute, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.transactions.attributes.with_raw_response.update(
                account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.transactions.attributes.with_raw_response.update(
                account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
                bank_id="BANK_ID",
                account_id="",
                transaction_id="TRANSACTION_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.banks.accounts.transactions.attributes.with_raw_response.update(
                account_attribute_id="ACCOUNT_ATTRIBUTE_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                transaction_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_attribute_id` but received ''"):
            await async_client.banks.accounts.transactions.attributes.with_raw_response.update(
                account_attribute_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                transaction_id="TRANSACTION_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        attribute = await async_client.banks.accounts.transactions.attributes.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert attribute.is_closed
        assert await attribute.json() == {"foo": "bar"}
        assert cast(Any, attribute.is_closed) is True
        assert isinstance(attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        attribute = await async_client.banks.accounts.transactions.attributes.with_raw_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert attribute.is_closed is True
        assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await attribute.json() == {"foo": "bar"}
        assert isinstance(attribute, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/transactions/TRANSACTION_ID/attributes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.accounts.transactions.attributes.with_streaming_response.list(
            transaction_id="TRANSACTION_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as attribute:
            assert not attribute.is_closed
            assert attribute.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await attribute.json() == {"foo": "bar"}
            assert cast(Any, attribute.is_closed) is True
            assert isinstance(attribute, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, attribute.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.transactions.attributes.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.transactions.attributes.with_raw_response.list(
                transaction_id="TRANSACTION_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.banks.accounts.transactions.attributes.with_raw_response.list(
                transaction_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )
