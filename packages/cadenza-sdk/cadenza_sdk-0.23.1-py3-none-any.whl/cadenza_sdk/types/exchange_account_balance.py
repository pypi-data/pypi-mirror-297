# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .balance_entry import BalanceEntry

__all__ = ["ExchangeAccountBalance"]


class ExchangeAccountBalance(BaseModel):
    balances: List[BalanceEntry]
    """List of balances"""

    exchange_account_id: str = FieldInfo(alias="exchangeAccountId")
    """Exchange account ID"""
