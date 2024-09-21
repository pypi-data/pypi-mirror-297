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


class TestConsumers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        consumer = client.consumers.create(
            body={},
        )
        assert consumer.is_closed
        assert consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        consumer = client.consumers.with_raw_response.create(
            body={},
        )

        assert consumer.is_closed is True
        assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consumer.json() == {"foo": "bar"}
        assert isinstance(consumer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.consumers.with_streaming_response.create(
            body={},
        ) as consumer:
            assert not consumer.is_closed
            assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consumer.json() == {"foo": "bar"}
            assert cast(Any, consumer.is_closed) is True
            assert isinstance(consumer, StreamedBinaryAPIResponse)

        assert cast(Any, consumer.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consumer = client.consumers.retrieve(
            "CONSUMER_ID",
        )
        assert consumer.is_closed
        assert consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consumer = client.consumers.with_raw_response.retrieve(
            "CONSUMER_ID",
        )

        assert consumer.is_closed is True
        assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consumer.json() == {"foo": "bar"}
        assert isinstance(consumer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consumers.with_streaming_response.retrieve(
            "CONSUMER_ID",
        ) as consumer:
            assert not consumer.is_closed
            assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consumer.json() == {"foo": "bar"}
            assert cast(Any, consumer.is_closed) is True
            assert isinstance(consumer, StreamedBinaryAPIResponse)

        assert cast(Any, consumer.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consumer_id` but received ''"):
            client.consumers.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consumer = client.consumers.update(
            consumer_id="CONSUMER_ID",
            body={},
        )
        assert consumer.is_closed
        assert consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consumer = client.consumers.with_raw_response.update(
            consumer_id="CONSUMER_ID",
            body={},
        )

        assert consumer.is_closed is True
        assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consumer.json() == {"foo": "bar"}
        assert isinstance(consumer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consumers.with_streaming_response.update(
            consumer_id="CONSUMER_ID",
            body={},
        ) as consumer:
            assert not consumer.is_closed
            assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consumer.json() == {"foo": "bar"}
            assert cast(Any, consumer.is_closed) is True
            assert isinstance(consumer, StreamedBinaryAPIResponse)

        assert cast(Any, consumer.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consumer_id` but received ''"):
            client.consumers.with_raw_response.update(
                consumer_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        consumer = client.consumers.list()
        assert consumer.is_closed
        assert consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        consumer = client.consumers.with_raw_response.list()

        assert consumer.is_closed is True
        assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consumer.json() == {"foo": "bar"}
        assert isinstance(consumer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.consumers.with_streaming_response.list() as consumer:
            assert not consumer.is_closed
            assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consumer.json() == {"foo": "bar"}
            assert cast(Any, consumer.is_closed) is True
            assert isinstance(consumer, StreamedBinaryAPIResponse)

        assert cast(Any, consumer.is_closed) is True


class TestAsyncConsumers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        consumer = await async_client.consumers.create(
            body={},
        )
        assert consumer.is_closed
        assert await consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        consumer = await async_client.consumers.with_raw_response.create(
            body={},
        )

        assert consumer.is_closed is True
        assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consumer.json() == {"foo": "bar"}
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.consumers.with_streaming_response.create(
            body={},
        ) as consumer:
            assert not consumer.is_closed
            assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consumer.json() == {"foo": "bar"}
            assert cast(Any, consumer.is_closed) is True
            assert isinstance(consumer, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consumer.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consumer = await async_client.consumers.retrieve(
            "CONSUMER_ID",
        )
        assert consumer.is_closed
        assert await consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consumer = await async_client.consumers.with_raw_response.retrieve(
            "CONSUMER_ID",
        )

        assert consumer.is_closed is True
        assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consumer.json() == {"foo": "bar"}
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consumers.with_streaming_response.retrieve(
            "CONSUMER_ID",
        ) as consumer:
            assert not consumer.is_closed
            assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consumer.json() == {"foo": "bar"}
            assert cast(Any, consumer.is_closed) is True
            assert isinstance(consumer, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consumer.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consumer_id` but received ''"):
            await async_client.consumers.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consumer = await async_client.consumers.update(
            consumer_id="CONSUMER_ID",
            body={},
        )
        assert consumer.is_closed
        assert await consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consumer = await async_client.consumers.with_raw_response.update(
            consumer_id="CONSUMER_ID",
            body={},
        )

        assert consumer.is_closed is True
        assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consumer.json() == {"foo": "bar"}
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/management/consumers/CONSUMER_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consumers.with_streaming_response.update(
            consumer_id="CONSUMER_ID",
            body={},
        ) as consumer:
            assert not consumer.is_closed
            assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consumer.json() == {"foo": "bar"}
            assert cast(Any, consumer.is_closed) is True
            assert isinstance(consumer, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consumer.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consumer_id` but received ''"):
            await async_client.consumers.with_raw_response.update(
                consumer_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        consumer = await async_client.consumers.list()
        assert consumer.is_closed
        assert await consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        consumer = await async_client.consumers.with_raw_response.list()

        assert consumer.is_closed is True
        assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consumer.json() == {"foo": "bar"}
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/management/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.consumers.with_streaming_response.list() as consumer:
            assert not consumer.is_closed
            assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consumer.json() == {"foo": "bar"}
            assert cast(Any, consumer.is_closed) is True
            assert isinstance(consumer, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consumer.is_closed) is True
