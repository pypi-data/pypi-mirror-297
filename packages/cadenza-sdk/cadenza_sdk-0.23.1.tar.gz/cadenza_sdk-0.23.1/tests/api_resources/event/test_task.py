# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import Cadenza, AsyncCadenza
from tests.utils import assert_matches_type
from cadenza_sdk.types.event import TaskQuote

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTask:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_task_quote(self, client: Cadenza) -> None:
        task = client.event.task.task_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(TaskQuote, task, path=["response"])

    @parametrize
    def test_method_task_quote_with_all_params(self, client: Cadenza) -> None:
        task = client.event.task.task_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "base_currency": "baseCurrency",
                "order_side": "orderSide",
                "quote_currency": "quoteCurrency",
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "quantity": 0,
                "quote_quantity": 0,
            },
            source="source",
        )
        assert_matches_type(TaskQuote, task, path=["response"])

    @parametrize
    def test_raw_response_task_quote(self, client: Cadenza) -> None:
        response = client.event.task.with_raw_response.task_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskQuote, task, path=["response"])

    @parametrize
    def test_streaming_response_task_quote(self, client: Cadenza) -> None:
        with client.event.task.with_streaming_response.task_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskQuote, task, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTask:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_task_quote(self, async_client: AsyncCadenza) -> None:
        task = await async_client.event.task.task_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(TaskQuote, task, path=["response"])

    @parametrize
    async def test_method_task_quote_with_all_params(self, async_client: AsyncCadenza) -> None:
        task = await async_client.event.task.task_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "base_currency": "baseCurrency",
                "order_side": "orderSide",
                "quote_currency": "quoteCurrency",
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "quantity": 0,
                "quote_quantity": 0,
            },
            source="source",
        )
        assert_matches_type(TaskQuote, task, path=["response"])

    @parametrize
    async def test_raw_response_task_quote(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.task.with_raw_response.task_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskQuote, task, path=["response"])

    @parametrize
    async def test_streaming_response_task_quote(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.task.with_streaming_response.task_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskQuote, task, path=["response"])

        assert cast(Any, response.is_closed) is True
