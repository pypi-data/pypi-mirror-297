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


class TestLimits:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        limit = client.accounts.views.counterparties.limits.create(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert limit.is_closed
        assert limit.json() == {"foo": "bar"}
        assert cast(Any, limit.is_closed) is True
        assert isinstance(limit, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        limit = client.accounts.views.counterparties.limits.with_raw_response.create(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert limit.is_closed is True
        assert limit.http_request.headers.get("X-Stainless-Lang") == "python"
        assert limit.json() == {"foo": "bar"}
        assert isinstance(limit, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.accounts.views.counterparties.limits.with_streaming_response.create(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as limit:
            assert not limit.is_closed
            assert limit.http_request.headers.get("X-Stainless-Lang") == "python"

            assert limit.json() == {"foo": "bar"}
            assert cast(Any, limit.is_closed) is True
            assert isinstance(limit, StreamedBinaryAPIResponse)

        assert cast(Any, limit.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.create(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.create(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.create(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `counterparty_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.create(
                counterparty_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        limit = client.accounts.views.counterparties.limits.retrieve(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert limit.is_closed
        assert limit.json() == {"foo": "bar"}
        assert cast(Any, limit.is_closed) is True
        assert isinstance(limit, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        limit = client.accounts.views.counterparties.limits.with_raw_response.retrieve(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert limit.is_closed is True
        assert limit.http_request.headers.get("X-Stainless-Lang") == "python"
        assert limit.json() == {"foo": "bar"}
        assert isinstance(limit, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.accounts.views.counterparties.limits.with_streaming_response.retrieve(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as limit:
            assert not limit.is_closed
            assert limit.http_request.headers.get("X-Stainless-Lang") == "python"

            assert limit.json() == {"foo": "bar"}
            assert cast(Any, limit.is_closed) is True
            assert isinstance(limit, StreamedBinaryAPIResponse)

        assert cast(Any, limit.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.retrieve(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.retrieve(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.retrieve(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `counterparty_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.retrieve(
                counterparty_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        limit = client.accounts.views.counterparties.limits.update(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert limit.is_closed
        assert limit.json() == {"foo": "bar"}
        assert cast(Any, limit.is_closed) is True
        assert isinstance(limit, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        limit = client.accounts.views.counterparties.limits.with_raw_response.update(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert limit.is_closed is True
        assert limit.http_request.headers.get("X-Stainless-Lang") == "python"
        assert limit.json() == {"foo": "bar"}
        assert isinstance(limit, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.accounts.views.counterparties.limits.with_streaming_response.update(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as limit:
            assert not limit.is_closed
            assert limit.http_request.headers.get("X-Stainless-Lang") == "python"

            assert limit.json() == {"foo": "bar"}
            assert cast(Any, limit.is_closed) is True
            assert isinstance(limit, StreamedBinaryAPIResponse)

        assert cast(Any, limit.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.update(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.update(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.update(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `counterparty_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.update(
                counterparty_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        limit = client.accounts.views.counterparties.limits.delete(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert limit is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.accounts.views.counterparties.limits.with_raw_response.delete(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        limit = response.parse()
        assert limit is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.accounts.views.counterparties.limits.with_streaming_response.delete(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            limit = response.parse()
            assert limit is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.delete(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.delete(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.delete(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `counterparty_id` but received ''"):
            client.accounts.views.counterparties.limits.with_raw_response.delete(
                counterparty_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )


class TestAsyncLimits:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        limit = await async_client.accounts.views.counterparties.limits.create(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert limit.is_closed
        assert await limit.json() == {"foo": "bar"}
        assert cast(Any, limit.is_closed) is True
        assert isinstance(limit, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        limit = await async_client.accounts.views.counterparties.limits.with_raw_response.create(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert limit.is_closed is True
        assert limit.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await limit.json() == {"foo": "bar"}
        assert isinstance(limit, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.accounts.views.counterparties.limits.with_streaming_response.create(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as limit:
            assert not limit.is_closed
            assert limit.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await limit.json() == {"foo": "bar"}
            assert cast(Any, limit.is_closed) is True
            assert isinstance(limit, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, limit.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.create(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.create(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.create(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `counterparty_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.create(
                counterparty_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        limit = await async_client.accounts.views.counterparties.limits.retrieve(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert limit.is_closed
        assert await limit.json() == {"foo": "bar"}
        assert cast(Any, limit.is_closed) is True
        assert isinstance(limit, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        limit = await async_client.accounts.views.counterparties.limits.with_raw_response.retrieve(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert limit.is_closed is True
        assert limit.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await limit.json() == {"foo": "bar"}
        assert isinstance(limit, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.accounts.views.counterparties.limits.with_streaming_response.retrieve(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as limit:
            assert not limit.is_closed
            assert limit.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await limit.json() == {"foo": "bar"}
            assert cast(Any, limit.is_closed) is True
            assert isinstance(limit, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, limit.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.retrieve(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.retrieve(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.retrieve(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `counterparty_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.retrieve(
                counterparty_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        limit = await async_client.accounts.views.counterparties.limits.update(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert limit.is_closed
        assert await limit.json() == {"foo": "bar"}
        assert cast(Any, limit.is_closed) is True
        assert isinstance(limit, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        limit = await async_client.accounts.views.counterparties.limits.with_raw_response.update(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert limit.is_closed is True
        assert limit.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await limit.json() == {"foo": "bar"}
        assert isinstance(limit, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/counterparties/COUNTERPARTY_ID/limits"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.accounts.views.counterparties.limits.with_streaming_response.update(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as limit:
            assert not limit.is_closed
            assert limit.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await limit.json() == {"foo": "bar"}
            assert cast(Any, limit.is_closed) is True
            assert isinstance(limit, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, limit.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.update(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.update(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.update(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `counterparty_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.update(
                counterparty_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        limit = await async_client.accounts.views.counterparties.limits.delete(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert limit is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.accounts.views.counterparties.limits.with_raw_response.delete(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        limit = await response.parse()
        assert limit is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.accounts.views.counterparties.limits.with_streaming_response.delete(
            counterparty_id="COUNTERPARTY_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            limit = await response.parse()
            assert limit is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.delete(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.delete(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.delete(
                counterparty_id="COUNTERPARTY_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `counterparty_id` but received ''"):
            await async_client.accounts.views.counterparties.limits.with_raw_response.delete(
                counterparty_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )
