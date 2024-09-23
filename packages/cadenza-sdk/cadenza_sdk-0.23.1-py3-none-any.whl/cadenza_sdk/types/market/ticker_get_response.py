# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .ticker import Ticker

__all__ = ["TickerGetResponse"]

TickerGetResponse: TypeAlias = List[Ticker]
