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


class TestNotes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/notes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        note = client.banks.atms.notes.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert note.is_closed
        assert note.json() == {"foo": "bar"}
        assert cast(Any, note.is_closed) is True
        assert isinstance(note, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/notes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        note = client.banks.atms.notes.with_raw_response.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert note.is_closed is True
        assert note.http_request.headers.get("X-Stainless-Lang") == "python"
        assert note.json() == {"foo": "bar"}
        assert isinstance(note, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/notes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.atms.notes.with_streaming_response.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        ) as note:
            assert not note.is_closed
            assert note.http_request.headers.get("X-Stainless-Lang") == "python"

            assert note.json() == {"foo": "bar"}
            assert cast(Any, note.is_closed) is True
            assert isinstance(note, StreamedBinaryAPIResponse)

        assert cast(Any, note.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.atms.notes.with_raw_response.update(
                atm_id="ATM_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `atm_id` but received ''"):
            client.banks.atms.notes.with_raw_response.update(
                atm_id="",
                bank_id="BANK_ID",
                body={},
            )


class TestAsyncNotes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/notes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        note = await async_client.banks.atms.notes.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert note.is_closed
        assert await note.json() == {"foo": "bar"}
        assert cast(Any, note.is_closed) is True
        assert isinstance(note, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/notes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        note = await async_client.banks.atms.notes.with_raw_response.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert note.is_closed is True
        assert note.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await note.json() == {"foo": "bar"}
        assert isinstance(note, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/atms/ATM_ID/notes").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.atms.notes.with_streaming_response.update(
            atm_id="ATM_ID",
            bank_id="BANK_ID",
            body={},
        ) as note:
            assert not note.is_closed
            assert note.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await note.json() == {"foo": "bar"}
            assert cast(Any, note.is_closed) is True
            assert isinstance(note, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, note.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.atms.notes.with_raw_response.update(
                atm_id="ATM_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `atm_id` but received ''"):
            await async_client.banks.atms.notes.with_raw_response.update(
                atm_id="",
                bank_id="BANK_ID",
                body={},
            )
