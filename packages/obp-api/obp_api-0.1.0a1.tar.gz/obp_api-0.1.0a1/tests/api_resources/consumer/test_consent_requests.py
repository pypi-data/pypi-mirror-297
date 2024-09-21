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


class TestConsentRequests:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent_request = client.consumer.consent_requests.create(
            body={},
        )
        assert consent_request.is_closed
        assert consent_request.json() == {"foo": "bar"}
        assert cast(Any, consent_request.is_closed) is True
        assert isinstance(consent_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent_request = client.consumer.consent_requests.with_raw_response.create(
            body={},
        )

        assert consent_request.is_closed is True
        assert consent_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consent_request.json() == {"foo": "bar"}
        assert isinstance(consent_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consumer.consent_requests.with_streaming_response.create(
            body={},
        ) as consent_request:
            assert not consent_request.is_closed
            assert consent_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consent_request.json() == {"foo": "bar"}
            assert cast(Any, consent_request.is_closed) is True
            assert isinstance(consent_request, StreamedBinaryAPIResponse)

        assert cast(Any, consent_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent_request = client.consumer.consent_requests.retrieve()
        assert consent_request.is_closed
        assert consent_request.json() == {"foo": "bar"}
        assert cast(Any, consent_request.is_closed) is True
        assert isinstance(consent_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent_request = client.consumer.consent_requests.with_raw_response.retrieve()

        assert consent_request.is_closed is True
        assert consent_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consent_request.json() == {"foo": "bar"}
        assert isinstance(consent_request, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consumer.consent_requests.with_streaming_response.retrieve() as consent_request:
            assert not consent_request.is_closed
            assert consent_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consent_request.json() == {"foo": "bar"}
            assert cast(Any, consent_request.is_closed) is True
            assert isinstance(consent_request, StreamedBinaryAPIResponse)

        assert cast(Any, consent_request.is_closed) is True


class TestAsyncConsentRequests:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent_request = await async_client.consumer.consent_requests.create(
            body={},
        )
        assert consent_request.is_closed
        assert await consent_request.json() == {"foo": "bar"}
        assert cast(Any, consent_request.is_closed) is True
        assert isinstance(consent_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent_request = await async_client.consumer.consent_requests.with_raw_response.create(
            body={},
        )

        assert consent_request.is_closed is True
        assert consent_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consent_request.json() == {"foo": "bar"}
        assert isinstance(consent_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/consumer/consent-requests").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consumer.consent_requests.with_streaming_response.create(
            body={},
        ) as consent_request:
            assert not consent_request.is_closed
            assert consent_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consent_request.json() == {"foo": "bar"}
            assert cast(Any, consent_request.is_closed) is True
            assert isinstance(consent_request, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consent_request.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent_request = await async_client.consumer.consent_requests.retrieve()
        assert consent_request.is_closed
        assert await consent_request.json() == {"foo": "bar"}
        assert cast(Any, consent_request.is_closed) is True
        assert isinstance(consent_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent_request = await async_client.consumer.consent_requests.with_raw_response.retrieve()

        assert consent_request.is_closed is True
        assert consent_request.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consent_request.json() == {"foo": "bar"}
        assert isinstance(consent_request, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consumer.consent_requests.with_streaming_response.retrieve() as consent_request:
            assert not consent_request.is_closed
            assert consent_request.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consent_request.json() == {"foo": "bar"}
            assert cast(Any, consent_request.is_closed) is True
            assert isinstance(consent_request, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consent_request.is_closed) is True
