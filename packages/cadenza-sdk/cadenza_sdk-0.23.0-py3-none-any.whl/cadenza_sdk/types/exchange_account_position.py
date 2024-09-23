# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .position_entry import PositionEntry

__all__ = ["ExchangeAccountPosition"]


class ExchangeAccountPosition(BaseModel):
    exchange_account_id: Optional[str] = FieldInfo(alias="exchangeAccountId", default=None)
    """Exchange account ID"""

    positions: Optional[List[PositionEntry]] = None
    """List of positions"""
