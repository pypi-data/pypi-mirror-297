# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .sms import (
    SMSResource,
    AsyncSMSResource,
    SMSResourceWithRawResponse,
    AsyncSMSResourceWithRawResponse,
    SMSResourceWithStreamingResponse,
    AsyncSMSResourceWithStreamingResponse,
)
from .email import (
    EmailResource,
    AsyncEmailResource,
    EmailResourceWithRawResponse,
    AsyncEmailResourceWithRawResponse,
    EmailResourceWithStreamingResponse,
    AsyncEmailResourceWithStreamingResponse,
)
from ...types import consent_challenge_params, consent_user_update_request_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .implicit import (
    ImplicitResource,
    AsyncImplicitResource,
    ImplicitResourceWithRawResponse,
    AsyncImplicitResourceWithRawResponse,
    ImplicitResourceWithStreamingResponse,
    AsyncImplicitResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["ConsentsResource", "AsyncConsentsResource"]


class ConsentsResource(SyncAPIResource):
    @cached_property
    def email(self) -> EmailResource:
        return EmailResource(self._client)

    @cached_property
    def implicit(self) -> ImplicitResource:
        return ImplicitResource(self._client)

    @cached_property
    def sms(self) -> SMSResource:
        return SMSResource(self._client)

    @cached_property
    def with_raw_response(self) -> ConsentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return ConsentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConsentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return ConsentsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        consent_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>This endpoint gets the Consent By consent id.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not consent_id:
            raise ValueError(f"Expected a non-empty value for `consent_id` but received {consent_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/consumer/current/consents/{consent_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def challenge(
        self,
        consent_id: str,
        *,
        bank_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>An OBP Consent allows the holder of the Consent to call one or more endpoints.</p><p>Consents must be created and authorisied using SCA (Strong Customer Authentication).</p><p>That is, Consents can be created by an authorised User via the OBP REST API but they must be confirmed via an out of band (OOB) mechanism such as a code sent to a mobile phone.</p><p>Each Consent has one of the following states: INITIATED, ACCEPTED, REJECTED, REVOKED, RECEIVED, VALID, REVOKEDBYPSU, EXPIRED, TERMINATEDBYTPP, AUTHORISED, AWAITINGAUTHORISATION.</p><p>Each Consent is bound to a consumer i.e. you need to identify yourself over request header value Consumer-Key.<br />For example:<br />GET /obp/v4.0.0/users/current HTTP/1.1<br />Host: 127.0.0.1:8080<br />Consent-JWT: eyJhbGciOiJIUzI1NiJ9.eyJlbnRpdGxlbWVudHMiOlt7InJvbGVfbmFtZSI6IkNhbkdldEFueVVzZXIiLCJiYW5rX2lkIjoiIn<br />1dLCJjcmVhdGVkQnlVc2VySWQiOiJhYjY1MzlhOS1iMTA1LTQ0ODktYTg4My0wYWQ4ZDZjNjE2NTciLCJzdWIiOiIzNDc1MDEzZi03YmY5LTQyNj<br />EtOWUxYy0xZTdlNWZjZTJlN2UiLCJhdWQiOiI4MTVhMGVmMS00YjZhLTQyMDUtYjExMi1lNDVmZDZmNGQzYWQiLCJuYmYiOjE1ODA3NDE2NjcsIml<br />zcyI6Imh0dHA6XC9cLzEyNy4wLjAuMTo4MDgwIiwiZXhwIjoxNTgwNzQ1MjY3LCJpYXQiOjE1ODA3NDE2NjcsImp0aSI6ImJkYzVjZTk5LTE2ZTY<br />tNDM4Yi1hNjllLTU3MTAzN2RhMTg3OCIsInZpZXdzIjpbXX0.L3fEEEhdCVr3qnmyRKBBUaIQ7dk1VjiFaEBW8hUNjfg</p><p>Consumer-Key: ejznk505d132ryomnhbx1qmtohurbsbb0kijajsk<br />cache-control: no-cache</p><p>Maximum time to live of the token is specified over props value consents.max_time_to_live. In case isn't defined default value is 3600 seconds.</p><p>Example of POST JSON:<br />{<br />&quot;everything&quot;: false,<br />&quot;views&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;account_id&quot;: &quot;8ca8a7e4-6d02-40e3-a129-0b2bf89de9f0&quot;,<br />&quot;view_id&quot;: &quot;owner&quot;<br />}<br />],<br />&quot;entitlements&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;role_name&quot;: &quot;CanGetCustomer&quot;<br />}<br />],<br />&quot;consumer_id&quot;: &quot;7uy8a7e4-6d02-40e3-a129-0b2bf89de8uh&quot;,<br />&quot;email&quot;: &quot;<a href="m&#97;i&#108;&#x74;&#111;&#x3a;&#101;v&#x65;&#108;&#105;&#x6e;&#101;&#64;&#x65;x&#x61;m&#112;&#108;&#x65;&#46;&#99;&#111;&#109;">&#x65;&#118;&#x65;&#108;&#105;&#x6e;&#x65;&#x40;&#x65;&#x78;&#97;&#109;&#112;&#108;&#x65;.&#99;&#111;&#x6d;</a>&quot;,<br />&quot;valid_from&quot;: &quot;2020-02-07T08:43:34Z&quot;,<br />&quot;time_to_live&quot;: 3600<br />}<br />Please note that only optional fields are: consumer_id, valid_from and time_to_live.<br />In case you omit they the default values are used:<br />consumer_id = consumer of current user<br />valid_from = current time<br />time_to_live = consents.max_time_to_live</p><p>This endpoint is used to confirm a Consent previously created.</p><p>The User must supply a code that was sent out of band (OOB) for example via an SMS.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not consent_id:
            raise ValueError(f"Expected a non-empty value for `consent_id` but received {consent_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/consents/{consent_id}/challenge",
            body=maybe_transform(body, consent_challenge_params.ConsentChallengeParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def revoke(
        self,
        consent_id: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Revoke Consent specified by CONSENT_ID</p><p>There are a few reasons you might need to revoke an application’s access to a user’s account:<br />- The user explicitly wishes to revoke the application’s access<br />- You as the service provider have determined an application is compromised or malicious, and want to disable it<br />- etc.</p><p>OBP as a resource server stores access tokens in a database, then it is relatively easy to revoke some token that belongs to a particular user.<br />The status of the token is changed to &quot;REVOKED&quot; so the next time the revoked client makes a request, their token will fail to validate.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not consent_id:
            raise ValueError(f"Expected a non-empty value for `consent_id` but received {consent_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/consents/{consent_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def user_update_request(
        self,
        consent_id: str,
        *,
        bank_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>This endpoint is used to add the User of Consent.</p><p>Each Consent has one of the following states: INITIATED, ACCEPTED, REJECTED, REVOKED, RECEIVED, VALID, REVOKEDBYPSU, EXPIRED, TERMINATEDBYTPP, AUTHORISED, AWAITINGAUTHORISATION.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not consent_id:
            raise ValueError(f"Expected a non-empty value for `consent_id` but received {consent_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/obp/v5.1.0/banks/{bank_id}/consents/{consent_id}/user-update-request",
            body=maybe_transform(body, consent_user_update_request_params.ConsentUserUpdateRequestParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncConsentsResource(AsyncAPIResource):
    @cached_property
    def email(self) -> AsyncEmailResource:
        return AsyncEmailResource(self._client)

    @cached_property
    def implicit(self) -> AsyncImplicitResource:
        return AsyncImplicitResource(self._client)

    @cached_property
    def sms(self) -> AsyncSMSResource:
        return AsyncSMSResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncConsentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConsentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConsentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncConsentsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        consent_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>This endpoint gets the Consent By consent id.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not consent_id:
            raise ValueError(f"Expected a non-empty value for `consent_id` but received {consent_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/consumer/current/consents/{consent_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def challenge(
        self,
        consent_id: str,
        *,
        bank_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>An OBP Consent allows the holder of the Consent to call one or more endpoints.</p><p>Consents must be created and authorisied using SCA (Strong Customer Authentication).</p><p>That is, Consents can be created by an authorised User via the OBP REST API but they must be confirmed via an out of band (OOB) mechanism such as a code sent to a mobile phone.</p><p>Each Consent has one of the following states: INITIATED, ACCEPTED, REJECTED, REVOKED, RECEIVED, VALID, REVOKEDBYPSU, EXPIRED, TERMINATEDBYTPP, AUTHORISED, AWAITINGAUTHORISATION.</p><p>Each Consent is bound to a consumer i.e. you need to identify yourself over request header value Consumer-Key.<br />For example:<br />GET /obp/v4.0.0/users/current HTTP/1.1<br />Host: 127.0.0.1:8080<br />Consent-JWT: eyJhbGciOiJIUzI1NiJ9.eyJlbnRpdGxlbWVudHMiOlt7InJvbGVfbmFtZSI6IkNhbkdldEFueVVzZXIiLCJiYW5rX2lkIjoiIn<br />1dLCJjcmVhdGVkQnlVc2VySWQiOiJhYjY1MzlhOS1iMTA1LTQ0ODktYTg4My0wYWQ4ZDZjNjE2NTciLCJzdWIiOiIzNDc1MDEzZi03YmY5LTQyNj<br />EtOWUxYy0xZTdlNWZjZTJlN2UiLCJhdWQiOiI4MTVhMGVmMS00YjZhLTQyMDUtYjExMi1lNDVmZDZmNGQzYWQiLCJuYmYiOjE1ODA3NDE2NjcsIml<br />zcyI6Imh0dHA6XC9cLzEyNy4wLjAuMTo4MDgwIiwiZXhwIjoxNTgwNzQ1MjY3LCJpYXQiOjE1ODA3NDE2NjcsImp0aSI6ImJkYzVjZTk5LTE2ZTY<br />tNDM4Yi1hNjllLTU3MTAzN2RhMTg3OCIsInZpZXdzIjpbXX0.L3fEEEhdCVr3qnmyRKBBUaIQ7dk1VjiFaEBW8hUNjfg</p><p>Consumer-Key: ejznk505d132ryomnhbx1qmtohurbsbb0kijajsk<br />cache-control: no-cache</p><p>Maximum time to live of the token is specified over props value consents.max_time_to_live. In case isn't defined default value is 3600 seconds.</p><p>Example of POST JSON:<br />{<br />&quot;everything&quot;: false,<br />&quot;views&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;account_id&quot;: &quot;8ca8a7e4-6d02-40e3-a129-0b2bf89de9f0&quot;,<br />&quot;view_id&quot;: &quot;owner&quot;<br />}<br />],<br />&quot;entitlements&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;role_name&quot;: &quot;CanGetCustomer&quot;<br />}<br />],<br />&quot;consumer_id&quot;: &quot;7uy8a7e4-6d02-40e3-a129-0b2bf89de8uh&quot;,<br />&quot;email&quot;: &quot;<a href="m&#97;i&#108;&#x74;&#111;&#x3a;&#101;v&#x65;&#108;&#105;&#x6e;&#101;&#64;&#x65;x&#x61;m&#112;&#108;&#x65;&#46;&#99;&#111;&#109;">&#x65;&#118;&#x65;&#108;&#105;&#x6e;&#x65;&#x40;&#x65;&#x78;&#97;&#109;&#112;&#108;&#x65;.&#99;&#111;&#x6d;</a>&quot;,<br />&quot;valid_from&quot;: &quot;2020-02-07T08:43:34Z&quot;,<br />&quot;time_to_live&quot;: 3600<br />}<br />Please note that only optional fields are: consumer_id, valid_from and time_to_live.<br />In case you omit they the default values are used:<br />consumer_id = consumer of current user<br />valid_from = current time<br />time_to_live = consents.max_time_to_live</p><p>This endpoint is used to confirm a Consent previously created.</p><p>The User must supply a code that was sent out of band (OOB) for example via an SMS.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not consent_id:
            raise ValueError(f"Expected a non-empty value for `consent_id` but received {consent_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/consents/{consent_id}/challenge",
            body=await async_maybe_transform(body, consent_challenge_params.ConsentChallengeParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def revoke(
        self,
        consent_id: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Revoke Consent specified by CONSENT_ID</p><p>There are a few reasons you might need to revoke an application’s access to a user’s account:<br />- The user explicitly wishes to revoke the application’s access<br />- You as the service provider have determined an application is compromised or malicious, and want to disable it<br />- etc.</p><p>OBP as a resource server stores access tokens in a database, then it is relatively easy to revoke some token that belongs to a particular user.<br />The status of the token is changed to &quot;REVOKED&quot; so the next time the revoked client makes a request, their token will fail to validate.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not consent_id:
            raise ValueError(f"Expected a non-empty value for `consent_id` but received {consent_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/consents/{consent_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def user_update_request(
        self,
        consent_id: str,
        *,
        bank_id: str,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>This endpoint is used to add the User of Consent.</p><p>Each Consent has one of the following states: INITIATED, ACCEPTED, REJECTED, REVOKED, RECEIVED, VALID, REVOKEDBYPSU, EXPIRED, TERMINATEDBYTPP, AUTHORISED, AWAITINGAUTHORISATION.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not consent_id:
            raise ValueError(f"Expected a non-empty value for `consent_id` but received {consent_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/obp/v5.1.0/banks/{bank_id}/consents/{consent_id}/user-update-request",
            body=await async_maybe_transform(body, consent_user_update_request_params.ConsentUserUpdateRequestParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ConsentsResourceWithRawResponse:
    def __init__(self, consents: ConsentsResource) -> None:
        self._consents = consents

        self.retrieve = to_custom_raw_response_wrapper(
            consents.retrieve,
            BinaryAPIResponse,
        )
        self.challenge = to_custom_raw_response_wrapper(
            consents.challenge,
            BinaryAPIResponse,
        )
        self.revoke = to_custom_raw_response_wrapper(
            consents.revoke,
            BinaryAPIResponse,
        )
        self.user_update_request = to_custom_raw_response_wrapper(
            consents.user_update_request,
            BinaryAPIResponse,
        )

    @cached_property
    def email(self) -> EmailResourceWithRawResponse:
        return EmailResourceWithRawResponse(self._consents.email)

    @cached_property
    def implicit(self) -> ImplicitResourceWithRawResponse:
        return ImplicitResourceWithRawResponse(self._consents.implicit)

    @cached_property
    def sms(self) -> SMSResourceWithRawResponse:
        return SMSResourceWithRawResponse(self._consents.sms)


class AsyncConsentsResourceWithRawResponse:
    def __init__(self, consents: AsyncConsentsResource) -> None:
        self._consents = consents

        self.retrieve = async_to_custom_raw_response_wrapper(
            consents.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.challenge = async_to_custom_raw_response_wrapper(
            consents.challenge,
            AsyncBinaryAPIResponse,
        )
        self.revoke = async_to_custom_raw_response_wrapper(
            consents.revoke,
            AsyncBinaryAPIResponse,
        )
        self.user_update_request = async_to_custom_raw_response_wrapper(
            consents.user_update_request,
            AsyncBinaryAPIResponse,
        )

    @cached_property
    def email(self) -> AsyncEmailResourceWithRawResponse:
        return AsyncEmailResourceWithRawResponse(self._consents.email)

    @cached_property
    def implicit(self) -> AsyncImplicitResourceWithRawResponse:
        return AsyncImplicitResourceWithRawResponse(self._consents.implicit)

    @cached_property
    def sms(self) -> AsyncSMSResourceWithRawResponse:
        return AsyncSMSResourceWithRawResponse(self._consents.sms)


class ConsentsResourceWithStreamingResponse:
    def __init__(self, consents: ConsentsResource) -> None:
        self._consents = consents

        self.retrieve = to_custom_streamed_response_wrapper(
            consents.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.challenge = to_custom_streamed_response_wrapper(
            consents.challenge,
            StreamedBinaryAPIResponse,
        )
        self.revoke = to_custom_streamed_response_wrapper(
            consents.revoke,
            StreamedBinaryAPIResponse,
        )
        self.user_update_request = to_custom_streamed_response_wrapper(
            consents.user_update_request,
            StreamedBinaryAPIResponse,
        )

    @cached_property
    def email(self) -> EmailResourceWithStreamingResponse:
        return EmailResourceWithStreamingResponse(self._consents.email)

    @cached_property
    def implicit(self) -> ImplicitResourceWithStreamingResponse:
        return ImplicitResourceWithStreamingResponse(self._consents.implicit)

    @cached_property
    def sms(self) -> SMSResourceWithStreamingResponse:
        return SMSResourceWithStreamingResponse(self._consents.sms)


class AsyncConsentsResourceWithStreamingResponse:
    def __init__(self, consents: AsyncConsentsResource) -> None:
        self._consents = consents

        self.retrieve = async_to_custom_streamed_response_wrapper(
            consents.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.challenge = async_to_custom_streamed_response_wrapper(
            consents.challenge,
            AsyncStreamedBinaryAPIResponse,
        )
        self.revoke = async_to_custom_streamed_response_wrapper(
            consents.revoke,
            AsyncStreamedBinaryAPIResponse,
        )
        self.user_update_request = async_to_custom_streamed_response_wrapper(
            consents.user_update_request,
            AsyncStreamedBinaryAPIResponse,
        )

    @cached_property
    def email(self) -> AsyncEmailResourceWithStreamingResponse:
        return AsyncEmailResourceWithStreamingResponse(self._consents.email)

    @cached_property
    def implicit(self) -> AsyncImplicitResourceWithStreamingResponse:
        return AsyncImplicitResourceWithStreamingResponse(self._consents.implicit)

    @cached_property
    def sms(self) -> AsyncSMSResourceWithStreamingResponse:
        return AsyncSMSResourceWithStreamingResponse(self._consents.sms)
