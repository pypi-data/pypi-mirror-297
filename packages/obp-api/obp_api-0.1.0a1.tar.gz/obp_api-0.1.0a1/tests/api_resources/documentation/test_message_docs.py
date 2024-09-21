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


class TestMessageDocs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        message_doc = client.documentation.message_docs.retrieve()
        assert message_doc.is_closed
        assert message_doc.json() == {"foo": "bar"}
        assert cast(Any, message_doc.is_closed) is True
        assert isinstance(message_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        message_doc = client.documentation.message_docs.with_raw_response.retrieve()

        assert message_doc.is_closed is True
        assert message_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert message_doc.json() == {"foo": "bar"}
        assert isinstance(message_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.documentation.message_docs.with_streaming_response.retrieve() as message_doc:
            assert not message_doc.is_closed
            assert message_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert message_doc.json() == {"foo": "bar"}
            assert cast(Any, message_doc.is_closed) is True
            assert isinstance(message_doc, StreamedBinaryAPIResponse)

        assert cast(Any, message_doc.is_closed) is True


class TestAsyncMessageDocs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        message_doc = await async_client.documentation.message_docs.retrieve()
        assert message_doc.is_closed
        assert await message_doc.json() == {"foo": "bar"}
        assert cast(Any, message_doc.is_closed) is True
        assert isinstance(message_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        message_doc = await async_client.documentation.message_docs.with_raw_response.retrieve()

        assert message_doc.is_closed is True
        assert message_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await message_doc.json() == {"foo": "bar"}
        assert isinstance(message_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/message-docs/CONNECTOR").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.documentation.message_docs.with_streaming_response.retrieve() as message_doc:
            assert not message_doc.is_closed
            assert message_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await message_doc.json() == {"foo": "bar"}
            assert cast(Any, message_doc.is_closed) is True
            assert isinstance(message_doc, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, message_doc.is_closed) is True
