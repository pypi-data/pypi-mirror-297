# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .exchange_account_position import ExchangeAccountPosition

__all__ = ["PortfolioListPositionsResponse"]

PortfolioListPositionsResponse: TypeAlias = List[ExchangeAccountPosition]
