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
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID/EMAIL/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = client.consumer.consent_requests.email.consents.create()
        assert consent.is_closed
        assert consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID/EMAIL/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = client.consumer.consent_requests.email.consents.with_raw_response.create()

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consent.json() == {"foo": "bar"}
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID/EMAIL/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consumer.consent_requests.email.consents.with_streaming_response.create() as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, StreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True


class TestAsyncConsents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID/EMAIL/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = await async_client.consumer.consent_requests.email.consents.create()
        assert consent.is_closed
        assert await consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID/EMAIL/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = await async_client.consumer.consent_requests.email.consents.with_raw_response.create()

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consent.json() == {"foo": "bar"}
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID/EMAIL/consents").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consumer.consent_requests.email.consents.with_streaming_response.create() as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True
