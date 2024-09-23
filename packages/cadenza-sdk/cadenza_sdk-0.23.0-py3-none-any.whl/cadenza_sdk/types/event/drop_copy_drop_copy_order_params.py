# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from ..trading.order_param import OrderParam

__all__ = ["DropCopyDropCopyOrderParams"]


class DropCopyDropCopyOrderParams(TypedDict, total=False):
    event_id: Required[Annotated[str, PropertyInfo(alias="eventId")]]
    """A unique identifier for the event."""

    event_type: Required[
        Annotated[
            Literal[
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
            PropertyInfo(alias="eventType"),
        ]
    ]
    """Event Type"""

    timestamp: Required[int]
    """Unix timestamp in milliseconds when the event was generated."""

    payload: OrderParam

    source: str
    """The source system or module that generated the event."""
