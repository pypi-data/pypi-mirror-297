# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["PositionEntry"]


class PositionEntry(BaseModel):
    amount: float
    """Amount"""

    position_side: Literal["LONG", "SHORT"] = FieldInfo(alias="positionSide")
    """Position side"""

    status: Literal["OPEN"]
    """Status"""

    symbol: str
    """Symbol"""

    cost: Optional[float] = None
    """Cost"""

    entry_price: Optional[float] = FieldInfo(alias="entryPrice", default=None)
    """Entry price"""
