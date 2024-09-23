# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

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
from ...types.event import task_task_quote_params
from ..._base_client import make_request_options
from ...types.event.task_quote import TaskQuote
from ...types.trading.quote_request_param import QuoteRequestParam

__all__ = ["TaskResource", "AsyncTaskResource"]


class TaskResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TaskResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TaskResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TaskResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#with_streaming_response
        """
        return TaskResourceWithStreamingResponse(self)

    def task_quote(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.task.quote",
            "cadenza.dropCopy.quoteRequestAck",
            "cadenza.dropCopy.placeOrderRequestAck",
            "cadenza.dropCopy.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.executionReport",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: QuoteRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskQuote:
        """
        PubSub event handler placeholder for quote request acknowledgment event

        Args:
          event_id: A unique identifier for the event.

          event_type: Event Type

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/webhook/pubsub/task/quote",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                task_task_quote_params.TaskTaskQuoteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskQuote,
        )


class AsyncTaskResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTaskResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTaskResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTaskResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#with_streaming_response
        """
        return AsyncTaskResourceWithStreamingResponse(self)

    async def task_quote(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.task.quote",
            "cadenza.dropCopy.quoteRequestAck",
            "cadenza.dropCopy.placeOrderRequestAck",
            "cadenza.dropCopy.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.executionReport",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: QuoteRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskQuote:
        """
        PubSub event handler placeholder for quote request acknowledgment event

        Args:
          event_id: A unique identifier for the event.

          event_type: Event Type

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/webhook/pubsub/task/quote",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                task_task_quote_params.TaskTaskQuoteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskQuote,
        )


class TaskResourceWithRawResponse:
    def __init__(self, task: TaskResource) -> None:
        self._task = task

        self.task_quote = to_raw_response_wrapper(
            task.task_quote,
        )


class AsyncTaskResourceWithRawResponse:
    def __init__(self, task: AsyncTaskResource) -> None:
        self._task = task

        self.task_quote = async_to_raw_response_wrapper(
            task.task_quote,
        )


class TaskResourceWithStreamingResponse:
    def __init__(self, task: TaskResource) -> None:
        self._task = task

        self.task_quote = to_streamed_response_wrapper(
            task.task_quote,
        )


class AsyncTaskResourceWithStreamingResponse:
    def __init__(self, task: AsyncTaskResource) -> None:
        self._task = task

        self.task_quote = async_to_streamed_response_wrapper(
            task.task_quote,
        )
