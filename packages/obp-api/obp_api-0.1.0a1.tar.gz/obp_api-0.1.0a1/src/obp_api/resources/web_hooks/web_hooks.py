# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .notifications import (
    NotificationsResource,
    AsyncNotificationsResource,
    NotificationsResourceWithRawResponse,
    AsyncNotificationsResourceWithRawResponse,
    NotificationsResourceWithStreamingResponse,
    AsyncNotificationsResourceWithStreamingResponse,
)

__all__ = ["WebHooksResource", "AsyncWebHooksResource"]


class WebHooksResource(SyncAPIResource):
    @cached_property
    def notifications(self) -> NotificationsResource:
        return NotificationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> WebHooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return WebHooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebHooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return WebHooksResourceWithStreamingResponse(self)


class AsyncWebHooksResource(AsyncAPIResource):
    @cached_property
    def notifications(self) -> AsyncNotificationsResource:
        return AsyncNotificationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncWebHooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/nemozak1/obp-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWebHooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebHooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/nemozak1/obp-api-python#with_streaming_response
        """
        return AsyncWebHooksResourceWithStreamingResponse(self)


class WebHooksResourceWithRawResponse:
    def __init__(self, web_hooks: WebHooksResource) -> None:
        self._web_hooks = web_hooks

    @cached_property
    def notifications(self) -> NotificationsResourceWithRawResponse:
        return NotificationsResourceWithRawResponse(self._web_hooks.notifications)


class AsyncWebHooksResourceWithRawResponse:
    def __init__(self, web_hooks: AsyncWebHooksResource) -> None:
        self._web_hooks = web_hooks

    @cached_property
    def notifications(self) -> AsyncNotificationsResourceWithRawResponse:
        return AsyncNotificationsResourceWithRawResponse(self._web_hooks.notifications)


class WebHooksResourceWithStreamingResponse:
    def __init__(self, web_hooks: WebHooksResource) -> None:
        self._web_hooks = web_hooks

    @cached_property
    def notifications(self) -> NotificationsResourceWithStreamingResponse:
        return NotificationsResourceWithStreamingResponse(self._web_hooks.notifications)


class AsyncWebHooksResourceWithStreamingResponse:
    def __init__(self, web_hooks: AsyncWebHooksResource) -> None:
        self._web_hooks = web_hooks

    @cached_property
    def notifications(self) -> AsyncNotificationsResourceWithStreamingResponse:
        return AsyncNotificationsResourceWithStreamingResponse(self._web_hooks.notifications)
