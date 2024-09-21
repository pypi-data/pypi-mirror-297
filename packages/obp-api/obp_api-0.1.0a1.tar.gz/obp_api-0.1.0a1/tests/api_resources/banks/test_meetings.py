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


class TestMeetings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/meetings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        meeting = client.banks.meetings.create(
            bank_id="BANK_ID",
            body={},
        )
        assert meeting.is_closed
        assert meeting.json() == {"foo": "bar"}
        assert cast(Any, meeting.is_closed) is True
        assert isinstance(meeting, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/meetings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        meeting = client.banks.meetings.with_raw_response.create(
            bank_id="BANK_ID",
            body={},
        )

        assert meeting.is_closed is True
        assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"
        assert meeting.json() == {"foo": "bar"}
        assert isinstance(meeting, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/meetings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.meetings.with_streaming_response.create(
            bank_id="BANK_ID",
            body={},
        ) as meeting:
            assert not meeting.is_closed
            assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"

            assert meeting.json() == {"foo": "bar"}
            assert cast(Any, meeting.is_closed) is True
            assert isinstance(meeting, StreamedBinaryAPIResponse)

        assert cast(Any, meeting.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_create(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.meetings.with_raw_response.create(
                bank_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings/MEETING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        meeting = client.banks.meetings.retrieve(
            meeting_id="MEETING_ID",
            bank_id="BANK_ID",
        )
        assert meeting.is_closed
        assert meeting.json() == {"foo": "bar"}
        assert cast(Any, meeting.is_closed) is True
        assert isinstance(meeting, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings/MEETING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        meeting = client.banks.meetings.with_raw_response.retrieve(
            meeting_id="MEETING_ID",
            bank_id="BANK_ID",
        )

        assert meeting.is_closed is True
        assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"
        assert meeting.json() == {"foo": "bar"}
        assert isinstance(meeting, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings/MEETING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.banks.meetings.with_streaming_response.retrieve(
            meeting_id="MEETING_ID",
            bank_id="BANK_ID",
        ) as meeting:
            assert not meeting.is_closed
            assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"

            assert meeting.json() == {"foo": "bar"}
            assert cast(Any, meeting.is_closed) is True
            assert isinstance(meeting, StreamedBinaryAPIResponse)

        assert cast(Any, meeting.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.meetings.with_raw_response.retrieve(
                meeting_id="MEETING_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meeting_id` but received ''"):
            client.banks.meetings.with_raw_response.retrieve(
                meeting_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        meeting = client.banks.meetings.list(
            "BANK_ID",
        )
        assert meeting.is_closed
        assert meeting.json() == {"foo": "bar"}
        assert cast(Any, meeting.is_closed) is True
        assert isinstance(meeting, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        meeting = client.banks.meetings.with_raw_response.list(
            "BANK_ID",
        )

        assert meeting.is_closed is True
        assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"
        assert meeting.json() == {"foo": "bar"}
        assert isinstance(meeting, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.banks.meetings.with_streaming_response.list(
            "BANK_ID",
        ) as meeting:
            assert not meeting.is_closed
            assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"

            assert meeting.json() == {"foo": "bar"}
            assert cast(Any, meeting.is_closed) is True
            assert isinstance(meeting, StreamedBinaryAPIResponse)

        assert cast(Any, meeting.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_list(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.banks.meetings.with_raw_response.list(
                "",
            )


class TestAsyncMeetings:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/meetings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        meeting = await async_client.banks.meetings.create(
            bank_id="BANK_ID",
            body={},
        )
        assert meeting.is_closed
        assert await meeting.json() == {"foo": "bar"}
        assert cast(Any, meeting.is_closed) is True
        assert isinstance(meeting, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/meetings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        meeting = await async_client.banks.meetings.with_raw_response.create(
            bank_id="BANK_ID",
            body={},
        )

        assert meeting.is_closed is True
        assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await meeting.json() == {"foo": "bar"}
        assert isinstance(meeting, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/meetings").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.meetings.with_streaming_response.create(
            bank_id="BANK_ID",
            body={},
        ) as meeting:
            assert not meeting.is_closed
            assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await meeting.json() == {"foo": "bar"}
            assert cast(Any, meeting.is_closed) is True
            assert isinstance(meeting, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, meeting.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_create(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.meetings.with_raw_response.create(
                bank_id="",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings/MEETING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        meeting = await async_client.banks.meetings.retrieve(
            meeting_id="MEETING_ID",
            bank_id="BANK_ID",
        )
        assert meeting.is_closed
        assert await meeting.json() == {"foo": "bar"}
        assert cast(Any, meeting.is_closed) is True
        assert isinstance(meeting, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings/MEETING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        meeting = await async_client.banks.meetings.with_raw_response.retrieve(
            meeting_id="MEETING_ID",
            bank_id="BANK_ID",
        )

        assert meeting.is_closed is True
        assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await meeting.json() == {"foo": "bar"}
        assert isinstance(meeting, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings/MEETING_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.banks.meetings.with_streaming_response.retrieve(
            meeting_id="MEETING_ID",
            bank_id="BANK_ID",
        ) as meeting:
            assert not meeting.is_closed
            assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await meeting.json() == {"foo": "bar"}
            assert cast(Any, meeting.is_closed) is True
            assert isinstance(meeting, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, meeting.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.meetings.with_raw_response.retrieve(
                meeting_id="MEETING_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meeting_id` but received ''"):
            await async_client.banks.meetings.with_raw_response.retrieve(
                meeting_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        meeting = await async_client.banks.meetings.list(
            "BANK_ID",
        )
        assert meeting.is_closed
        assert await meeting.json() == {"foo": "bar"}
        assert cast(Any, meeting.is_closed) is True
        assert isinstance(meeting, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        meeting = await async_client.banks.meetings.with_raw_response.list(
            "BANK_ID",
        )

        assert meeting.is_closed is True
        assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await meeting.json() == {"foo": "bar"}
        assert isinstance(meeting, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/banks/BANK_ID/meetings").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.banks.meetings.with_streaming_response.list(
            "BANK_ID",
        ) as meeting:
            assert not meeting.is_closed
            assert meeting.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await meeting.json() == {"foo": "bar"}
            assert cast(Any, meeting.is_closed) is True
            assert isinstance(meeting, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, meeting.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_list(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.banks.meetings.with_raw_response.list(
                "",
            )
