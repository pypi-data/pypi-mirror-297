# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .balance_entry_param import BalanceEntryParam
from .position_entry_param import PositionEntryParam
from .exchange_account_credit_param import ExchangeAccountCreditParam

__all__ = ["ExchangeAccountPortfolioParam"]


class ExchangeAccountPortfolioParam(TypedDict, total=False):
    credit: Required[ExchangeAccountCreditParam]
    """Exchange Account Credit Info"""

    exchange_account_id: Required[Annotated[str, PropertyInfo(alias="exchangeAccountId")]]
    """The unique identifier for the account."""

    exchange_type: Required[
        Annotated[
            Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"],
            PropertyInfo(alias="exchangeType"),
        ]
    ]
    """Exchange type"""

    updated_at: Required[Annotated[int, PropertyInfo(alias="updatedAt")]]
    """The timestamp when the portfolio information was updated."""

    balances: Iterable[BalanceEntryParam]

    positions: Iterable[PositionEntryParam]
