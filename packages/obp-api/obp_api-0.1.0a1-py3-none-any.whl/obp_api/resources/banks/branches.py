# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...types.banks import branch_create_params
from ..._base_client import make_request_options

__all__ = ["BranchesResource", "AsyncBranchesResource"]


class BranchesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BranchesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return BranchesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BranchesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return BranchesResourceWithStreamingResponse(self)

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
        <p>Create Branch for the Bank.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/branches",
            body=maybe_transform(body, branch_create_params.BranchCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def retrieve(
        self,
        branch_id: str,
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
        <p>Returns information about a single Branch specified by BANK_ID and BRANCH_ID including:</p><ul><li>Name</li><li>Address</li><li>Geo Location</li><li>License the data under this endpoint is released under.</li></ul><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not branch_id:
            raise ValueError(f"Expected a non-empty value for `branch_id` but received {branch_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/branches/{branch_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        <p>Returns information about branches for a single bank specified by BANK_ID including:</p><ul><li>Name</li><li>Address</li><li>Geo Location</li><li>License the data under this endpoint is released under</li><li>Structured opening hours</li><li>Accessible flag</li><li>Branch Type</li><li>More Info</li></ul><p>Pagination:</p><p>By default, 50 records are returned.</p><p>You can use the url query parameters <em>limit</em> and <em>offset</em> for pagination<br />You can also use the follow url query parameters:</p><ul><li><p>city - string, find Branches those in this city, optional</p></li><li><p>withinMetersOf - number, find Branches within given meters distance, optional</p></li><li>nearLatitude - number, a position of latitude value, cooperate with withMetersOf do query filter, optional</li><li>nearLongitude - number, a position of longitude value, cooperate with withMetersOf do query filter, optional</li></ul><p>note: withinMetersOf, nearLatitude and nearLongitude either all empty or all have value.</p><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/obp/v5.1.0/banks/{bank_id}/branches",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def delete(
        self,
        branch_id: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete Branch from given Bank.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not branch_id:
            raise ValueError(f"Expected a non-empty value for `branch_id` but received {branch_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/branches/{branch_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncBranchesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBranchesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBranchesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBranchesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncBranchesResourceWithStreamingResponse(self)

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
        <p>Create Branch for the Bank.</p><p>Authentication is Mandatory</p>

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
            f"/obp/v5.1.0/banks/{bank_id}/branches",
            body=await async_maybe_transform(body, branch_create_params.BranchCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def retrieve(
        self,
        branch_id: str,
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
        <p>Returns information about a single Branch specified by BANK_ID and BRANCH_ID including:</p><ul><li>Name</li><li>Address</li><li>Geo Location</li><li>License the data under this endpoint is released under.</li></ul><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not branch_id:
            raise ValueError(f"Expected a non-empty value for `branch_id` but received {branch_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/branches/{branch_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
        self,
        bank_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        <p>Returns information about branches for a single bank specified by BANK_ID including:</p><ul><li>Name</li><li>Address</li><li>Geo Location</li><li>License the data under this endpoint is released under</li><li>Structured opening hours</li><li>Accessible flag</li><li>Branch Type</li><li>More Info</li></ul><p>Pagination:</p><p>By default, 50 records are returned.</p><p>You can use the url query parameters <em>limit</em> and <em>offset</em> for pagination<br />You can also use the follow url query parameters:</p><ul><li><p>city - string, find Branches those in this city, optional</p></li><li><p>withinMetersOf - number, find Branches within given meters distance, optional</p></li><li>nearLatitude - number, a position of latitude value, cooperate with withMetersOf do query filter, optional</li><li>nearLongitude - number, a position of longitude value, cooperate with withMetersOf do query filter, optional</li></ul><p>note: withinMetersOf, nearLatitude and nearLongitude either all empty or all have value.</p><p>Authentication is Optional</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/obp/v5.1.0/banks/{bank_id}/branches",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def delete(
        self,
        branch_id: str,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        <p>Delete Branch from given Bank.</p><p>Authentication is Mandatory</p>

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bank_id:
            raise ValueError(f"Expected a non-empty value for `bank_id` but received {bank_id!r}")
        if not branch_id:
            raise ValueError(f"Expected a non-empty value for `branch_id` but received {branch_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/obp/v5.1.0/banks/{bank_id}/branches/{branch_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class BranchesResourceWithRawResponse:
    def __init__(self, branches: BranchesResource) -> None:
        self._branches = branches

        self.create = to_custom_raw_response_wrapper(
            branches.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_custom_raw_response_wrapper(
            branches.retrieve,
            BinaryAPIResponse,
        )
        self.list = to_custom_raw_response_wrapper(
            branches.list,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            branches.delete,
        )


class AsyncBranchesResourceWithRawResponse:
    def __init__(self, branches: AsyncBranchesResource) -> None:
        self._branches = branches

        self.create = async_to_custom_raw_response_wrapper(
            branches.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_raw_response_wrapper(
            branches.retrieve,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_custom_raw_response_wrapper(
            branches.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            branches.delete,
        )


class BranchesResourceWithStreamingResponse:
    def __init__(self, branches: BranchesResource) -> None:
        self._branches = branches

        self.create = to_custom_streamed_response_wrapper(
            branches.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_custom_streamed_response_wrapper(
            branches.retrieve,
            StreamedBinaryAPIResponse,
        )
        self.list = to_custom_streamed_response_wrapper(
            branches.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            branches.delete,
        )


class AsyncBranchesResourceWithStreamingResponse:
    def __init__(self, branches: AsyncBranchesResource) -> None:
        self._branches = branches

        self.create = async_to_custom_streamed_response_wrapper(
            branches.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_custom_streamed_response_wrapper(
            branches.retrieve,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            branches.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            branches.delete,
        )
