# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..exchange_account_portfolio import ExchangeAccountPortfolio

__all__ = ["DropCopyPortfolio"]


class DropCopyPortfolio(BaseModel):
    event_id: str = FieldInfo(alias="eventId")
    """A unique identifier for the event."""

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
    ] = FieldInfo(alias="eventType")
    """Event Type"""

    timestamp: int
    """Unix timestamp in milliseconds when the event was generated."""

    payload: Optional[ExchangeAccountPortfolio] = None

    source: Optional[str] = None
    """The source system or module that generated the event."""
