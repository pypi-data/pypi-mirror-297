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


class TestConsents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = client.consents.retrieve(
            "CONSENT_ID",
        )
        assert consent.is_closed
        assert consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = client.consents.with_raw_response.retrieve(
            "CONSENT_ID",
        )

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consent.json() == {"foo": "bar"}
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consents.with_streaming_response.retrieve(
            "CONSENT_ID",
        ) as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, StreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            client.consents.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_challenge(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/challenge").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = client.consents.challenge(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert consent.is_closed
        assert consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_challenge(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/challenge").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = client.consents.with_raw_response.challenge(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consent.json() == {"foo": "bar"}
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_challenge(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/challenge").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consents.with_streaming_response.challenge(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        ) as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, StreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_challenge(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.consents.with_raw_response.challenge(
                consent_id="CONSENT_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            client.consents.with_raw_response.challenge(
                consent_id="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_revoke(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = client.consents.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        )
        assert consent.is_closed
        assert consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_revoke(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = client.consents.with_raw_response.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        )

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consent.json() == {"foo": "bar"}
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_revoke(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consents.with_streaming_response.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        ) as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, StreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_revoke(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.consents.with_raw_response.revoke(
                consent_id="CONSENT_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            client.consents.with_raw_response.revoke(
                consent_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_user_update_request(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/user-update-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = client.consents.user_update_request(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert consent.is_closed
        assert consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_user_update_request(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/user-update-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = client.consents.with_raw_response.user_update_request(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consent.json() == {"foo": "bar"}
        assert isinstance(consent, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_user_update_request(self, client: ObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/user-update-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.consents.with_streaming_response.user_update_request(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        ) as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, StreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_user_update_request(self, client: ObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            client.consents.with_raw_response.user_update_request(
                consent_id="CONSENT_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            client.consents.with_raw_response.user_update_request(
                consent_id="",
                bank_id="BANK_ID",
                body={},
            )


class TestAsyncConsents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = await async_client.consents.retrieve(
            "CONSENT_ID",
        )
        assert consent.is_closed
        assert await consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = await async_client.consents.with_raw_response.retrieve(
            "CONSENT_ID",
        )

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consent.json() == {"foo": "bar"}
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.get("/obp/v5.1.0/consumer/current/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consents.with_streaming_response.retrieve(
            "CONSENT_ID",
        ) as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            await async_client.consents.with_raw_response.retrieve(
                "",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_challenge(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/challenge").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = await async_client.consents.challenge(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert consent.is_closed
        assert await consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_challenge(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/challenge").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = await async_client.consents.with_raw_response.challenge(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consent.json() == {"foo": "bar"}
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_challenge(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.post("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/challenge").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consents.with_streaming_response.challenge(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        ) as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_challenge(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.consents.with_raw_response.challenge(
                consent_id="CONSENT_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            await async_client.consents.with_raw_response.challenge(
                consent_id="",
                bank_id="BANK_ID",
                body={},
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_revoke(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = await async_client.consents.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        )
        assert consent.is_closed
        assert await consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_revoke(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = await async_client.consents.with_raw_response.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        )

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consent.json() == {"foo": "bar"}
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_revoke(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.delete("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consents.with_streaming_response.revoke(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
        ) as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_revoke(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.consents.with_raw_response.revoke(
                consent_id="CONSENT_ID",
                bank_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            await async_client.consents.with_raw_response.revoke(
                consent_id="",
                bank_id="BANK_ID",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_user_update_request(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/user-update-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        consent = await async_client.consents.user_update_request(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        )
        assert consent.is_closed
        assert await consent.json() == {"foo": "bar"}
        assert cast(Any, consent.is_closed) is True
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_user_update_request(self, async_client: AsyncObpAPI, respx_mock: MockRouter) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/user-update-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        consent = await async_client.consents.with_raw_response.user_update_request(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        )

        assert consent.is_closed is True
        assert consent.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consent.json() == {"foo": "bar"}
        assert isinstance(consent, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_user_update_request(
        self, async_client: AsyncObpAPI, respx_mock: MockRouter
    ) -> None:
        respx_mock.put("/obp/v5.1.0/banks/BANK_ID/consents/CONSENT_ID/user-update-request").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.consents.with_streaming_response.user_update_request(
            consent_id="CONSENT_ID",
            bank_id="BANK_ID",
            body={},
        ) as consent:
            assert not consent.is_closed
            assert consent.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consent.json() == {"foo": "bar"}
            assert cast(Any, consent.is_closed) is True
            assert isinstance(consent, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consent.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_user_update_request(self, async_client: AsyncObpAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bank_id` but received ''"):
            await async_client.consents.with_raw_response.user_update_request(
                consent_id="CONSENT_ID",
                bank_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `consent_id` but received ''"):
            await async_client.consents.with_raw_response.user_update_request(
                consent_id="",
                bank_id="BANK_ID",
                body={},
            )
