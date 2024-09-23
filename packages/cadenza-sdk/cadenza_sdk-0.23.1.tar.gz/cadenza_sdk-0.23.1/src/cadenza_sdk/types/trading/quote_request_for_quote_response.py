# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .quote import Quote

__all__ = ["QuoteRequestForQuoteResponse"]

QuoteRequestForQuoteResponse: TypeAlias = List[Quote]
