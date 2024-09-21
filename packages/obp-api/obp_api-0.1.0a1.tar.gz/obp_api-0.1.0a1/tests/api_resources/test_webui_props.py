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


class TestWebuiProps:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/webui_props").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        webui_prop = client.webui_props.create(
            body={},
        )
        assert webui_prop.is_closed
        assert webui_prop.json() == {"foo": "bar"}
        assert cast(Any, webui_prop.is_closed) is True
        assert isinstance(webui_prop, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/webui_props").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        webui_prop = client.webui_props.with_raw_response.create(
            body={},
        )

        assert webui_prop.is_closed is True
        assert webui_prop.http_request.headers.get("X-Stainless-Lang") == "python"
        assert webui_prop.json() == {"foo": "bar"}
        assert isinstance(webui_prop, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/webui_props").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.webui_props.with_streaming_response.create(
            body={},
        ) as webui_prop:
            assert not webui_prop.is_closed
            assert webui_prop.http_request.headers.get("X-Stainless-Lang") == "python"

            assert webui_prop.json() == {"foo": "bar"}
            assert cast(Any, webui_prop.is_closed) is True
            assert isinstance(webui_prop, StreamedBinaryAPIResponse)

        assert cast(Any, webui_prop.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/webui_props").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        webui_prop = client.webui_props.list()
        assert webui_prop.is_closed
        assert webui_prop.json() == {"foo": "bar"}
        assert cast(Any, webui_prop.is_closed) is True
        assert isinstance(webui_prop, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/webui_props").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        webui_prop = client.webui_props.with_raw_response.list()

        assert webui_prop.is_closed is True
        assert webui_prop.http_request.headers.get("X-Stainless-Lang") == "python"
        assert webui_prop.json() == {"foo": "bar"}
        assert isinstance(webui_prop, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/webui_props").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.webui_props.with_streaming_response.list() as webui_prop:
            assert not webui_prop.is_closed
            assert webui_prop.http_request.headers.get("X-Stainless-Lang") == "python"

            assert webui_prop.json() == {"foo": "bar"}
            assert cast(Any, webui_prop.is_closed) is True
            assert isinstance(webui_prop, StreamedBinaryAPIResponse)

        assert cast(Any, webui_prop.is_closed) is True

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        webui_prop = client.webui_props.delete(
            "WEB_UI_PROPS_ID",
        )
        assert webui_prop is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.webui_props.with_raw_response.delete(
            "WEB_UI_PROPS_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webui_prop = response.parse()
        assert webui_prop is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.webui_props.with_streaming_response.delete(
            "WEB_UI_PROPS_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webui_prop = response.parse()
            assert webui_prop is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `web_ui_props_id` but received ''"):
            client.webui_props.with_raw_response.delete(
                "",
            )


class TestAsyncWebuiProps:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/webui_props").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        webui_prop = await async_client.webui_props.create(
            body={},
        )
        assert webui_prop.is_closed
        assert await webui_prop.json() == {"foo": "bar"}
        assert cast(Any, webui_prop.is_closed) is True
        assert isinstance(webui_prop, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/webui_props").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        webui_prop = await async_client.webui_props.with_raw_response.create(
            body={},
        )

        assert webui_prop.is_closed is True
        assert webui_prop.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await webui_prop.json() == {"foo": "bar"}
        assert isinstance(webui_prop, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/webui_props").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.webui_props.with_streaming_response.create(
            body={},
        ) as webui_prop:
            assert not webui_prop.is_closed
            assert webui_prop.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await webui_prop.json() == {"foo": "bar"}
            assert cast(Any, webui_prop.is_closed) is True
            assert isinstance(webui_prop, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, webui_prop.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/webui_props").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        webui_prop = await async_client.webui_props.list()
        assert webui_prop.is_closed
        assert await webui_prop.json() == {"foo": "bar"}
        assert cast(Any, webui_prop.is_closed) is True
        assert isinstance(webui_prop, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/webui_props").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        webui_prop = await async_client.webui_props.with_raw_response.list()

        assert webui_prop.is_closed is True
        assert webui_prop.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await webui_prop.json() == {"foo": "bar"}
        assert isinstance(webui_prop, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/webui_props").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.webui_props.with_streaming_response.list() as webui_prop:
            assert not webui_prop.is_closed
            assert webui_prop.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await webui_prop.json() == {"foo": "bar"}
            assert cast(Any, webui_prop.is_closed) is True
            assert isinstance(webui_prop, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, webui_prop.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        webui_prop = await async_client.webui_props.delete(
            "WEB_UI_PROPS_ID",
        )
        assert webui_prop is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.webui_props.with_raw_response.delete(
            "WEB_UI_PROPS_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webui_prop = await response.parse()
        assert webui_prop is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.webui_props.with_streaming_response.delete(
            "WEB_UI_PROPS_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webui_prop = await response.parse()
            assert webui_prop is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `web_ui_props_id` but received ''"):
            await async_client.webui_props.with_raw_response.delete(
                "",
            )
