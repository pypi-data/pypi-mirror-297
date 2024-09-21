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


class TestStatistics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/search/warehouse/statistics/INDEX/FIELD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        statistic = client.search.warehouse.statistics.create(
            field="FIELD",
            index="INDEX",
            body={},
        )
        assert statistic.is_closed
        assert statistic.json() == {"foo": "bar"}
        assert cast(Any, statistic.is_closed) is True
        assert isinstance(statistic, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/search/warehouse/statistics/INDEX/FIELD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        statistic = client.search.warehouse.statistics.with_raw_response.create(
            field="FIELD",
            index="INDEX",
            body={},
        )

        assert statistic.is_closed is True
        assert statistic.http_request.headers.get("X-Stainless-Lang") == "python"
        assert statistic.json() == {"foo": "bar"}
        assert isinstance(statistic, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/search/warehouse/statistics/INDEX/FIELD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.search.warehouse.statistics.with_streaming_response.create(
            field="FIELD",
            index="INDEX",
            body={},
        ) as statistic:
            assert not statistic.is_closed
            assert statistic.http_request.headers.get("X-Stainless-Lang") == "python"

            assert statistic.json() == {"foo": "bar"}
            assert cast(Any, statistic.is_closed) is True
            assert isinstance(statistic, StreamedBinaryAPIResponse)

        assert cast(Any, statistic.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index` but received ''"):
            client.search.warehouse.statistics.with_raw_response.create(
                field="FIELD",
                index="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `field` but received ''"):
            client.search.warehouse.statistics.with_raw_response.create(
                field="",
                index="INDEX",
                body={},
            )


class TestAsyncStatistics:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/search/warehouse/statistics/INDEX/FIELD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        statistic = await async_client.search.warehouse.statistics.create(
            field="FIELD",
            index="INDEX",
            body={},
        )
        assert statistic.is_closed
        assert await statistic.json() == {"foo": "bar"}
        assert cast(Any, statistic.is_closed) is True
        assert isinstance(statistic, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/search/warehouse/statistics/INDEX/FIELD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        statistic = await async_client.search.warehouse.statistics.with_raw_response.create(
            field="FIELD",
            index="INDEX",
            body={},
        )

        assert statistic.is_closed is True
        assert statistic.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await statistic.json() == {"foo": "bar"}
        assert isinstance(statistic, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/search/warehouse/statistics/INDEX/FIELD").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.search.warehouse.statistics.with_streaming_response.create(
            field="FIELD",
            index="INDEX",
            body={},
        ) as statistic:
            assert not statistic.is_closed
            assert statistic.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await statistic.json() == {"foo": "bar"}
            assert cast(Any, statistic.is_closed) is True
            assert isinstance(statistic, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, statistic.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index` but received ''"):
            await async_client.search.warehouse.statistics.with_raw_response.create(
                field="FIELD",
                index="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `field` but received ''"):
            await async_client.search.warehouse.statistics.with_raw_response.create(
                field="",
                index="INDEX",
                body={},
            )
