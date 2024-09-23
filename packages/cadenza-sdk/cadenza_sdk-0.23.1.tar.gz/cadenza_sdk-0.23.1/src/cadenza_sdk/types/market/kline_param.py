# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo
from ..balance_entry_param import BalanceEntryParam

__all__ = ["KlineParam"]


class KlineParam(TypedDict, total=False):
    candles: Iterable[BalanceEntryParam]

    exchange_account_id: Annotated[str, PropertyInfo(alias="exchangeAccountId")]
    """The unique identifier for the account."""

    exchange_type: Annotated[
        Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"],
        PropertyInfo(alias="exchangeType"),
    ]
    """Exchange type"""

    interval: Literal["1s", "1m", "5m", "15m", "30m", "1h", "2h", "1d", "1w"]

    symbol: str
