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
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        transaction_request = client.banks.attribute_definitions.transaction_requests.retrieve(
            "BANK_ID",
        )
        assert transaction_request.is_closed
        assert transaction_request.json() == {"foo": "bar"}
        assert cast(Any, transaction_request.is_closed) is True
        assert isinstance(transaction_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        transaction_request = client.banks.attribute_definitions.transaction_requests.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert transaction_request.is_closed is True
        assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert transaction_request.json() == {"foo": "bar"}
        assert isinstance(transaction_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.attribute_definitions.transaction_requests.with_streaming_response.retrieve(
            "BANK_ID",
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
            client.banks.attribute_definitions.transaction_requests.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        transaction_request = client.banks.attribute_definitions.transaction_requests.update(
            bank_id="BANK_ID",
            body={},
        )
        assert transaction_request.is_closed
        assert transaction_request.json() == {"foo": "bar"}
        assert cast(Any, transaction_request.is_closed) is True
        assert isinstance(transaction_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        transaction_request = client.banks.attribute_definitions.transaction_requests.with_raw_response.update(
            bank_id="BANK_ID",
            body={},
        )

        assert transaction_request.is_closed is True
        assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert transaction_request.json() == {"foo": "bar"}
        assert isinstance(transaction_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.attribute_definitions.transaction_requests.with_streaming_response.update(
            bank_id="BANK_ID",
            body={},
        ) as transaction_request:
            assert not transaction_request.is_closed
            assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert transaction_request.json() == {"foo": "bar"}
            assert cast(Any, transaction_request.is_closed) is True
            assert isinstance(transaction_request, StreamedBinaryAPIResponse)

        assert cast(Any, transaction_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.attribute_definitions.transaction_requests.with_raw_response.update(
                bank_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        transaction_request = client.banks.attribute_definitions.transaction_requests.delete(
            bank_id="BANK_ID",
            body={},
        )
        assert transaction_request.is_closed
        assert transaction_request.json() == {"foo": "bar"}
        assert cast(Any, transaction_request.is_closed) is True
        assert isinstance(transaction_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        transaction_request = client.banks.attribute_definitions.transaction_requests.with_raw_response.delete(
            bank_id="BANK_ID",
            body={},
        )

        assert transaction_request.is_closed is True
        assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert transaction_request.json() == {"foo": "bar"}
        assert isinstance(transaction_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.attribute_definitions.transaction_requests.with_streaming_response.delete(
            bank_id="BANK_ID",
            body={},
        ) as transaction_request:
            assert not transaction_request.is_closed
            assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert transaction_request.json() == {"foo": "bar"}
            assert cast(Any, transaction_request.is_closed) is True
            assert isinstance(transaction_request, StreamedBinaryAPIResponse)

        assert cast(Any, transaction_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.attribute_definitions.transaction_requests.with_raw_response.delete(
                bank_id="",
                body={},
            )


class TestAsyncTransactionRequests:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        transaction_request = await async_client.banks.attribute_definitions.transaction_requests.retrieve(
            "BANK_ID",
        )
        assert transaction_request.is_closed
        assert await transaction_request.json() == {"foo": "bar"}
        assert cast(Any, transaction_request.is_closed) is True
        assert isinstance(transaction_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        transaction_request = (
            await async_client.banks.attribute_definitions.transaction_requests.with_raw_response.retrieve(
                "BANK_ID",
            )
        )

        assert transaction_request.is_closed is True
        assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await transaction_request.json() == {"foo": "bar"}
        assert isinstance(transaction_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.attribute_definitions.transaction_requests.with_streaming_response.retrieve(
            "BANK_ID",
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
            await async_client.banks.attribute_definitions.transaction_requests.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        transaction_request = await async_client.banks.attribute_definitions.transaction_requests.update(
            bank_id="BANK_ID",
            body={},
        )
        assert transaction_request.is_closed
        assert await transaction_request.json() == {"foo": "bar"}
        assert cast(Any, transaction_request.is_closed) is True
        assert isinstance(transaction_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        transaction_request = (
            await async_client.banks.attribute_definitions.transaction_requests.with_raw_response.update(
                bank_id="BANK_ID",
                body={},
            )
        )

        assert transaction_request.is_closed is True
        assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await transaction_request.json() == {"foo": "bar"}
        assert isinstance(transaction_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/transaction-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.attribute_definitions.transaction_requests.with_streaming_response.update(
            bank_id="BANK_ID",
            body={},
        ) as transaction_request:
            assert not transaction_request.is_closed
            assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await transaction_request.json() == {"foo": "bar"}
            assert cast(Any, transaction_request.is_closed) is True
            assert isinstance(transaction_request, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, transaction_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.attribute_definitions.transaction_requests.with_raw_response.update(
                bank_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        transaction_request = await async_client.banks.attribute_definitions.transaction_requests.delete(
            bank_id="BANK_ID",
            body={},
        )
        assert transaction_request.is_closed
        assert await transaction_request.json() == {"foo": "bar"}
        assert cast(Any, transaction_request.is_closed) is True
        assert isinstance(transaction_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        transaction_request = (
            await async_client.banks.attribute_definitions.transaction_requests.with_raw_response.delete(
                bank_id="BANK_ID",
                body={},
            )
        )

        assert transaction_request.is_closed is True
        assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await transaction_request.json() == {"foo": "bar"}
        assert isinstance(transaction_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/account").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.attribute_definitions.transaction_requests.with_streaming_response.delete(
            bank_id="BANK_ID",
            body={},
        ) as transaction_request:
            assert not transaction_request.is_closed
            assert transaction_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await transaction_request.json() == {"foo": "bar"}
            assert cast(Any, transaction_request.is_closed) is True
            assert isinstance(transaction_request, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, transaction_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.attribute_definitions.transaction_requests.with_raw_response.delete(
                bank_id="",
                body={},
            )
