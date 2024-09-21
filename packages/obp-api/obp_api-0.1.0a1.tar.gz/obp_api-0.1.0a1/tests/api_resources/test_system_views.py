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


class TestSystemViews:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/system-views").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        system_view = client.system_views.create(
            body={},
        )
        assert system_view.is_closed
        assert system_view.json() == {"foo": "bar"}
        assert cast(Any, system_view.is_closed) is True
        assert isinstance(system_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/system-views").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        system_view = client.system_views.with_raw_response.create(
            body={},
        )

        assert system_view.is_closed is True
        assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert system_view.json() == {"foo": "bar"}
        assert isinstance(system_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/system-views").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.system_views.with_streaming_response.create(
            body={},
        ) as system_view:
            assert not system_view.is_closed
            assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert system_view.json() == {"foo": "bar"}
            assert cast(Any, system_view.is_closed) is True
            assert isinstance(system_view, StreamedBinaryAPIResponse)

        assert cast(Any, system_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        system_view = client.system_views.retrieve(
            "VIEW_ID",
        )
        assert system_view.is_closed
        assert system_view.json() == {"foo": "bar"}
        assert cast(Any, system_view.is_closed) is True
        assert isinstance(system_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        system_view = client.system_views.with_raw_response.retrieve(
            "VIEW_ID",
        )

        assert system_view.is_closed is True
        assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert system_view.json() == {"foo": "bar"}
        assert isinstance(system_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.system_views.with_streaming_response.retrieve(
            "VIEW_ID",
        ) as system_view:
            assert not system_view.is_closed
            assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert system_view.json() == {"foo": "bar"}
            assert cast(Any, system_view.is_closed) is True
            assert isinstance(system_view, StreamedBinaryAPIResponse)

        assert cast(Any, system_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.system_views.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        system_view = client.system_views.update(
            view_id="VIEW_ID",
            body={},
        )
        assert system_view.is_closed
        assert system_view.json() == {"foo": "bar"}
        assert cast(Any, system_view.is_closed) is True
        assert isinstance(system_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        system_view = client.system_views.with_raw_response.update(
            view_id="VIEW_ID",
            body={},
        )

        assert system_view.is_closed is True
        assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert system_view.json() == {"foo": "bar"}
        assert isinstance(system_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.system_views.with_streaming_response.update(
            view_id="VIEW_ID",
            body={},
        ) as system_view:
            assert not system_view.is_closed
            assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert system_view.json() == {"foo": "bar"}
            assert cast(Any, system_view.is_closed) is True
            assert isinstance(system_view, StreamedBinaryAPIResponse)

        assert cast(Any, system_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.system_views.with_raw_response.update(
                view_id="",
                body={},
            )

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        system_view = client.system_views.delete(
            "VIEW_ID",
        )
        assert system_view is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.system_views.with_raw_response.delete(
            "VIEW_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        system_view = response.parse()
        assert system_view is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.system_views.with_streaming_response.delete(
            "VIEW_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            system_view = response.parse()
            assert system_view is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.system_views.with_raw_response.delete(
                "",
            )


class TestAsyncSystemViews:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/system-views").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        system_view = await async_client.system_views.create(
            body={},
        )
        assert system_view.is_closed
        assert await system_view.json() == {"foo": "bar"}
        assert cast(Any, system_view.is_closed) is True
        assert isinstance(system_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/system-views").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        system_view = await async_client.system_views.with_raw_response.create(
            body={},
        )

        assert system_view.is_closed is True
        assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await system_view.json() == {"foo": "bar"}
        assert isinstance(system_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/system-views").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.system_views.with_streaming_response.create(
            body={},
        ) as system_view:
            assert not system_view.is_closed
            assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await system_view.json() == {"foo": "bar"}
            assert cast(Any, system_view.is_closed) is True
            assert isinstance(system_view, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, system_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        system_view = await async_client.system_views.retrieve(
            "VIEW_ID",
        )
        assert system_view.is_closed
        assert await system_view.json() == {"foo": "bar"}
        assert cast(Any, system_view.is_closed) is True
        assert isinstance(system_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        system_view = await async_client.system_views.with_raw_response.retrieve(
            "VIEW_ID",
        )

        assert system_view.is_closed is True
        assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await system_view.json() == {"foo": "bar"}
        assert isinstance(system_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.system_views.with_streaming_response.retrieve(
            "VIEW_ID",
        ) as system_view:
            assert not system_view.is_closed
            assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await system_view.json() == {"foo": "bar"}
            assert cast(Any, system_view.is_closed) is True
            assert isinstance(system_view, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, system_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.system_views.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        system_view = await async_client.system_views.update(
            view_id="VIEW_ID",
            body={},
        )
        assert system_view.is_closed
        assert await system_view.json() == {"foo": "bar"}
        assert cast(Any, system_view.is_closed) is True
        assert isinstance(system_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        system_view = await async_client.system_views.with_raw_response.update(
            view_id="VIEW_ID",
            body={},
        )

        assert system_view.is_closed is True
        assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await system_view.json() == {"foo": "bar"}
        assert isinstance(system_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/system-views/VIEW_ID").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.system_views.with_streaming_response.update(
            view_id="VIEW_ID",
            body={},
        ) as system_view:
            assert not system_view.is_closed
            assert system_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await system_view.json() == {"foo": "bar"}
            assert cast(Any, system_view.is_closed) is True
            assert isinstance(system_view, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, system_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.system_views.with_raw_response.update(
                view_id="",
                body={},
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        system_view = await async_client.system_views.delete(
            "VIEW_ID",
        )
        assert system_view is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.system_views.with_raw_response.delete(
            "VIEW_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        system_view = await response.parse()
        assert system_view is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.system_views.with_streaming_response.delete(
            "VIEW_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            system_view = await response.parse()
            assert system_view is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.system_views.with_raw_response.delete(
                "",
            )
