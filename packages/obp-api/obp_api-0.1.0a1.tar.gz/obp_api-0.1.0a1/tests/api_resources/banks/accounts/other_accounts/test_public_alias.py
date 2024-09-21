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


class TestPublicAlias:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        public_alias = client.banks.accounts.other_accounts.public_alias.create(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert public_alias.is_closed
        assert public_alias.json() == {"foo": "bar"}
        assert cast(Any, public_alias.is_closed) is True
        assert isinstance(public_alias, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        public_alias = client.banks.accounts.other_accounts.public_alias.with_raw_response.create(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert public_alias.is_closed is True
        assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"
        assert public_alias.json() == {"foo": "bar"}
        assert isinstance(public_alias, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.accounts.other_accounts.public_alias.with_streaming_response.create(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as public_alias:
            assert not public_alias.is_closed
            assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"

            assert public_alias.json() == {"foo": "bar"}
            assert cast(Any, public_alias.is_closed) is True
            assert isinstance(public_alias, StreamedBinaryAPIResponse)

        assert cast(Any, public_alias.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.create(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.create(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.create(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.create(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        public_alias = client.banks.accounts.other_accounts.public_alias.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert public_alias.is_closed
        assert public_alias.json() == {"foo": "bar"}
        assert cast(Any, public_alias.is_closed) is True
        assert isinstance(public_alias, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        public_alias = client.banks.accounts.other_accounts.public_alias.with_raw_response.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert public_alias.is_closed is True
        assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"
        assert public_alias.json() == {"foo": "bar"}
        assert isinstance(public_alias, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.accounts.other_accounts.public_alias.with_streaming_response.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as public_alias:
            assert not public_alias.is_closed
            assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"

            assert public_alias.json() == {"foo": "bar"}
            assert cast(Any, public_alias.is_closed) is True
            assert isinstance(public_alias, StreamedBinaryAPIResponse)

        assert cast(Any, public_alias.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.retrieve(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        public_alias = client.banks.accounts.other_accounts.public_alias.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert public_alias.is_closed
        assert public_alias.json() == {"foo": "bar"}
        assert cast(Any, public_alias.is_closed) is True
        assert isinstance(public_alias, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        public_alias = client.banks.accounts.other_accounts.public_alias.with_raw_response.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert public_alias.is_closed is True
        assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"
        assert public_alias.json() == {"foo": "bar"}
        assert isinstance(public_alias, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.accounts.other_accounts.public_alias.with_streaming_response.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as public_alias:
            assert not public_alias.is_closed
            assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"

            assert public_alias.json() == {"foo": "bar"}
            assert cast(Any, public_alias.is_closed) is True
            assert isinstance(public_alias, StreamedBinaryAPIResponse)

        assert cast(Any, public_alias.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.update(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        public_alias = client.banks.accounts.other_accounts.public_alias.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert public_alias.is_closed
        assert public_alias.json() == {"foo": "bar"}
        assert cast(Any, public_alias.is_closed) is True
        assert isinstance(public_alias, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        public_alias = client.banks.accounts.other_accounts.public_alias.with_raw_response.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert public_alias.is_closed is True
        assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"
        assert public_alias.json() == {"foo": "bar"}
        assert isinstance(public_alias, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.accounts.other_accounts.public_alias.with_streaming_response.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as public_alias:
            assert not public_alias.is_closed
            assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"

            assert public_alias.json() == {"foo": "bar"}
            assert cast(Any, public_alias.is_closed) is True
            assert isinstance(public_alias, StreamedBinaryAPIResponse)

        assert cast(Any, public_alias.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            client.banks.accounts.other_accounts.public_alias.with_raw_response.delete(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )


class TestAsyncPublicAlias:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        public_alias = await async_client.banks.accounts.other_accounts.public_alias.create(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert public_alias.is_closed
        assert await public_alias.json() == {"foo": "bar"}
        assert cast(Any, public_alias.is_closed) is True
        assert isinstance(public_alias, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        public_alias = await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.create(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert public_alias.is_closed is True
        assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await public_alias.json() == {"foo": "bar"}
        assert isinstance(public_alias, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.accounts.other_accounts.public_alias.with_streaming_response.create(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as public_alias:
            assert not public_alias.is_closed
            assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await public_alias.json() == {"foo": "bar"}
            assert cast(Any, public_alias.is_closed) is True
            assert isinstance(public_alias, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, public_alias.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.create(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.create(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.create(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.create(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        public_alias = await async_client.banks.accounts.other_accounts.public_alias.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )
        assert public_alias.is_closed
        assert await public_alias.json() == {"foo": "bar"}
        assert cast(Any, public_alias.is_closed) is True
        assert isinstance(public_alias, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        public_alias = await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        )

        assert public_alias.is_closed is True
        assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await public_alias.json() == {"foo": "bar"}
        assert isinstance(public_alias, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.accounts.other_accounts.public_alias.with_streaming_response.retrieve(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
        ) as public_alias:
            assert not public_alias.is_closed
            assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await public_alias.json() == {"foo": "bar"}
            assert cast(Any, public_alias.is_closed) is True
            assert isinstance(public_alias, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, public_alias.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.retrieve(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.retrieve(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        public_alias = await async_client.banks.accounts.other_accounts.public_alias.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert public_alias.is_closed
        assert await public_alias.json() == {"foo": "bar"}
        assert cast(Any, public_alias.is_closed) is True
        assert isinstance(public_alias, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        public_alias = await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert public_alias.is_closed is True
        assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await public_alias.json() == {"foo": "bar"}
        assert isinstance(public_alias, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.accounts.other_accounts.public_alias.with_streaming_response.update(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as public_alias:
            assert not public_alias.is_closed
            assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await public_alias.json() == {"foo": "bar"}
            assert cast(Any, public_alias.is_closed) is True
            assert isinstance(public_alias, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, public_alias.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.update(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.update(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        public_alias = await async_client.banks.accounts.other_accounts.public_alias.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )
        assert public_alias.is_closed
        assert await public_alias.json() == {"foo": "bar"}
        assert cast(Any, public_alias.is_closed) is True
        assert isinstance(public_alias, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        public_alias = await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        )

        assert public_alias.is_closed is True
        assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await public_alias.json() == {"foo": "bar"}
        assert isinstance(public_alias, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete(
            "/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/VIEW_ID/other_accounts/OTHER_ACCOUNT_ID/public_alias"
        ).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.accounts.other_accounts.public_alias.with_streaming_response.delete(
            other_account_id="OTHER_ACCOUNT_ID",
            bank_id="BANK_ID",
            account_id="ACCOUNT_ID",
            view_id="VIEW_ID",
            body={},
        ) as public_alias:
            assert not public_alias.is_closed
            assert public_alias.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await public_alias.json() == {"foo": "bar"}
            assert cast(Any, public_alias.is_closed) is True
            assert isinstance(public_alias, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, public_alias.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="",
                view_id="VIEW_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `view_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.delete(
                other_account_id="OTHER_ACCOUNT_ID",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `other_account_id` but received ''"):
            await async_client.banks.accounts.other_accounts.public_alias.with_raw_response.delete(
                other_account_id="",
                bank_id="BANK_ID",
                account_id="ACCOUNT_ID",
                view_id="VIEW_ID",
                body={},
            )
