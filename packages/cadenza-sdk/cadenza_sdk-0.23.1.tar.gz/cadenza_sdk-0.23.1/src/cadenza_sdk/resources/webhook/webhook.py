# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import webhook_pubsub_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from .cloud_scheduler import (
    CloudSchedulerResource,
    AsyncCloudSchedulerResource,
    CloudSchedulerResourceWithRawResponse,
    AsyncCloudSchedulerResourceWithRawResponse,
    CloudSchedulerResourceWithStreamingResponse,
    AsyncCloudSchedulerResourceWithStreamingResponse,
)
from ...types.webhook_pubsub_response import WebhookPubsubResponse

__all__ = ["WebhookResource", "AsyncWebhookResource"]


class WebhookResource(SyncAPIResource):
    @cached_property
    def cloud_scheduler(self) -> CloudSchedulerResource:
        return CloudSchedulerResource(self._client)

    @cached_property
    def with_raw_response(self) -> WebhookResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#accessing-raw-response-data-eg-headers
        """
        return WebhookResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebhookResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#with_streaming_response
        """
        return WebhookResourceWithStreamingResponse(self)

    def pubsub(
        self,
        *,
        message: webhook_pubsub_params.Message,
        subscription: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookPubsubResponse:
        """
        PubSub Event Handler

        Args:
          subscription: The subscription name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/webhook/pubsub",
            body=maybe_transform(
                {
                    "message": message,
                    "subscription": subscription,
                },
                webhook_pubsub_params.WebhookPubsubParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookPubsubResponse,
        )


class AsyncWebhookResource(AsyncAPIResource):
    @cached_property
    def cloud_scheduler(self) -> AsyncCloudSchedulerResource:
        return AsyncCloudSchedulerResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncWebhookResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWebhookResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebhookResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#with_streaming_response
        """
        return AsyncWebhookResourceWithStreamingResponse(self)

    async def pubsub(
        self,
        *,
        message: webhook_pubsub_params.Message,
        subscription: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookPubsubResponse:
        """
        PubSub Event Handler

        Args:
          subscription: The subscription name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/webhook/pubsub",
            body=await async_maybe_transform(
                {
                    "message": message,
                    "subscription": subscription,
                },
                webhook_pubsub_params.WebhookPubsubParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookPubsubResponse,
        )


class WebhookResourceWithRawResponse:
    def __init__(self, webhook: WebhookResource) -> None:
        self._webhook = webhook

        self.pubsub = to_raw_response_wrapper(
            webhook.pubsub,
        )

    @cached_property
    def cloud_scheduler(self) -> CloudSchedulerResourceWithRawResponse:
        return CloudSchedulerResourceWithRawResponse(self._webhook.cloud_scheduler)


class AsyncWebhookResourceWithRawResponse:
    def __init__(self, webhook: AsyncWebhookResource) -> None:
        self._webhook = webhook

        self.pubsub = async_to_raw_response_wrapper(
            webhook.pubsub,
        )

    @cached_property
    def cloud_scheduler(self) -> AsyncCloudSchedulerResourceWithRawResponse:
        return AsyncCloudSchedulerResourceWithRawResponse(self._webhook.cloud_scheduler)


class WebhookResourceWithStreamingResponse:
    def __init__(self, webhook: WebhookResource) -> None:
        self._webhook = webhook

        self.pubsub = to_streamed_response_wrapper(
            webhook.pubsub,
        )

    @cached_property
    def cloud_scheduler(self) -> CloudSchedulerResourceWithStreamingResponse:
        return CloudSchedulerResourceWithStreamingResponse(self._webhook.cloud_scheduler)


class AsyncWebhookResourceWithStreamingResponse:
    def __init__(self, webhook: AsyncWebhookResource) -> None:
        self._webhook = webhook

        self.pubsub = async_to_streamed_response_wrapper(
            webhook.pubsub,
        )

    @cached_property
    def cloud_scheduler(self) -> AsyncCloudSchedulerResourceWithStreamingResponse:
        return AsyncCloudSchedulerResourceWithStreamingResponse(self._webhook.cloud_scheduler)
