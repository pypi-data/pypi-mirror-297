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


class TestTargetViews:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        target_view = client.accounts.views.target_views.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert target_view.is_closed
        assert target_view.json() == {"foo": "bar"}
        assert cast(Any, target_view.is_closed) is True
        assert isinstance(target_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        target_view = client.accounts.views.target_views.with_raw_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert target_view.is_closed is True
        assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert target_view.json() == {"foo": "bar"}
        assert isinstance(target_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.accounts.views.target_views.with_streaming_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as target_view:
            assert not target_view.is_closed
            assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert target_view.json() == {"foo": "bar"}
            assert cast(Any, target_view.is_closed) is True
            assert isinstance(target_view, StreamedBinaryAPIResponse)

        assert cast(Any, target_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.create(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        target_view = client.accounts.views.target_views.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert target_view.is_closed
        assert target_view.json() == {"foo": "bar"}
        assert cast(Any, target_view.is_closed) is True
        assert isinstance(target_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        target_view = client.accounts.views.target_views.with_raw_response.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert target_view.is_closed is True
        assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert target_view.json() == {"foo": "bar"}
        assert isinstance(target_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.accounts.views.target_views.with_streaming_response.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as target_view:
            assert not target_view.is_closed
            assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert target_view.json() == {"foo": "bar"}
            assert cast(Any, target_view.is_closed) is True
            assert isinstance(target_view, StreamedBinaryAPIResponse)

        assert cast(Any, target_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.retrieve(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.retrieve(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.retrieve(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        target_view = client.accounts.views.target_views.update(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert target_view.is_closed
        assert target_view.json() == {"foo": "bar"}
        assert cast(Any, target_view.is_closed) is True
        assert isinstance(target_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        target_view = client.accounts.views.target_views.with_raw_response.update(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert target_view.is_closed is True
        assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert target_view.json() == {"foo": "bar"}
        assert isinstance(target_view, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.accounts.views.target_views.with_streaming_response.update(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as target_view:
            assert not target_view.is_closed
            assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert target_view.json() == {"foo": "bar"}
            assert cast(Any, target_view.is_closed) is True
            assert isinstance(target_view, StreamedBinaryAPIResponse)

        assert cast(Any, target_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.update(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.update(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.update(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        target_view = client.accounts.views.target_views.delete(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert target_view is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.accounts.views.target_views.with_raw_response.delete(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        target_view = response.parse()
        assert target_view is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.accounts.views.target_views.with_streaming_response.delete(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            target_view = response.parse()
            assert target_view is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.delete(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.delete(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.accounts.views.target_views.with_raw_response.delete(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )


class TestAsyncTargetViews:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        target_view = await async_client.accounts.views.target_views.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert target_view.is_closed
        assert await target_view.json() == {"foo": "bar"}
        assert cast(Any, target_view.is_closed) is True
        assert isinstance(target_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        target_view = await async_client.accounts.views.target_views.with_raw_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert target_view.is_closed is True
        assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await target_view.json() == {"foo": "bar"}
        assert isinstance(target_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.accounts.views.target_views.with_streaming_response.create(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as target_view:
            assert not target_view.is_closed
            assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await target_view.json() == {"foo": "bar"}
            assert cast(Any, target_view.is_closed) is True
            assert isinstance(target_view, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, target_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.create(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.create(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        target_view = await async_client.accounts.views.target_views.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert target_view.is_closed
        assert await target_view.json() == {"foo": "bar"}
        assert cast(Any, target_view.is_closed) is True
        assert isinstance(target_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        target_view = await async_client.accounts.views.target_views.with_raw_response.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert target_view.is_closed is True
        assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await target_view.json() == {"foo": "bar"}
        assert isinstance(target_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.accounts.views.target_views.with_streaming_response.retrieve(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as target_view:
            assert not target_view.is_closed
            assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await target_view.json() == {"foo": "bar"}
            assert cast(Any, target_view.is_closed) is True
            assert isinstance(target_view, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, target_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.retrieve(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.retrieve(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.retrieve(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        target_view = await async_client.accounts.views.target_views.update(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )
        assert target_view.is_closed
        assert await target_view.json() == {"foo": "bar"}
        assert cast(Any, target_view.is_closed) is True
        assert isinstance(target_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        target_view = await async_client.accounts.views.target_views.with_raw_response.update(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        )

        assert target_view.is_closed is True
        assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await target_view.json() == {"foo": "bar"}
        assert isinstance(target_view, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/views/VIEW_ID/target-views/TARGET_VIEW_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.accounts.views.target_views.with_streaming_response.update(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            body={},
        ) as target_view:
            assert not target_view.is_closed
            assert target_view.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await target_view.json() == {"foo": "bar"}
            assert cast(Any, target_view.is_closed) is True
            assert isinstance(target_view, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, target_view.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.update(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.update(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.update(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                body={},
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        target_view = await async_client.accounts.views.target_views.delete(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )
        assert target_view is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.accounts.views.target_views.with_raw_response.delete(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        target_view = await response.parse()
        assert target_view is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.accounts.views.target_views.with_streaming_response.delete(
            view_id="VIEW_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            target_view = await response.parse()
            assert target_view is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.delete(
                view_id="VIEW_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.delete(
                view_id="VIEW_ID",
                bank_id="BANK_ID",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.accounts.views.target_views.with_raw_response.delete(
                view_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
            )
