# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .balance_entry import BalanceEntry
from .position_entry import PositionEntry
from .exchange_account_credit import ExchangeAccountCredit

__all__ = ["ExchangeAccountPortfolio"]


class ExchangeAccountPortfolio(BaseModel):
    credit: ExchangeAccountCredit
    """Exchange Account Credit Info"""

    exchange_account_id: str = FieldInfo(alias="exchangeAccountId")
    """The unique identifier for the account."""

    exchange_type: Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"] = FieldInfo(
        alias="exchangeType"
    )
    """Exchange type"""

    updated_at: int = FieldInfo(alias="updatedAt")
    """The timestamp when the portfolio information was updated."""

    balances: Optional[List[BalanceEntry]] = None

    positions: Optional[List[PositionEntry]] = None
