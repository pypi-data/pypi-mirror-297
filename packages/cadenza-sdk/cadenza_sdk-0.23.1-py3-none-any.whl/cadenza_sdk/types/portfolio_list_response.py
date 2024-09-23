# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .exchange_account_portfolio import ExchangeAccountPortfolio

__all__ = ["PortfolioListResponse"]

PortfolioListResponse: TypeAlias = List[ExchangeAccountPortfolio]
