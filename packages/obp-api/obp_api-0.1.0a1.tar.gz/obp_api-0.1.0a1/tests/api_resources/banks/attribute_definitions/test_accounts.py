# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from obp_api import ObpAPI, AsyncObpAPI

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAccounts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: ObpAPI) -> None:
        account = client.banks.attribute_definitions.accounts.retrieve(
            "BANK_ID",
        )
        assert account is None

    @parametrize
    def test_raw_response_retrieve(self, client: ObpAPI) -> None:
        response = client.banks.attribute_definitions.accounts.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert account is None

    @parametrize
    def test_streaming_response_retrieve(self, client: ObpAPI) -> None:
        with client.banks.attribute_definitions.accounts.with_streaming_response.retrieve(
            "BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert account is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.attribute_definitions.accounts.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: ObpAPI) -> None:
        account = client.banks.attribute_definitions.accounts.update(
            "BANK_ID",
        )
        assert account is None

    @parametrize
    def test_raw_response_update(self, client: ObpAPI) -> None:
        response = client.banks.attribute_definitions.accounts.with_raw_response.update(
            "BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert account is None

    @parametrize
    def test_streaming_response_update(self, client: ObpAPI) -> None:
        with client.banks.attribute_definitions.accounts.with_streaming_response.update(
            "BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert account is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.attribute_definitions.accounts.with_raw_response.update(
                "",
            )

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        account = client.banks.attribute_definitions.accounts.delete(
            "BANK_ID",
        )
        assert account is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.banks.attribute_definitions.accounts.with_raw_response.delete(
            "BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert account is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.banks.attribute_definitions.accounts.with_streaming_response.delete(
            "BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert account is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.attribute_definitions.accounts.with_raw_response.delete(
                "",
            )


class TestAsyncAccounts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncObpAPI) -> None:
        account = await async_client.banks.attribute_definitions.accounts.retrieve(
            "BANK_ID",
        )
        assert account is None

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.banks.attribute_definitions.accounts.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert account is None

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI) -> None:
        async with async_client.banks.attribute_definitions.accounts.with_streaming_response.retrieve(
            "BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert account is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.attribute_definitions.accounts.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncObpAPI) -> None:
        account = await async_client.banks.attribute_definitions.accounts.update(
            "BANK_ID",
        )
        assert account is None

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.banks.attribute_definitions.accounts.with_raw_response.update(
            "BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert account is None

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncObpAPI) -> None:
        async with async_client.banks.attribute_definitions.accounts.with_streaming_response.update(
            "BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert account is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.attribute_definitions.accounts.with_raw_response.update(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        account = await async_client.banks.attribute_definitions.accounts.delete(
            "BANK_ID",
        )
        assert account is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.banks.attribute_definitions.accounts.with_raw_response.delete(
            "BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert account is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.banks.attribute_definitions.accounts.with_streaming_response.delete(
            "BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert account is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.attribute_definitions.accounts.with_raw_response.delete(
                "",
            )
