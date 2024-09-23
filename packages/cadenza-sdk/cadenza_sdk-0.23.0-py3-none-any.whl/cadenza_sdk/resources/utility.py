# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["UtilityResource", "AsyncUtilityResource"]


class UtilityResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UtilityResourceWithRawResponse:
        return UtilityResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UtilityResourceWithStreamingResponse:
        return UtilityResourceWithStreamingResponse(self)

    def health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """Health check"""
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return self._get(
            "/api/v2/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class AsyncUtilityResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUtilityResourceWithRawResponse:
        return AsyncUtilityResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUtilityResourceWithStreamingResponse:
        return AsyncUtilityResourceWithStreamingResponse(self)

    async def health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """Health check"""
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return await self._get(
            "/api/v2/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class UtilityResourceWithRawResponse:
    def __init__(self, utility: UtilityResource) -> None:
        self._utility = utility

        self.health = to_raw_response_wrapper(
            utility.health,
        )


class AsyncUtilityResourceWithRawResponse:
    def __init__(self, utility: AsyncUtilityResource) -> None:
        self._utility = utility

        self.health = async_to_raw_response_wrapper(
            utility.health,
        )


class UtilityResourceWithStreamingResponse:
    def __init__(self, utility: UtilityResource) -> None:
        self._utility = utility

        self.health = to_streamed_response_wrapper(
            utility.health,
        )


class AsyncUtilityResourceWithStreamingResponse:
    def __init__(self, utility: AsyncUtilityResource) -> None:
        self._utility = utility

        self.health = async_to_streamed_response_wrapper(
            utility.health,
        )
