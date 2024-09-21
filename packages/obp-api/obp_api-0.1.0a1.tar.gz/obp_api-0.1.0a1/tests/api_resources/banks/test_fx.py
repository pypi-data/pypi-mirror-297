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


class TestFx:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/fx/FROM_CURRENCY_CODE/TO_CURRENCY_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fx = client.banks.fx.retrieve(
            to_currency_code="TO_CURRENCY_CODE",
            bank_id="BANK_ID",
            from_currency_code="FROM_CURRENCY_CODE",
        )
        assert fx.is_closed
        assert fx.json() == {"foo": "bar"}
        assert cast(Any, fx.is_closed) is True
        assert isinstance(fx, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/fx/FROM_CURRENCY_CODE/TO_CURRENCY_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fx = client.banks.fx.with_raw_response.retrieve(
            to_currency_code="TO_CURRENCY_CODE",
            bank_id="BANK_ID",
            from_currency_code="FROM_CURRENCY_CODE",
        )

        assert fx.is_closed is True
        assert fx.http_request.headers.get("X-Stainless-Lang") == "python"
        assert fx.json() == {"foo": "bar"}
        assert isinstance(fx, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/fx/FROM_CURRENCY_CODE/TO_CURRENCY_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.fx.with_streaming_response.retrieve(
            to_currency_code="TO_CURRENCY_CODE",
            bank_id="BANK_ID",
            from_currency_code="FROM_CURRENCY_CODE",
        ) as fx:
            assert not fx.is_closed
            assert fx.http_request.headers.get("X-Stainless-Lang") == "python"

            assert fx.json() == {"foo": "bar"}
            assert cast(Any, fx.is_closed) is True
            assert isinstance(fx, StreamedBinaryAPIResponse)

        assert cast(Any, fx.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.fx.with_raw_response.retrieve(
                to_currency_code="TO_CURRENCY_CODE",
                bank_id="",
                from_currency_code="FROM_CURRENCY_CODE",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `from_currency_code` but received ''"):
            client.banks.fx.with_raw_response.retrieve(
                to_currency_code="TO_CURRENCY_CODE",
                bank_id="BANK_ID",
                from_currency_code="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `to_currency_code` but received ''"):
            client.banks.fx.with_raw_response.retrieve(
                to_currency_code="",
                bank_id="BANK_ID",
                from_currency_code="FROM_CURRENCY_CODE",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/fx").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        fx = client.banks.fx.update(
            bank_id="BANK_ID",
            body={},
        )
        assert fx.is_closed
        assert fx.json() == {"foo": "bar"}
        assert cast(Any, fx.is_closed) is True
        assert isinstance(fx, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/fx").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        fx = client.banks.fx.with_raw_response.update(
            bank_id="BANK_ID",
            body={},
        )

        assert fx.is_closed is True
        assert fx.http_request.headers.get("X-Stainless-Lang") == "python"
        assert fx.json() == {"foo": "bar"}
        assert isinstance(fx, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/fx").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.fx.with_streaming_response.update(
            bank_id="BANK_ID",
            body={},
        ) as fx:
            assert not fx.is_closed
            assert fx.http_request.headers.get("X-Stainless-Lang") == "python"

            assert fx.json() == {"foo": "bar"}
            assert cast(Any, fx.is_closed) is True
            assert isinstance(fx, StreamedBinaryAPIResponse)

        assert cast(Any, fx.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.fx.with_raw_response.update(
                bank_id="",
                body={},
            )


class TestAsyncFx:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/fx/FROM_CURRENCY_CODE/TO_CURRENCY_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        fx = await async_client.banks.fx.retrieve(
            to_currency_code="TO_CURRENCY_CODE",
            bank_id="BANK_ID",
            from_currency_code="FROM_CURRENCY_CODE",
        )
        assert fx.is_closed
        assert await fx.json() == {"foo": "bar"}
        assert cast(Any, fx.is_closed) is True
        assert isinstance(fx, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/fx/FROM_CURRENCY_CODE/TO_CURRENCY_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        fx = await async_client.banks.fx.with_raw_response.retrieve(
            to_currency_code="TO_CURRENCY_CODE",
            bank_id="BANK_ID",
            from_currency_code="FROM_CURRENCY_CODE",
        )

        assert fx.is_closed is True
        assert fx.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await fx.json() == {"foo": "bar"}
        assert isinstance(fx, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/fx/FROM_CURRENCY_CODE/TO_CURRENCY_CODE").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.fx.with_streaming_response.retrieve(
            to_currency_code="TO_CURRENCY_CODE",
            bank_id="BANK_ID",
            from_currency_code="FROM_CURRENCY_CODE",
        ) as fx:
            assert not fx.is_closed
            assert fx.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await fx.json() == {"foo": "bar"}
            assert cast(Any, fx.is_closed) is True
            assert isinstance(fx, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, fx.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.fx.with_raw_response.retrieve(
                to_currency_code="TO_CURRENCY_CODE",
                bank_id="",
                from_currency_code="FROM_CURRENCY_CODE",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `from_currency_code` but received ''"):
            await async_client.banks.fx.with_raw_response.retrieve(
                to_currency_code="TO_CURRENCY_CODE",
                bank_id="BANK_ID",
                from_currency_code="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `to_currency_code` but received ''"):
            await async_client.banks.fx.with_raw_response.retrieve(
                to_currency_code="",
                bank_id="BANK_ID",
                from_currency_code="FROM_CURRENCY_CODE",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/fx").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        fx = await async_client.banks.fx.update(
            bank_id="BANK_ID",
            body={},
        )
        assert fx.is_closed
        assert await fx.json() == {"foo": "bar"}
        assert cast(Any, fx.is_closed) is True
        assert isinstance(fx, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/fx").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        fx = await async_client.banks.fx.with_raw_response.update(
            bank_id="BANK_ID",
            body={},
        )

        assert fx.is_closed is True
        assert fx.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await fx.json() == {"foo": "bar"}
        assert isinstance(fx, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/fx").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.fx.with_streaming_response.update(
            bank_id="BANK_ID",
            body={},
        ) as fx:
            assert not fx.is_closed
            assert fx.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await fx.json() == {"foo": "bar"}
            assert cast(Any, fx.is_closed) is True
            assert isinstance(fx, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, fx.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.fx.with_raw_response.update(
                bank_id="",
                body={},
            )
