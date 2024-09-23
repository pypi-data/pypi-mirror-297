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
from ...types.event import (
    drop_copy_drop_copy_order_params,
    drop_copy_drop_copy_quote_params,
    drop_copy_drop_copy_portfolio_params,
    drop_copy_drop_copy_execution_report_params,
    drop_copy_drop_copy_quote_request_ack_params,
    drop_copy_drop_copy_place_order_request_ack_params,
    drop_copy_drop_copy_cancel_order_request_ack_params,
)
from ..._base_client import make_request_options
from ...types.trading.order_param import OrderParam
from ...types.trading.quote_param import QuoteParam
from ...types.event.drop_copy_order import DropCopyOrder
from ...types.event.drop_copy_quote import DropCopyQuote
from ...types.event.drop_copy_portfolio import DropCopyPortfolio
from ...types.event.drop_copy_request_ack import DropCopyRequestAck
from ...types.trading.quote_request_param import QuoteRequestParam
from ...types.trading.execution_report_param import ExecutionReportParam
from ...types.event.drop_copy_execution_report import DropCopyExecutionReport
from ...types.exchange_account_portfolio_param import ExchangeAccountPortfolioParam
from ...types.trading.place_order_request_param import PlaceOrderRequestParam
from ...types.trading.cancel_order_request_param import CancelOrderRequestParam
from ...types.event.drop_copy_place_order_request_ack import DropCopyPlaceOrderRequestAck
from ...types.event.drop_copy_cancel_order_request_ack import DropCopyCancelOrderRequestAck

__all__ = ["DropCopyResource", "AsyncDropCopyResource"]


class DropCopyResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DropCopyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DropCopyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DropCopyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#with_streaming_response
        """
        return DropCopyResourceWithStreamingResponse(self)

    def drop_copy_cancel_order_request_ack(
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
        payload: CancelOrderRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyCancelOrderRequestAck:
        """
        PubSub event handler placeholder for cancel order request acknowledgment event

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
            "/api/v2/webhook/pubsub/dropCopy/cancelOrderRequestAck",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_cancel_order_request_ack_params.DropCopyDropCopyCancelOrderRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyCancelOrderRequestAck,
        )

    def drop_copy_execution_report(
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
        payload: ExecutionReportParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyExecutionReport:
        """
        PubSub event handler for execution report drop copy event

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
            "/api/v2/webhook/pubsub/dropCopy/executionReport",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_execution_report_params.DropCopyDropCopyExecutionReportParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyExecutionReport,
        )

    def drop_copy_order(
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
        payload: OrderParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyOrder:
        """
        PubSub event handler placeholder for order event

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
            "/api/v2/webhook/pubsub/dropCopy/order",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_order_params.DropCopyDropCopyOrderParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyOrder,
        )

    def drop_copy_place_order_request_ack(
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
        payload: PlaceOrderRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyPlaceOrderRequestAck:
        """
        PubSub event handler placeholder for place order request acknowledgment event

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
            "/api/v2/webhook/pubsub/dropCopy/placeOrderRequestAck",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_place_order_request_ack_params.DropCopyDropCopyPlaceOrderRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyPlaceOrderRequestAck,
        )

    def drop_copy_portfolio(
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
        payload: ExchangeAccountPortfolioParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyPortfolio:
        """
        PubSub event handler placeholder for portfolio event

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
            "/api/v2/webhook/pubsub/dropCopy/portfolio",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_portfolio_params.DropCopyDropCopyPortfolioParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyPortfolio,
        )

    def drop_copy_quote(
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
        payload: QuoteParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyQuote:
        """
        PubSub event handler placeholder for quote event

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
            "/api/v2/webhook/pubsub/dropCopy/quote",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_quote_params.DropCopyDropCopyQuoteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyQuote,
        )

    def drop_copy_quote_request_ack(
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
    ) -> DropCopyRequestAck:
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
            "/api/v2/webhook/pubsub/dropCopy/quoteRequestAck",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_quote_request_ack_params.DropCopyDropCopyQuoteRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyRequestAck,
        )


class AsyncDropCopyResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDropCopyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDropCopyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDropCopyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cyberapper/cadenza-lite-sdk-python#with_streaming_response
        """
        return AsyncDropCopyResourceWithStreamingResponse(self)

    async def drop_copy_cancel_order_request_ack(
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
        payload: CancelOrderRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyCancelOrderRequestAck:
        """
        PubSub event handler placeholder for cancel order request acknowledgment event

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
            "/api/v2/webhook/pubsub/dropCopy/cancelOrderRequestAck",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_cancel_order_request_ack_params.DropCopyDropCopyCancelOrderRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyCancelOrderRequestAck,
        )

    async def drop_copy_execution_report(
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
        payload: ExecutionReportParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyExecutionReport:
        """
        PubSub event handler for execution report drop copy event

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
            "/api/v2/webhook/pubsub/dropCopy/executionReport",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_execution_report_params.DropCopyDropCopyExecutionReportParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyExecutionReport,
        )

    async def drop_copy_order(
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
        payload: OrderParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyOrder:
        """
        PubSub event handler placeholder for order event

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
            "/api/v2/webhook/pubsub/dropCopy/order",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_order_params.DropCopyDropCopyOrderParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyOrder,
        )

    async def drop_copy_place_order_request_ack(
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
        payload: PlaceOrderRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyPlaceOrderRequestAck:
        """
        PubSub event handler placeholder for place order request acknowledgment event

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
            "/api/v2/webhook/pubsub/dropCopy/placeOrderRequestAck",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_place_order_request_ack_params.DropCopyDropCopyPlaceOrderRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyPlaceOrderRequestAck,
        )

    async def drop_copy_portfolio(
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
        payload: ExchangeAccountPortfolioParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyPortfolio:
        """
        PubSub event handler placeholder for portfolio event

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
            "/api/v2/webhook/pubsub/dropCopy/portfolio",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_portfolio_params.DropCopyDropCopyPortfolioParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyPortfolio,
        )

    async def drop_copy_quote(
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
        payload: QuoteParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyQuote:
        """
        PubSub event handler placeholder for quote event

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
            "/api/v2/webhook/pubsub/dropCopy/quote",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_quote_params.DropCopyDropCopyQuoteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyQuote,
        )

    async def drop_copy_quote_request_ack(
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
    ) -> DropCopyRequestAck:
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
            "/api/v2/webhook/pubsub/dropCopy/quoteRequestAck",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                drop_copy_drop_copy_quote_request_ack_params.DropCopyDropCopyQuoteRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyRequestAck,
        )


class DropCopyResourceWithRawResponse:
    def __init__(self, drop_copy: DropCopyResource) -> None:
        self._drop_copy = drop_copy

        self.drop_copy_cancel_order_request_ack = to_raw_response_wrapper(
            drop_copy.drop_copy_cancel_order_request_ack,
        )
        self.drop_copy_execution_report = to_raw_response_wrapper(
            drop_copy.drop_copy_execution_report,
        )
        self.drop_copy_order = to_raw_response_wrapper(
            drop_copy.drop_copy_order,
        )
        self.drop_copy_place_order_request_ack = to_raw_response_wrapper(
            drop_copy.drop_copy_place_order_request_ack,
        )
        self.drop_copy_portfolio = to_raw_response_wrapper(
            drop_copy.drop_copy_portfolio,
        )
        self.drop_copy_quote = to_raw_response_wrapper(
            drop_copy.drop_copy_quote,
        )
        self.drop_copy_quote_request_ack = to_raw_response_wrapper(
            drop_copy.drop_copy_quote_request_ack,
        )


class AsyncDropCopyResourceWithRawResponse:
    def __init__(self, drop_copy: AsyncDropCopyResource) -> None:
        self._drop_copy = drop_copy

        self.drop_copy_cancel_order_request_ack = async_to_raw_response_wrapper(
            drop_copy.drop_copy_cancel_order_request_ack,
        )
        self.drop_copy_execution_report = async_to_raw_response_wrapper(
            drop_copy.drop_copy_execution_report,
        )
        self.drop_copy_order = async_to_raw_response_wrapper(
            drop_copy.drop_copy_order,
        )
        self.drop_copy_place_order_request_ack = async_to_raw_response_wrapper(
            drop_copy.drop_copy_place_order_request_ack,
        )
        self.drop_copy_portfolio = async_to_raw_response_wrapper(
            drop_copy.drop_copy_portfolio,
        )
        self.drop_copy_quote = async_to_raw_response_wrapper(
            drop_copy.drop_copy_quote,
        )
        self.drop_copy_quote_request_ack = async_to_raw_response_wrapper(
            drop_copy.drop_copy_quote_request_ack,
        )


class DropCopyResourceWithStreamingResponse:
    def __init__(self, drop_copy: DropCopyResource) -> None:
        self._drop_copy = drop_copy

        self.drop_copy_cancel_order_request_ack = to_streamed_response_wrapper(
            drop_copy.drop_copy_cancel_order_request_ack,
        )
        self.drop_copy_execution_report = to_streamed_response_wrapper(
            drop_copy.drop_copy_execution_report,
        )
        self.drop_copy_order = to_streamed_response_wrapper(
            drop_copy.drop_copy_order,
        )
        self.drop_copy_place_order_request_ack = to_streamed_response_wrapper(
            drop_copy.drop_copy_place_order_request_ack,
        )
        self.drop_copy_portfolio = to_streamed_response_wrapper(
            drop_copy.drop_copy_portfolio,
        )
        self.drop_copy_quote = to_streamed_response_wrapper(
            drop_copy.drop_copy_quote,
        )
        self.drop_copy_quote_request_ack = to_streamed_response_wrapper(
            drop_copy.drop_copy_quote_request_ack,
        )


class AsyncDropCopyResourceWithStreamingResponse:
    def __init__(self, drop_copy: AsyncDropCopyResource) -> None:
        self._drop_copy = drop_copy

        self.drop_copy_cancel_order_request_ack = async_to_streamed_response_wrapper(
            drop_copy.drop_copy_cancel_order_request_ack,
        )
        self.drop_copy_execution_report = async_to_streamed_response_wrapper(
            drop_copy.drop_copy_execution_report,
        )
        self.drop_copy_order = async_to_streamed_response_wrapper(
            drop_copy.drop_copy_order,
        )
        self.drop_copy_place_order_request_ack = async_to_streamed_response_wrapper(
            drop_copy.drop_copy_place_order_request_ack,
        )
        self.drop_copy_portfolio = async_to_streamed_response_wrapper(
            drop_copy.drop_copy_portfolio,
        )
        self.drop_copy_quote = async_to_streamed_response_wrapper(
            drop_copy.drop_copy_quote,
        )
        self.drop_copy_quote_request_ack = async_to_streamed_response_wrapper(
            drop_copy.drop_copy_quote_request_ack,
        )
