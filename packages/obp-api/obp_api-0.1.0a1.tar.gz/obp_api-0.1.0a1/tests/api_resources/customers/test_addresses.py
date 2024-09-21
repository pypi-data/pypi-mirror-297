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


class TestAddresses:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/address").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        address = client.customers.addresses.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert address.is_closed
        assert address.json() == {"foo": "bar"}
        assert cast(Any, address.is_closed) is True
        assert isinstance(address, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/address").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        address = client.customers.addresses.with_raw_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert address.is_closed is True
        assert address.http_request.headers.get("X-Stainless-Lang") == "python"
        assert address.json() == {"foo": "bar"}
        assert isinstance(address, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/address").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.addresses.with_streaming_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as address:
            assert not address.is_closed
            assert address.http_request.headers.get("X-Stainless-Lang") == "python"

            assert address.json() == {"foo": "bar"}
            assert cast(Any, address.is_closed) is True
            assert isinstance(address, StreamedBinaryAPIResponse)

        assert cast(Any, address.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.addresses.with_raw_response.create(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.addresses.with_raw_response.create(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses/CUSTOMER_ADDRESS_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        address = client.customers.addresses.update(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        )
        assert address.is_closed
        assert address.json() == {"foo": "bar"}
        assert cast(Any, address.is_closed) is True
        assert isinstance(address, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses/CUSTOMER_ADDRESS_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        address = client.customers.addresses.with_raw_response.update(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        )

        assert address.is_closed is True
        assert address.http_request.headers.get("X-Stainless-Lang") == "python"
        assert address.json() == {"foo": "bar"}
        assert isinstance(address, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses/CUSTOMER_ADDRESS_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.addresses.with_streaming_response.update(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        ) as address:
            assert not address.is_closed
            assert address.http_request.headers.get("X-Stainless-Lang") == "python"

            assert address.json() == {"foo": "bar"}
            assert cast(Any, address.is_closed) is True
            assert isinstance(address, StreamedBinaryAPIResponse)

        assert cast(Any, address.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.addresses.with_raw_response.update(
                customer_address_id="CUSTOMER_ADDRESS_ID",
                bank_id="",
                customer_id="CUSTOMER_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.addresses.with_raw_response.update(
                customer_address_id="CUSTOMER_ADDRESS_ID",
                bank_id="BANK_ID",
                customer_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_address_id` but received ''"):
            client.customers.addresses.with_raw_response.update(
                customer_address_id="",
                bank_id="BANK_ID",
                customer_id="CUSTOMER_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        address = client.customers.addresses.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert address.is_closed
        assert address.json() == {"foo": "bar"}
        assert cast(Any, address.is_closed) is True
        assert isinstance(address, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        address = client.customers.addresses.with_raw_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert address.is_closed is True
        assert address.http_request.headers.get("X-Stainless-Lang") == "python"
        assert address.json() == {"foo": "bar"}
        assert isinstance(address, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.customers.addresses.with_streaming_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as address:
            assert not address.is_closed
            assert address.http_request.headers.get("X-Stainless-Lang") == "python"

            assert address.json() == {"foo": "bar"}
            assert cast(Any, address.is_closed) is True
            assert isinstance(address, StreamedBinaryAPIResponse)

        assert cast(Any, address.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.addresses.with_raw_response.list(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.addresses.with_raw_response.list(
                customer_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        address = client.customers.addresses.delete(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        )
        assert address is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.customers.addresses.with_raw_response.delete(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        address = response.parse()
        assert address is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.customers.addresses.with_streaming_response.delete(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            address = response.parse()
            assert address is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.customers.addresses.with_raw_response.delete(
                customer_address_id="CUSTOMER_ADDRESS_ID",
                bank_id="",
                customer_id="CUSTOMER_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.customers.addresses.with_raw_response.delete(
                customer_address_id="CUSTOMER_ADDRESS_ID",
                bank_id="BANK_ID",
                customer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_address_id` but received ''"):
            client.customers.addresses.with_raw_response.delete(
                customer_address_id="",
                bank_id="BANK_ID",
                customer_id="CUSTOMER_ID",
            )


class TestAsyncAddresses:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/address").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        address = await async_client.customers.addresses.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert address.is_closed
        assert await address.json() == {"foo": "bar"}
        assert cast(Any, address.is_closed) is True
        assert isinstance(address, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/address").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        address = await async_client.customers.addresses.with_raw_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert address.is_closed is True
        assert address.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await address.json() == {"foo": "bar"}
        assert isinstance(address, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/address").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.addresses.with_streaming_response.create(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
            body={},
        ) as address:
            assert not address.is_closed
            assert address.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await address.json() == {"foo": "bar"}
            assert cast(Any, address.is_closed) is True
            assert isinstance(address, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, address.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.addresses.with_raw_response.create(
                customer_id="CUSTOMER_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.addresses.with_raw_response.create(
                customer_id="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses/CUSTOMER_ADDRESS_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        address = await async_client.customers.addresses.update(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        )
        assert address.is_closed
        assert await address.json() == {"foo": "bar"}
        assert cast(Any, address.is_closed) is True
        assert isinstance(address, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses/CUSTOMER_ADDRESS_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        address = await async_client.customers.addresses.with_raw_response.update(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        )

        assert address.is_closed is True
        assert address.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await address.json() == {"foo": "bar"}
        assert isinstance(address, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses/CUSTOMER_ADDRESS_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.addresses.with_streaming_response.update(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
            body={},
        ) as address:
            assert not address.is_closed
            assert address.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await address.json() == {"foo": "bar"}
            assert cast(Any, address.is_closed) is True
            assert isinstance(address, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, address.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.addresses.with_raw_response.update(
                customer_address_id="CUSTOMER_ADDRESS_ID",
                bank_id="",
                customer_id="CUSTOMER_ID",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.addresses.with_raw_response.update(
                customer_address_id="CUSTOMER_ADDRESS_ID",
                bank_id="BANK_ID",
                customer_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_address_id` but received ''"):
            await async_client.customers.addresses.with_raw_response.update(
                customer_address_id="",
                bank_id="BANK_ID",
                customer_id="CUSTOMER_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        address = await async_client.customers.addresses.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )
        assert address.is_closed
        assert await address.json() == {"foo": "bar"}
        assert cast(Any, address.is_closed) is True
        assert isinstance(address, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        address = await async_client.customers.addresses.with_raw_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        )

        assert address.is_closed is True
        assert address.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await address.json() == {"foo": "bar"}
        assert isinstance(address, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/customers/CUSTOMER_ID/addresses").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.customers.addresses.with_streaming_response.list(
            customer_id="CUSTOMER_ID",
            bank_id="BANK_ID",
        ) as address:
            assert not address.is_closed
            assert address.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await address.json() == {"foo": "bar"}
            assert cast(Any, address.is_closed) is True
            assert isinstance(address, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, address.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.addresses.with_raw_response.list(
                customer_id="CUSTOMER_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.addresses.with_raw_response.list(
                customer_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        address = await async_client.customers.addresses.delete(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        )
        assert address is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.customers.addresses.with_raw_response.delete(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        address = await response.parse()
        assert address is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.customers.addresses.with_streaming_response.delete(
            customer_address_id="CUSTOMER_ADDRESS_ID",
            bank_id="BANK_ID",
            customer_id="CUSTOMER_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            address = await response.parse()
            assert address is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.customers.addresses.with_raw_response.delete(
                customer_address_id="CUSTOMER_ADDRESS_ID",
                bank_id="",
                customer_id="CUSTOMER_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.customers.addresses.with_raw_response.delete(
                customer_address_id="CUSTOMER_ADDRESS_ID",
                bank_id="BANK_ID",
                customer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_address_id` but received ''"):
            await async_client.customers.addresses.with_raw_response.delete(
                customer_address_id="",
                bank_id="BANK_ID",
                customer_id="CUSTOMER_ID",
            )
