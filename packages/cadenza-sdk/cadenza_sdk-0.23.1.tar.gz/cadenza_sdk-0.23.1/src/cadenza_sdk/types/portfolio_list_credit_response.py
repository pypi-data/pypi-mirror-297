# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .exchange_account_credit import ExchangeAccountCredit

__all__ = ["PortfolioListCreditResponse"]

PortfolioListCreditResponse: TypeAlias = List[ExchangeAccountCredit]
