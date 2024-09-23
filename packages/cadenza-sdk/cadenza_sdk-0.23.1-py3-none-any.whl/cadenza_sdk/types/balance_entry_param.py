# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["BalanceEntryParam"]


class BalanceEntryParam(TypedDict, total=False):
    asset: Required[str]
    """Asset"""

    borrowed: Required[float]
    """Borrowed balance from exchange"""

    free: Required[float]
    """Free balance"""

    locked: Required[float]
    """Locked balance"""

    net: Required[float]
    """Net Balance, net = total - borrowed"""

    total: Required[float]
    """Total available balance"""
