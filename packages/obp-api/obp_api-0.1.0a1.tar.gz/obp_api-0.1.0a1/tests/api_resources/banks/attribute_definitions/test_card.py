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


class TestCard:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        card = client.banks.attribute_definitions.card.retrieve(
            "BANK_ID",
        )
        assert card.is_closed
        assert card.json() == {"foo": "bar"}
        assert cast(Any, card.is_closed) is True
        assert isinstance(card, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        card = client.banks.attribute_definitions.card.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert card.is_closed is True
        assert card.http_request.headers.get("X-Stainless-Lang") == "python"
        assert card.json() == {"foo": "bar"}
        assert isinstance(card, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.attribute_definitions.card.with_streaming_response.retrieve(
            "BANK_ID",
        ) as card:
            assert not card.is_closed
            assert card.http_request.headers.get("X-Stainless-Lang") == "python"

            assert card.json() == {"foo": "bar"}
            assert cast(Any, card.is_closed) is True
            assert isinstance(card, StreamedBinaryAPIResponse)

        assert cast(Any, card.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.attribute_definitions.card.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        card = client.banks.attribute_definitions.card.update(
            bank_id="BANK_ID",
            body={},
        )
        assert card.is_closed
        assert card.json() == {"foo": "bar"}
        assert cast(Any, card.is_closed) is True
        assert isinstance(card, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        card = client.banks.attribute_definitions.card.with_raw_response.update(
            bank_id="BANK_ID",
            body={},
        )

        assert card.is_closed is True
        assert card.http_request.headers.get("X-Stainless-Lang") == "python"
        assert card.json() == {"foo": "bar"}
        assert isinstance(card, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.attribute_definitions.card.with_streaming_response.update(
            bank_id="BANK_ID",
            body={},
        ) as card:
            assert not card.is_closed
            assert card.http_request.headers.get("X-Stainless-Lang") == "python"

            assert card.json() == {"foo": "bar"}
            assert cast(Any, card.is_closed) is True
            assert isinstance(card, StreamedBinaryAPIResponse)

        assert cast(Any, card.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.attribute_definitions.card.with_raw_response.update(
                bank_id="",
                body={},
            )


class TestAsyncCard:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        card = await async_client.banks.attribute_definitions.card.retrieve(
            "BANK_ID",
        )
        assert card.is_closed
        assert await card.json() == {"foo": "bar"}
        assert cast(Any, card.is_closed) is True
        assert isinstance(card, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        card = await async_client.banks.attribute_definitions.card.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert card.is_closed is True
        assert card.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await card.json() == {"foo": "bar"}
        assert isinstance(card, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.attribute_definitions.card.with_streaming_response.retrieve(
            "BANK_ID",
        ) as card:
            assert not card.is_closed
            assert card.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await card.json() == {"foo": "bar"}
            assert cast(Any, card.is_closed) is True
            assert isinstance(card, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, card.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.attribute_definitions.card.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        card = await async_client.banks.attribute_definitions.card.update(
            bank_id="BANK_ID",
            body={},
        )
        assert card.is_closed
        assert await card.json() == {"foo": "bar"}
        assert cast(Any, card.is_closed) is True
        assert isinstance(card, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        card = await async_client.banks.attribute_definitions.card.with_raw_response.update(
            bank_id="BANK_ID",
            body={},
        )

        assert card.is_closed is True
        assert card.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await card.json() == {"foo": "bar"}
        assert isinstance(card, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/attribute-definitions/card").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.attribute_definitions.card.with_streaming_response.update(
            bank_id="BANK_ID",
            body={},
        ) as card:
            assert not card.is_closed
            assert card.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await card.json() == {"foo": "bar"}
            assert cast(Any, card.is_closed) is True
            assert isinstance(card, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, card.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.attribute_definitions.card.with_raw_response.update(
                bank_id="",
                body={},
            )
