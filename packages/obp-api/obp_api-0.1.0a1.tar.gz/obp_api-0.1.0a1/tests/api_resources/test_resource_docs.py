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


class TestResourceDocs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/obp").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        resource_doc = client.resource_docs.list(
            "API_VERSION",
        )
        assert resource_doc.is_closed
        assert resource_doc.json() == {"foo": "bar"}
        assert cast(Any, resource_doc.is_closed) is True
        assert isinstance(resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/obp").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        resource_doc = client.resource_docs.with_raw_response.list(
            "API_VERSION",
        )

        assert resource_doc.is_closed is True
        assert resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert resource_doc.json() == {"foo": "bar"}
        assert isinstance(resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/obp").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.resource_docs.with_streaming_response.list(
            "API_VERSION",
        ) as resource_doc:
            assert not resource_doc.is_closed
            assert resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert resource_doc.json() == {"foo": "bar"}
            assert cast(Any, resource_doc.is_closed) is True
            assert isinstance(resource_doc, StreamedBinaryAPIResponse)

        assert cast(Any, resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_version` but received ''"):
            client.resource_docs.with_raw_response.list(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_swagger(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/swagger").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        resource_doc = client.resource_docs.swagger(
            "API_VERSION",
        )
        assert resource_doc.is_closed
        assert resource_doc.json() == {"foo": "bar"}
        assert cast(Any, resource_doc.is_closed) is True
        assert isinstance(resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_swagger(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/swagger").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        resource_doc = client.resource_docs.with_raw_response.swagger(
            "API_VERSION",
        )

        assert resource_doc.is_closed is True
        assert resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert resource_doc.json() == {"foo": "bar"}
        assert isinstance(resource_doc, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_swagger(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/swagger").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.resource_docs.with_streaming_response.swagger(
            "API_VERSION",
        ) as resource_doc:
            assert not resource_doc.is_closed
            assert resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert resource_doc.json() == {"foo": "bar"}
            assert cast(Any, resource_doc.is_closed) is True
            assert isinstance(resource_doc, StreamedBinaryAPIResponse)

        assert cast(Any, resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_swagger(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_version` but received ''"):
            client.resource_docs.with_raw_response.swagger(
                "",
            )


class TestAsyncResourceDocs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/obp").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        resource_doc = await async_client.resource_docs.list(
            "API_VERSION",
        )
        assert resource_doc.is_closed
        assert await resource_doc.json() == {"foo": "bar"}
        assert cast(Any, resource_doc.is_closed) is True
        assert isinstance(resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/obp").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        resource_doc = await async_client.resource_docs.with_raw_response.list(
            "API_VERSION",
        )

        assert resource_doc.is_closed is True
        assert resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await resource_doc.json() == {"foo": "bar"}
        assert isinstance(resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/obp").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.resource_docs.with_streaming_response.list(
            "API_VERSION",
        ) as resource_doc:
            assert not resource_doc.is_closed
            assert resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await resource_doc.json() == {"foo": "bar"}
            assert cast(Any, resource_doc.is_closed) is True
            assert isinstance(resource_doc, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_version` but received ''"):
            await async_client.resource_docs.with_raw_response.list(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_swagger(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/swagger").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        resource_doc = await async_client.resource_docs.swagger(
            "API_VERSION",
        )
        assert resource_doc.is_closed
        assert await resource_doc.json() == {"foo": "bar"}
        assert cast(Any, resource_doc.is_closed) is True
        assert isinstance(resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_swagger(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/swagger").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        resource_doc = await async_client.resource_docs.with_raw_response.swagger(
            "API_VERSION",
        )

        assert resource_doc.is_closed is True
        assert resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await resource_doc.json() == {"foo": "bar"}
        assert isinstance(resource_doc, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_swagger(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/resource-docs/API_VERSION/swagger").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.resource_docs.with_streaming_response.swagger(
            "API_VERSION",
        ) as resource_doc:
            assert not resource_doc.is_closed
            assert resource_doc.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await resource_doc.json() == {"foo": "bar"}
            assert cast(Any, resource_doc.is_closed) is True
            assert isinstance(resource_doc, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, resource_doc.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_swagger(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_version` but received ''"):
            await async_client.resource_docs.with_raw_response.swagger(
                "",
            )
