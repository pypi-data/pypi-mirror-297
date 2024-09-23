# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .orderbook import Orderbook

__all__ = ["OrderbookGetResponse"]

OrderbookGetResponse: TypeAlias = List[Orderbook]
