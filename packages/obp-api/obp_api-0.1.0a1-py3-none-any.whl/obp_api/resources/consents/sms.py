# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
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
from ...types.consents import sms_create_params

__all__ = ["SMSResource", "AsyncSMSResource"]


class SMSResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SMSResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return SMSResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SMSResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return SMSResourceWithStreamingResponse(self)

    def create(
        self,
        bank_id: str,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>This endpoint starts the process of creating a Consent.</p><p>The Consent is created in an INITIATED state.</p><p>A One Time Password (OTP) (AKA security challenge) is sent Out of Band (OOB) to the User via the transport defined in SCA_METHOD<br />SCA_METHOD is typically &quot;SMS&quot;,&quot;EMAIL&quot; or &quot;IMPLICIT&quot;. &quot;EMAIL&quot; is used for testing purposes. OBP mapped mode &quot;IMPLICIT&quot; is &quot;EMAIL&quot;.<br />Other mode, bank can decide it in the connector method 'getConsentImplicitSCA'.</p><p>When the Consent is created, OBP (or a backend system) stores the challenge so it can be checked later against the value supplied by the User with the Answer Consent Challenge endpoint.</p><p>An OBP Consent allows the holder of the Consent to call one or more endpoints.</p><p>Consents must be created and authorisied using SCA (Strong Customer Authentication).</p><p>That is, Consents can be created by an authorised User via the OBP REST API but they must be confirmed via an out of band (OOB) mechanism such as a code sent to a mobile phone.</p><p>Each Consent has one of the following states: INITIATED, ACCEPTED, REJECTED, REVOKED, RECEIVED, VALID, REVOKEDBYPSU, EXPIRED, TERMINATEDBYTPP, AUTHORISED, AWAITINGAUTHORISATION.</p><p>Each Consent is bound to a consumer i.e. you need to identify yourself over request header value Consumer-Key.<br />For example:<br />GET /obp/v4.0.0/users/current HTTP/1.1<br />Host: 127.0.0.1:8080<br />Consent-JWT: eyJhbGciOiJIUzI1NiJ9.eyJlbnRpdGxlbWVudHMiOlt7InJvbGVfbmFtZSI6IkNhbkdldEFueVVzZXIiLCJiYW5rX2lkIjoiIn<br />1dLCJjcmVhdGVkQnlVc2VySWQiOiJhYjY1MzlhOS1iMTA1LTQ0ODktYTg4My0wYWQ4ZDZjNjE2NTciLCJzdWIiOiIzNDc1MDEzZi03YmY5LTQyNj<br />EtOWUxYy0xZTdlNWZjZTJlN2UiLCJhdWQiOiI4MTVhMGVmMS00YjZhLTQyMDUtYjExMi1lNDVmZDZmNGQzYWQiLCJuYmYiOjE1ODA3NDE2NjcsIml<br />zcyI6Imh0dHA6XC9cLzEyNy4wLjAuMTo4MDgwIiwiZXhwIjoxNTgwNzQ1MjY3LCJpYXQiOjE1ODA3NDE2NjcsImp0aSI6ImJkYzVjZTk5LTE2ZTY<br />tNDM4Yi1hNjllLTU3MTAzN2RhMTg3OCIsInZpZXdzIjpbXX0.L3fEEEhdCVr3qnmyRKBBUaIQ7dk1VjiFaEBW8hUNjfg</p><p>Consumer-Key: ejznk505d132ryomnhbx1qmtohurbsbb0kijajsk<br />cache-control: no-cache</p><p>Maximum time to live of the token is specified over props value consents.max_time_to_live. In case isn't defined default value is 3600 seconds.</p><p>Example of POST JSON:<br />{<br />&quot;everything&quot;: false,<br />&quot;views&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;account_id&quot;: &quot;8ca8a7e4-6d02-40e3-a129-0b2bf89de9f0&quot;,<br />&quot;view_id&quot;: &quot;owner&quot;<br />}<br />],<br />&quot;entitlements&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;role_name&quot;: &quot;CanGetCustomer&quot;<br />}<br />],<br />&quot;consumer_id&quot;: &quot;7uy8a7e4-6d02-40e3-a129-0b2bf89de8uh&quot;,<br />&quot;email&quot;: &quot;<a href="&#x6d;a&#105;&#x6c;&#x74;&#x6f;&#58;&#101;v&#101;&#x6c;&#105;n&#x65;&#x40;&#101;xa&#109;&#x70;l&#x65;&#x2e;&#x63;&#x6f;&#x6d;">&#101;&#x76;&#x65;&#108;ine&#x40;&#x65;x&#x61;&#109;&#112;&#108;&#101;&#46;&#99;&#x6f;&#109;</a>&quot;,<br />&quot;valid_from&quot;: &quot;2020-02-07T08:43:34Z&quot;,<br />&quot;time_to_live&quot;: 3600<br />}<br />Please note that only optional fields are: consumer_id, valid_from and time_to_live.<br />In case you omit they the default values are used:<br />consumer_id = consumer of current user<br />valid_from = current time<br />time_to_live = consents.max_time_to_live</p><p>Authentication is Mandatory</p><p>Example 1:<br />{<br />&quot;everything&quot;: true,<br />&quot;views&quot;: [],<br />&quot;entitlements&quot;: [],<br />&quot;consumer_id&quot;: &quot;7uy8a7e4-6d02-40e3-a129-0b2bf89de8uh&quot;,<br />&quot;email&quot;: &quot;<a href="&#x6d;a&#x69;&#108;to&#58;e&#118;e&#x6c;i&#110;e&#x40;&#x65;&#x78;&#97;&#109;&#x70;&#x6c;&#x65;&#x2e;&#99;&#x6f;&#109;">&#101;v&#x65;&#108;&#x69;&#110;&#x65;&#x40;&#101;&#120;&#97;&#x6d;&#112;&#108;&#101;&#x2e;co&#x6d;</a>&quot;<br />}</p><p>Please note that consumer_id is optional field<br />Example 2:<br />{<br />&quot;everything&quot;: true,<br />&quot;views&quot;: [],<br />&quot;entitlements&quot;: [],<br />&quot;email&quot;: &quot;<a href="&#x6d;a&#105;&#108;&#116;&#x6f;:&#101;&#118;&#x65;&#108;i&#110;&#x65;&#64;&#101;&#x78;&#x61;&#109;p&#108;&#101;&#46;&#x63;&#x6f;&#x6d;">&#101;&#x76;el&#105;&#x6e;&#x65;&#x40;&#x65;&#120;&#x61;m&#x70;&#108;&#x65;&#x2e;&#99;&#x6f;&#x6d;</a>&quot;<br />}</p><p>Please note if everything=false you need to explicitly specify views and entitlements<br />Example 3:<br />{<br />&quot;everything&quot;: false,<br />&quot;views&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;account_id&quot;: &quot;8ca8a7e4-6d02-40e3-a129-0b2bf89de9f0&quot;,<br />&quot;view_id&quot;: &quot;owner&quot;<br />}<br />],<br />&quot;entitlements&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;role_name&quot;: &quot;CanGetCustomer&quot;<br />}<br />],<br />&quot;consumer_id&quot;: &quot;7uy8a7e4-6d02-40e3-a129-0b2bf89de8uh&quot;,<br />&quot;email&quot;: &quot;<a href="m&#x61;&#x69;&#108;&#x74;o&#x3a;&#101;&#x76;&#x65;&#x6c;&#105;n&#101;&#64;&#101;&#120;&#97;&#x6d;&#112;&#108;&#x65;.&#x63;&#x6f;&#109;">&#x65;&#x76;&#101;&#x6c;&#x69;&#110;&#x65;&#x40;&#x65;x&#97;m&#x70;&#108;&#x65;&#46;&#x63;&#111;&#x6d;</a>&quot;<br />}</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/obp/v5.1.0/banks/{bank_id}/my/consents/SMS",
            body=maybe_transform(body, sms_create_params.SMSCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncSMSResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSMSResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSMSResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSMSResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncSMSResourceWithStreamingResponse(self)

    async def create(
        self,
        bank_id: str,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>This endpoint starts the process of creating a Consent.</p><p>The Consent is created in an INITIATED state.</p><p>A One Time Password (OTP) (AKA security challenge) is sent Out of Band (OOB) to the User via the transport defined in SCA_METHOD<br />SCA_METHOD is typically &quot;SMS&quot;,&quot;EMAIL&quot; or &quot;IMPLICIT&quot;. &quot;EMAIL&quot; is used for testing purposes. OBP mapped mode &quot;IMPLICIT&quot; is &quot;EMAIL&quot;.<br />Other mode, bank can decide it in the connector method 'getConsentImplicitSCA'.</p><p>When the Consent is created, OBP (or a backend system) stores the challenge so it can be checked later against the value supplied by the User with the Answer Consent Challenge endpoint.</p><p>An OBP Consent allows the holder of the Consent to call one or more endpoints.</p><p>Consents must be created and authorisied using SCA (Strong Customer Authentication).</p><p>That is, Consents can be created by an authorised User via the OBP REST API but they must be confirmed via an out of band (OOB) mechanism such as a code sent to a mobile phone.</p><p>Each Consent has one of the following states: INITIATED, ACCEPTED, REJECTED, REVOKED, RECEIVED, VALID, REVOKEDBYPSU, EXPIRED, TERMINATEDBYTPP, AUTHORISED, AWAITINGAUTHORISATION.</p><p>Each Consent is bound to a consumer i.e. you need to identify yourself over request header value Consumer-Key.<br />For example:<br />GET /obp/v4.0.0/users/current HTTP/1.1<br />Host: 127.0.0.1:8080<br />Consent-JWT: eyJhbGciOiJIUzI1NiJ9.eyJlbnRpdGxlbWVudHMiOlt7InJvbGVfbmFtZSI6IkNhbkdldEFueVVzZXIiLCJiYW5rX2lkIjoiIn<br />1dLCJjcmVhdGVkQnlVc2VySWQiOiJhYjY1MzlhOS1iMTA1LTQ0ODktYTg4My0wYWQ4ZDZjNjE2NTciLCJzdWIiOiIzNDc1MDEzZi03YmY5LTQyNj<br />EtOWUxYy0xZTdlNWZjZTJlN2UiLCJhdWQiOiI4MTVhMGVmMS00YjZhLTQyMDUtYjExMi1lNDVmZDZmNGQzYWQiLCJuYmYiOjE1ODA3NDE2NjcsIml<br />zcyI6Imh0dHA6XC9cLzEyNy4wLjAuMTo4MDgwIiwiZXhwIjoxNTgwNzQ1MjY3LCJpYXQiOjE1ODA3NDE2NjcsImp0aSI6ImJkYzVjZTk5LTE2ZTY<br />tNDM4Yi1hNjllLTU3MTAzN2RhMTg3OCIsInZpZXdzIjpbXX0.L3fEEEhdCVr3qnmyRKBBUaIQ7dk1VjiFaEBW8hUNjfg</p><p>Consumer-Key: ejznk505d132ryomnhbx1qmtohurbsbb0kijajsk<br />cache-control: no-cache</p><p>Maximum time to live of the token is specified over props value consents.max_time_to_live. In case isn't defined default value is 3600 seconds.</p><p>Example of POST JSON:<br />{<br />&quot;everything&quot;: false,<br />&quot;views&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;account_id&quot;: &quot;8ca8a7e4-6d02-40e3-a129-0b2bf89de9f0&quot;,<br />&quot;view_id&quot;: &quot;owner&quot;<br />}<br />],<br />&quot;entitlements&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;role_name&quot;: &quot;CanGetCustomer&quot;<br />}<br />],<br />&quot;consumer_id&quot;: &quot;7uy8a7e4-6d02-40e3-a129-0b2bf89de8uh&quot;,<br />&quot;email&quot;: &quot;<a href="&#x6d;a&#105;&#x6c;&#x74;&#x6f;&#58;&#101;v&#101;&#x6c;&#105;n&#x65;&#x40;&#101;xa&#109;&#x70;l&#x65;&#x2e;&#x63;&#x6f;&#x6d;">&#101;&#x76;&#x65;&#108;ine&#x40;&#x65;x&#x61;&#109;&#112;&#108;&#101;&#46;&#99;&#x6f;&#109;</a>&quot;,<br />&quot;valid_from&quot;: &quot;2020-02-07T08:43:34Z&quot;,<br />&quot;time_to_live&quot;: 3600<br />}<br />Please note that only optional fields are: consumer_id, valid_from and time_to_live.<br />In case you omit they the default values are used:<br />consumer_id = consumer of current user<br />valid_from = current time<br />time_to_live = consents.max_time_to_live</p><p>Authentication is Mandatory</p><p>Example 1:<br />{<br />&quot;everything&quot;: true,<br />&quot;views&quot;: [],<br />&quot;entitlements&quot;: [],<br />&quot;consumer_id&quot;: &quot;7uy8a7e4-6d02-40e3-a129-0b2bf89de8uh&quot;,<br />&quot;email&quot;: &quot;<a href="&#x6d;a&#x69;&#108;to&#58;e&#118;e&#x6c;i&#110;e&#x40;&#x65;&#x78;&#97;&#109;&#x70;&#x6c;&#x65;&#x2e;&#99;&#x6f;&#109;">&#101;v&#x65;&#108;&#x69;&#110;&#x65;&#x40;&#101;&#120;&#97;&#x6d;&#112;&#108;&#101;&#x2e;co&#x6d;</a>&quot;<br />}</p><p>Please note that consumer_id is optional field<br />Example 2:<br />{<br />&quot;everything&quot;: true,<br />&quot;views&quot;: [],<br />&quot;entitlements&quot;: [],<br />&quot;email&quot;: &quot;<a href="&#x6d;a&#105;&#108;&#116;&#x6f;:&#101;&#118;&#x65;&#108;i&#110;&#x65;&#64;&#101;&#x78;&#x61;&#109;p&#108;&#101;&#46;&#x63;&#x6f;&#x6d;">&#101;&#x76;el&#105;&#x6e;&#x65;&#x40;&#x65;&#120;&#x61;m&#x70;&#108;&#x65;&#x2e;&#99;&#x6f;&#x6d;</a>&quot;<br />}</p><p>Please note if everything=false you need to explicitly specify views and entitlements<br />Example 3:<br />{<br />&quot;everything&quot;: false,<br />&quot;views&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;account_id&quot;: &quot;8ca8a7e4-6d02-40e3-a129-0b2bf89de9f0&quot;,<br />&quot;view_id&quot;: &quot;owner&quot;<br />}<br />],<br />&quot;entitlements&quot;: [<br />{<br />&quot;bank_id&quot;: &quot;GENODEM1GLS&quot;,<br />&quot;role_name&quot;: &quot;CanGetCustomer&quot;<br />}<br />],<br />&quot;consumer_id&quot;: &quot;7uy8a7e4-6d02-40e3-a129-0b2bf89de8uh&quot;,<br />&quot;email&quot;: &quot;<a href="m&#x61;&#x69;&#108;&#x74;o&#x3a;&#101;&#x76;&#x65;&#x6c;&#105;n&#101;&#64;&#101;&#120;&#97;&#x6d;&#112;&#108;&#x65;.&#x63;&#x6f;&#109;">&#x65;&#x76;&#101;&#x6c;&#x69;&#110;&#x65;&#x40;&#x65;x&#97;m&#x70;&#108;&#x65;&#46;&#x63;&#111;&#x6d;</a>&quot;<br />}</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/obp/v5.1.0/banks/{bank_id}/my/consents/SMS",
            body=await async_maybe_transform(body, sms_create_params.SMSCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class SMSResourceWithRawResponse:
    def __init__(self, sms: SMSResource) -> None:
        self._sms = sms

        self.create = to_custom_raw_response_wrapper(
            sms.create,
            BinaryAPIResponse,
        )


class AsyncSMSResourceWithRawResponse:
    def __init__(self, sms: AsyncSMSResource) -> None:
        self._sms = sms

        self.create = async_to_custom_raw_response_wrapper(
            sms.create,
            AsyncBinaryAPIResponse,
        )


class SMSResourceWithStreamingResponse:
    def __init__(self, sms: SMSResource) -> None:
        self._sms = sms

        self.create = to_custom_streamed_response_wrapper(
            sms.create,
            StreamedBinaryAPIResponse,
        )


class AsyncSMSResourceWithStreamingResponse:
    def __init__(self, sms: AsyncSMSResource) -> None:
        self._sms = sms

        self.create = async_to_custom_streamed_response_wrapper(
            sms.create,
            AsyncStreamedBinaryAPIResponse,
        )
