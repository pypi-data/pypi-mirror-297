# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PositionEntryParam"]


class PositionEntryParam(TypedDict, total=False):
    amount: Required[float]
    """Amount"""

    position_side: Required[Annotated[Literal["LONG", "SHORT"], PropertyInfo(alias="positionSide")]]
    """Position side"""

    status: Required[Literal["OPEN"]]
    """Status"""

    symbol: Required[str]
    """Symbol"""

    cost: float
    """Cost"""

    entry_price: Annotated[float, PropertyInfo(alias="entryPrice")]
    """Entry price"""
