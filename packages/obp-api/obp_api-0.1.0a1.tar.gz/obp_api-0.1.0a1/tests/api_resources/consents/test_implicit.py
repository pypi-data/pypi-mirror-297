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


class TestImplicit:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/my/consents/IMPLICIT").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        implicit = client.consents.implicit.create(
            bank_id="BANK_ID",
            body={},
        )
        assert implicit.is_closed
        assert implicit.json() == {"foo": "bar"}
        assert cast(Any, implicit.is_closed) is True
        assert isinstance(implicit, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/my/consents/IMPLICIT").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        implicit = client.consents.implicit.with_raw_response.create(
            bank_id="BANK_ID",
            body={},
        )

        assert implicit.is_closed is True
        assert implicit.http_request.headers.get("X-Stainless-Lang") == "python"
        assert implicit.json() == {"foo": "bar"}
        assert isinstance(implicit, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/my/consents/IMPLICIT").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consents.implicit.with_streaming_response.create(
            bank_id="BANK_ID",
            body={},
        ) as implicit:
            assert not implicit.is_closed
            assert implicit.http_request.headers.get("X-Stainless-Lang") == "python"

            assert implicit.json() == {"foo": "bar"}
            assert cast(Any, implicit.is_closed) is True
            assert isinstance(implicit, StreamedBinaryAPIResponse)

        assert cast(Any, implicit.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.consents.implicit.with_raw_response.create(
                bank_id="",
                body={},
            )


class TestAsyncImplicit:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/my/consents/IMPLICIT").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        implicit = await async_client.consents.implicit.create(
            bank_id="BANK_ID",
            body={},
        )
        assert implicit.is_closed
        assert await implicit.json() == {"foo": "bar"}
        assert cast(Any, implicit.is_closed) is True
        assert isinstance(implicit, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/my/consents/IMPLICIT").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        implicit = await async_client.consents.implicit.with_raw_response.create(
            bank_id="BANK_ID",
            body={},
        )

        assert implicit.is_closed is True
        assert implicit.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await implicit.json() == {"foo": "bar"}
        assert isinstance(implicit, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/my/consents/IMPLICIT").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consents.implicit.with_streaming_response.create(
            bank_id="BANK_ID",
            body={},
        ) as implicit:
            assert not implicit.is_closed
            assert implicit.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await implicit.json() == {"foo": "bar"}
            assert cast(Any, implicit.is_closed) is True
            assert isinstance(implicit, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, implicit.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.consents.implicit.with_raw_response.create(
                bank_id="",
                body={},
            )
