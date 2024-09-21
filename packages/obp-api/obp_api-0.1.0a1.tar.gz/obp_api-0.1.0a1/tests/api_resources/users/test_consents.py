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


class TestConsents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/user/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = client.users.consents.retrieve(
            "CONSENT_ID",
        )
        assert consent.is_closed
        assert consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/user/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = client.users.consents.with_raw_response.retrieve(
            "CONSENT_ID",
        )

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consent.json() == {"foo": "bar"}
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/user/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.users.consents.with_streaming_response.retrieve(
            "CONSENT_ID",
        ) as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, StreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            client.users.consents.with_raw_response.retrieve(
                "",
            )


class TestAsyncConsents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/user/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = await async_client.users.consents.retrieve(
            "CONSENT_ID",
        )
        assert consent.is_closed
        assert await consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/user/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = await async_client.users.consents.with_raw_response.retrieve(
            "CONSENT_ID",
        )

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consent.json() == {"foo": "bar"}
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/user/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.users.consents.with_streaming_response.retrieve(
            "CONSENT_ID",
        ) as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            await async_client.users.consents.with_raw_response.retrieve(
                "",
            )
