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


class TestCustomerAccountLinks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_account_link = client.customer_account_links.create(
            bank_id="BANK_ID",
            body={},
        )
        assert customer_account_link.is_closed
        assert customer_account_link.json() == {"foo": "bar"}
        assert cast(Any, customer_account_link.is_closed) is True
        assert isinstance(customer_account_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_account_link = client.customer_account_links.with_raw_response.create(
            bank_id="BANK_ID",
            body={},
        )

        assert customer_account_link.is_closed is True
        assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert customer_account_link.json() == {"foo": "bar"}
        assert isinstance(customer_account_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customer_account_links.with_streaming_response.create(
            bank_id="BANK_ID",
            body={},
        ) as customer_account_link:
            assert not customer_account_link.is_closed
            assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert customer_account_link.json() == {"foo": "bar"}
            assert cast(Any, customer_account_link.is_closed) is True
            assert isinstance(customer_account_link, StreamedBinaryAPIResponse)

        assert cast(Any, customer_account_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customer_account_links.with_raw_response.create(
                bank_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_account_link = client.customer_account_links.retrieve(
            "BANK_ID",
        )
        assert customer_account_link.is_closed
        assert customer_account_link.json() == {"foo": "bar"}
        assert cast(Any, customer_account_link.is_closed) is True
        assert isinstance(customer_account_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_account_link = client.customer_account_links.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert customer_account_link.is_closed is True
        assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert customer_account_link.json() == {"foo": "bar"}
        assert isinstance(customer_account_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customer_account_links.with_streaming_response.retrieve(
            "BANK_ID",
        ) as customer_account_link:
            assert not customer_account_link.is_closed
            assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert customer_account_link.json() == {"foo": "bar"}
            assert cast(Any, customer_account_link.is_closed) is True
            assert isinstance(customer_account_link, StreamedBinaryAPIResponse)

        assert cast(Any, customer_account_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customer_account_links.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_account_link = client.customer_account_links.update(
            bank_id="BANK_ID",
            body={},
        )
        assert customer_account_link.is_closed
        assert customer_account_link.json() == {"foo": "bar"}
        assert cast(Any, customer_account_link.is_closed) is True
        assert isinstance(customer_account_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_account_link = client.customer_account_links.with_raw_response.update(
            bank_id="BANK_ID",
            body={},
        )

        assert customer_account_link.is_closed is True
        assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert customer_account_link.json() == {"foo": "bar"}
        assert isinstance(customer_account_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customer_account_links.with_streaming_response.update(
            bank_id="BANK_ID",
            body={},
        ) as customer_account_link:
            assert not customer_account_link.is_closed
            assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert customer_account_link.json() == {"foo": "bar"}
            assert cast(Any, customer_account_link.is_closed) is True
            assert isinstance(customer_account_link, StreamedBinaryAPIResponse)

        assert cast(Any, customer_account_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customer_account_links.with_raw_response.update(
                bank_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_account_link = client.customer_account_links.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        )
        assert customer_account_link.is_closed
        assert customer_account_link.json() == {"foo": "bar"}
        assert cast(Any, customer_account_link.is_closed) is True
        assert isinstance(customer_account_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_account_link = client.customer_account_links.with_raw_response.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        )

        assert customer_account_link.is_closed is True
        assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert customer_account_link.json() == {"foo": "bar"}
        assert isinstance(customer_account_link, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customer_account_links.with_streaming_response.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        ) as customer_account_link:
            assert not customer_account_link.is_closed
            assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert customer_account_link.json() == {"foo": "bar"}
            assert cast(Any, customer_account_link.is_closed) is True
            assert isinstance(customer_account_link, StreamedBinaryAPIResponse)

        assert cast(Any, customer_account_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customer_account_links.with_raw_response.list(
                account_id="ACCOUNT_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.customer_account_links.with_raw_response.list(
                account_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        customer_account_link = client.customer_account_links.delete(
            "BANK_ID",
        )
        assert customer_account_link is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.customer_account_links.with_raw_response.delete(
            "BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        customer_account_link = response.parse()
        assert customer_account_link is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.customer_account_links.with_streaming_response.delete(
            "BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            customer_account_link = response.parse()
            assert customer_account_link is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customer_account_links.with_raw_response.delete(
                "",
            )


class TestAsyncCustomerAccountLinks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_account_link = await async_client.customer_account_links.create(
            bank_id="BANK_ID",
            body={},
        )
        assert customer_account_link.is_closed
        assert await customer_account_link.json() == {"foo": "bar"}
        assert cast(Any, customer_account_link.is_closed) is True
        assert isinstance(customer_account_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_account_link = await async_client.customer_account_links.with_raw_response.create(
            bank_id="BANK_ID",
            body={},
        )

        assert customer_account_link.is_closed is True
        assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await customer_account_link.json() == {"foo": "bar"}
        assert isinstance(customer_account_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customer_account_links.with_streaming_response.create(
            bank_id="BANK_ID",
            body={},
        ) as customer_account_link:
            assert not customer_account_link.is_closed
            assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await customer_account_link.json() == {"foo": "bar"}
            assert cast(Any, customer_account_link.is_closed) is True
            assert isinstance(customer_account_link, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, customer_account_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customer_account_links.with_raw_response.create(
                bank_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_account_link = await async_client.customer_account_links.retrieve(
            "BANK_ID",
        )
        assert customer_account_link.is_closed
        assert await customer_account_link.json() == {"foo": "bar"}
        assert cast(Any, customer_account_link.is_closed) is True
        assert isinstance(customer_account_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_account_link = await async_client.customer_account_links.with_raw_response.retrieve(
            "BANK_ID",
        )

        assert customer_account_link.is_closed is True
        assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await customer_account_link.json() == {"foo": "bar"}
        assert isinstance(customer_account_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customer_account_links.with_streaming_response.retrieve(
            "BANK_ID",
        ) as customer_account_link:
            assert not customer_account_link.is_closed
            assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await customer_account_link.json() == {"foo": "bar"}
            assert cast(Any, customer_account_link.is_closed) is True
            assert isinstance(customer_account_link, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, customer_account_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customer_account_links.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_account_link = await async_client.customer_account_links.update(
            bank_id="BANK_ID",
            body={},
        )
        assert customer_account_link.is_closed
        assert await customer_account_link.json() == {"foo": "bar"}
        assert cast(Any, customer_account_link.is_closed) is True
        assert isinstance(customer_account_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_account_link = await async_client.customer_account_links.with_raw_response.update(
            bank_id="BANK_ID",
            body={},
        )

        assert customer_account_link.is_closed is True
        assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await customer_account_link.json() == {"foo": "bar"}
        assert isinstance(customer_account_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customer_account_links.with_streaming_response.update(
            bank_id="BANK_ID",
            body={},
        ) as customer_account_link:
            assert not customer_account_link.is_closed
            assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await customer_account_link.json() == {"foo": "bar"}
            assert cast(Any, customer_account_link.is_closed) is True
            assert isinstance(customer_account_link, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, customer_account_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customer_account_links.with_raw_response.update(
                bank_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        customer_account_link = await async_client.customer_account_links.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        )
        assert customer_account_link.is_closed
        assert await customer_account_link.json() == {"foo": "bar"}
        assert cast(Any, customer_account_link.is_closed) is True
        assert isinstance(customer_account_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        customer_account_link = await async_client.customer_account_links.with_raw_response.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        )

        assert customer_account_link.is_closed is True
        assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await customer_account_link.json() == {"foo": "bar"}
        assert isinstance(customer_account_link, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/accounts/ACCOUNT_ID/customer-account-links").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customer_account_links.with_streaming_response.list(
            account_id="ACCOUNT_ID",
            bank_id="BANK_ID",
        ) as customer_account_link:
            assert not customer_account_link.is_closed
            assert customer_account_link.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await customer_account_link.json() == {"foo": "bar"}
            assert cast(Any, customer_account_link.is_closed) is True
            assert isinstance(customer_account_link, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, customer_account_link.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customer_account_links.with_raw_response.list(
                account_id="ACCOUNT_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.customer_account_links.with_raw_response.list(
                account_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        customer_account_link = await async_client.customer_account_links.delete(
            "BANK_ID",
        )
        assert customer_account_link is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.customer_account_links.with_raw_response.delete(
            "BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        customer_account_link = await response.parse()
        assert customer_account_link is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.customer_account_links.with_streaming_response.delete(
            "BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            customer_account_link = await response.parse()
            assert customer_account_link is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customer_account_links.with_raw_response.delete(
                "",
            )
