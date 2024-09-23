# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from .._models import BaseModel

__all__ = ["BalanceEntry"]


class BalanceEntry(BaseModel):
    asset: str
    """Asset"""

    borrowed: float
    """Borrowed balance from exchange"""

    free: float
    """Free balance"""

    locked: float
    """Locked balance"""

    net: float
    """Net Balance, net = total - borrowed"""

    total: float
    """Total available balance"""
