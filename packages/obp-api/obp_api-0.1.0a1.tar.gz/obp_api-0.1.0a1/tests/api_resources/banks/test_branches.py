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


class TestBranches:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/branches").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        branch = client.banks.branches.create(
            bank_id="BANK_ID",
            body={},
        )
        assert branch.is_closed
        assert branch.json() == {"foo": "bar"}
        assert cast(Any, branch.is_closed) is True
        assert isinstance(branch, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/branches").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        branch = client.banks.branches.with_raw_response.create(
            bank_id="BANK_ID",
            body={},
        )

        assert branch.is_closed is True
        assert branch.http_request.headers.get("X-Stainless-Lang") == "python"
        assert branch.json() == {"foo": "bar"}
        assert isinstance(branch, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/branches").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.branches.with_streaming_response.create(
            bank_id="BANK_ID",
            body={},
        ) as branch:
            assert not branch.is_closed
            assert branch.http_request.headers.get("X-Stainless-Lang") == "python"

            assert branch.json() == {"foo": "bar"}
            assert cast(Any, branch.is_closed) is True
            assert isinstance(branch, StreamedBinaryAPIResponse)

        assert cast(Any, branch.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.branches.with_raw_response.create(
                bank_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches/BRANCH_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        branch = client.banks.branches.retrieve(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        )
        assert branch.is_closed
        assert branch.json() == {"foo": "bar"}
        assert cast(Any, branch.is_closed) is True
        assert isinstance(branch, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches/BRANCH_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        branch = client.banks.branches.with_raw_response.retrieve(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        )

        assert branch.is_closed is True
        assert branch.http_request.headers.get("X-Stainless-Lang") == "python"
        assert branch.json() == {"foo": "bar"}
        assert isinstance(branch, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches/BRANCH_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.branches.with_streaming_response.retrieve(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        ) as branch:
            assert not branch.is_closed
            assert branch.http_request.headers.get("X-Stainless-Lang") == "python"

            assert branch.json() == {"foo": "bar"}
            assert cast(Any, branch.is_closed) is True
            assert isinstance(branch, StreamedBinaryAPIResponse)

        assert cast(Any, branch.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.branches.with_raw_response.retrieve(
                branch_id="BRANCH_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `branch_id` but received ''"):
            client.banks.branches.with_raw_response.retrieve(
                branch_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        branch = client.banks.branches.list(
            "BANK_ID",
        )
        assert branch.is_closed
        assert branch.json() == {"foo": "bar"}
        assert cast(Any, branch.is_closed) is True
        assert isinstance(branch, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        branch = client.banks.branches.with_raw_response.list(
            "BANK_ID",
        )

        assert branch.is_closed is True
        assert branch.http_request.headers.get("X-Stainless-Lang") == "python"
        assert branch.json() == {"foo": "bar"}
        assert isinstance(branch, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.branches.with_streaming_response.list(
            "BANK_ID",
        ) as branch:
            assert not branch.is_closed
            assert branch.http_request.headers.get("X-Stainless-Lang") == "python"

            assert branch.json() == {"foo": "bar"}
            assert cast(Any, branch.is_closed) is True
            assert isinstance(branch, StreamedBinaryAPIResponse)

        assert cast(Any, branch.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.branches.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_delete(self, client: ObpAPI) -> None:
        branch = client.banks.branches.delete(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        )
        assert branch is None

    @parametrize
    def test_raw_response_delete(self, client: ObpAPI) -> None:
        response = client.banks.branches.with_raw_response.delete(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        branch = response.parse()
        assert branch is None

    @parametrize
    def test_streaming_response_delete(self, client: ObpAPI) -> None:
        with client.banks.branches.with_streaming_response.delete(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            branch = response.parse()
            assert branch is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.branches.with_raw_response.delete(
                branch_id="BRANCH_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `branch_id` but received ''"):
            client.banks.branches.with_raw_response.delete(
                branch_id="",
                bank_id="BANK_ID",
            )


class TestAsyncBranches:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/branches").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        branch = await async_client.banks.branches.create(
            bank_id="BANK_ID",
            body={},
        )
        assert branch.is_closed
        assert await branch.json() == {"foo": "bar"}
        assert cast(Any, branch.is_closed) is True
        assert isinstance(branch, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/branches").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        branch = await async_client.banks.branches.with_raw_response.create(
            bank_id="BANK_ID",
            body={},
        )

        assert branch.is_closed is True
        assert branch.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await branch.json() == {"foo": "bar"}
        assert isinstance(branch, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/branches").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.branches.with_streaming_response.create(
            bank_id="BANK_ID",
            body={},
        ) as branch:
            assert not branch.is_closed
            assert branch.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await branch.json() == {"foo": "bar"}
            assert cast(Any, branch.is_closed) is True
            assert isinstance(branch, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, branch.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.branches.with_raw_response.create(
                bank_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches/BRANCH_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        branch = await async_client.banks.branches.retrieve(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        )
        assert branch.is_closed
        assert await branch.json() == {"foo": "bar"}
        assert cast(Any, branch.is_closed) is True
        assert isinstance(branch, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches/BRANCH_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        branch = await async_client.banks.branches.with_raw_response.retrieve(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        )

        assert branch.is_closed is True
        assert branch.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await branch.json() == {"foo": "bar"}
        assert isinstance(branch, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches/BRANCH_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.branches.with_streaming_response.retrieve(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        ) as branch:
            assert not branch.is_closed
            assert branch.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await branch.json() == {"foo": "bar"}
            assert cast(Any, branch.is_closed) is True
            assert isinstance(branch, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, branch.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.branches.with_raw_response.retrieve(
                branch_id="BRANCH_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `branch_id` but received ''"):
            await async_client.banks.branches.with_raw_response.retrieve(
                branch_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        branch = await async_client.banks.branches.list(
            "BANK_ID",
        )
        assert branch.is_closed
        assert await branch.json() == {"foo": "bar"}
        assert cast(Any, branch.is_closed) is True
        assert isinstance(branch, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        branch = await async_client.banks.branches.with_raw_response.list(
            "BANK_ID",
        )

        assert branch.is_closed is True
        assert branch.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await branch.json() == {"foo": "bar"}
        assert isinstance(branch, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/branches").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.branches.with_streaming_response.list(
            "BANK_ID",
        ) as branch:
            assert not branch.is_closed
            assert branch.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await branch.json() == {"foo": "bar"}
            assert cast(Any, branch.is_closed) is True
            assert isinstance(branch, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, branch.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.branches.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncObpAPI) -> None:
        branch = await async_client.banks.branches.delete(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        )
        assert branch is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObpAPI) -> None:
        response = await async_client.banks.branches.with_raw_response.delete(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        branch = await response.parse()
        assert branch is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObpAPI) -> None:
        async with async_client.banks.branches.with_streaming_response.delete(
            branch_id="BRANCH_ID",
            bank_id="BANK_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            branch = await response.parse()
            assert branch is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.branches.with_raw_response.delete(
                branch_id="BRANCH_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `branch_id` but received ''"):
            await async_client.banks.branches.with_raw_response.delete(
                branch_id="",
                bank_id="BANK_ID",
            )
