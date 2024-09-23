# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import Cadenza, AsyncCadenza
from tests.utils import assert_matches_type
from cadenza_sdk.types.event import (
    DropCopyOrder,
    DropCopyQuote,
    DropCopyPortfolio,
    DropCopyRequestAck,
    DropCopyExecutionReport,
    DropCopyPlaceOrderRequestAck,
    DropCopyCancelOrderRequestAck,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDropCopy:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_drop_copy_cancel_order_request_ack(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyCancelOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_cancel_order_request_ack_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={"order_id": "orderId"},
            source="source",
        )
        assert_matches_type(DropCopyCancelOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_cancel_order_request_ack(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyCancelOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_cancel_order_request_ack(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyCancelOrderRequestAck, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_execution_report(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_execution_report_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "base_currency": "BTC",
                "cost": 42859.99,
                "created_at": 1632933600000,
                "filled": 1,
                "quote_currency": "USDT",
                "route_policy": "PRIORITY",
                "status": "SUBMITTED",
                "updated_at": 1632933600000,
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "executions": [
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "exchange_type": "BINANCE",
                        "filled": 0,
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "base_currency": "BTC",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quote_currency": "USDT",
                        "quote_quantity": 0,
                        "tenant_id": "tenantId",
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    },
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "exchange_type": "BINANCE",
                        "filled": 0,
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "base_currency": "BTC",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quote_currency": "USDT",
                        "quote_quantity": 0,
                        "tenant_id": "tenantId",
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    },
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "exchange_type": "BINANCE",
                        "filled": 0,
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "base_currency": "BTC",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quote_currency": "USDT",
                        "quote_quantity": 0,
                        "tenant_id": "tenantId",
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    },
                ],
                "fees": [
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                ],
                "order": {
                    "cost": 0,
                    "created_at": 1703052635110,
                    "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "exchange_type": "BINANCE",
                    "filled": 0,
                    "order_side": "BUY",
                    "order_type": "MARKET",
                    "quantity": 0,
                    "status": "SUBMITTED",
                    "symbol": "BTC/USDT",
                    "time_in_force": "DAY",
                    "updated_at": 1703052635111,
                    "base_currency": "BTC",
                    "fee": 0,
                    "fee_currency": "USDT",
                    "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "price": 0,
                    "quote_currency": "USDT",
                    "quote_quantity": 0,
                    "tenant_id": "tenantId",
                    "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                },
            },
            source="source",
        )
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_execution_report(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_execution_report(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_order(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_order_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "cost": 0,
                "created_at": 1703052635110,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
                "filled": 0,
                "order_side": "BUY",
                "order_type": "MARKET",
                "quantity": 0,
                "status": "SUBMITTED",
                "symbol": "BTC/USDT",
                "time_in_force": "DAY",
                "updated_at": 1703052635111,
                "base_currency": "BTC",
                "fee": 0,
                "fee_currency": "USDT",
                "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "price": 0,
                "quote_currency": "USDT",
                "quote_quantity": 0,
                "tenant_id": "tenantId",
                "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            },
            source="source",
        )
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_order(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_order(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_place_order_request_ack(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyPlaceOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_place_order_request_ack_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "route_policy": "PRIORITY",
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "leverage": 0,
                "order_side": "BUY",
                "order_type": "MARKET",
                "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "price": 0,
                "price_slippage_tolerance": 0,
                "priority": ["exchange_account_id_1", "exchange_account_id_2", "exchange_account_id_3"],
                "quantity": 0,
                "quote_id": "quoteId",
                "quote_quantity": 0,
                "quote_request_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "symbol": "BTC/USDT",
                "tenant_id": "tenantId",
                "time_in_force": "DAY",
            },
            source="source",
        )
        assert_matches_type(DropCopyPlaceOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_place_order_request_ack(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyPlaceOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_place_order_request_ack(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyPlaceOrderRequestAck, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_portfolio(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_portfolio_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "credit": {
                    "account_type": "SPOT",
                    "credit": 10000,
                    "currency": "USDT",
                    "exchange_account_id": "018e41a1-cebc-7b49-a729-ae2c1c41e297",
                    "exchange_type": "BINANCE",
                    "leverage": 1,
                    "margin": 5000,
                    "margin_level": 0.89,
                    "margin_loan": 3000,
                    "margin_requirement": 1500,
                    "margin_usage": 0.5,
                    "max_risk_exposure": 5000000,
                    "risk_exposure": 5677517.76,
                    "risk_exposure_rate": 0.89,
                },
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
                "updated_at": 1632933600000,
                "balances": [
                    {
                        "asset": "BTC",
                        "borrowed": 3,
                        "free": 1,
                        "locked": 0,
                        "net": -2,
                        "total": 1,
                    },
                    {
                        "asset": "BTC",
                        "borrowed": 3,
                        "free": 1,
                        "locked": 0,
                        "net": -2,
                        "total": 1,
                    },
                    {
                        "asset": "BTC",
                        "borrowed": 3,
                        "free": 1,
                        "locked": 0,
                        "net": -2,
                        "total": 1,
                    },
                ],
                "positions": [
                    {
                        "amount": 0,
                        "position_side": "LONG",
                        "status": "OPEN",
                        "symbol": "BTC/USDT",
                        "cost": 0,
                        "entry_price": 0,
                    },
                    {
                        "amount": 0,
                        "position_side": "LONG",
                        "status": "OPEN",
                        "symbol": "BTC/USDT",
                        "cost": 0,
                        "entry_price": 0,
                    },
                    {
                        "amount": 0,
                        "position_side": "LONG",
                        "status": "OPEN",
                        "symbol": "BTC/USDT",
                        "cost": 0,
                        "entry_price": 0,
                    },
                ],
            },
            source="source",
        )
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_portfolio(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_portfolio(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_quote(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_quote_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "base_currency": "BTC",
                "quote_currency": "USDT",
                "quote_request_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "timestamp": 1632933600000,
                "valid_until": 1632933600000,
                "ask_price": 42859.99,
                "ask_quantity": 1,
                "bid_price": 42859.71,
                "bid_quantity": 1,
                "created_at": 1632933600000,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
                "expired_at": 1632933600000,
            },
            source="source",
        )
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_quote(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_quote(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_quote_request_ack(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyRequestAck, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_quote_request_ack_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_quote_request_ack(
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
        assert_matches_type(DropCopyRequestAck, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_quote_request_ack(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyRequestAck, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_quote_request_ack(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyRequestAck, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDropCopy:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_drop_copy_cancel_order_request_ack(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyCancelOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_cancel_order_request_ack_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={"order_id": "orderId"},
            source="source",
        )
        assert_matches_type(DropCopyCancelOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_cancel_order_request_ack(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyCancelOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_cancel_order_request_ack(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyCancelOrderRequestAck, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_execution_report(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_execution_report_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "base_currency": "BTC",
                "cost": 42859.99,
                "created_at": 1632933600000,
                "filled": 1,
                "quote_currency": "USDT",
                "route_policy": "PRIORITY",
                "status": "SUBMITTED",
                "updated_at": 1632933600000,
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "executions": [
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "exchange_type": "BINANCE",
                        "filled": 0,
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "base_currency": "BTC",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quote_currency": "USDT",
                        "quote_quantity": 0,
                        "tenant_id": "tenantId",
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    },
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "exchange_type": "BINANCE",
                        "filled": 0,
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "base_currency": "BTC",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quote_currency": "USDT",
                        "quote_quantity": 0,
                        "tenant_id": "tenantId",
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    },
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "exchange_type": "BINANCE",
                        "filled": 0,
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "base_currency": "BTC",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quote_currency": "USDT",
                        "quote_quantity": 0,
                        "tenant_id": "tenantId",
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    },
                ],
                "fees": [
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                ],
                "order": {
                    "cost": 0,
                    "created_at": 1703052635110,
                    "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "exchange_type": "BINANCE",
                    "filled": 0,
                    "order_side": "BUY",
                    "order_type": "MARKET",
                    "quantity": 0,
                    "status": "SUBMITTED",
                    "symbol": "BTC/USDT",
                    "time_in_force": "DAY",
                    "updated_at": 1703052635111,
                    "base_currency": "BTC",
                    "fee": 0,
                    "fee_currency": "USDT",
                    "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "price": 0,
                    "quote_currency": "USDT",
                    "quote_quantity": 0,
                    "tenant_id": "tenantId",
                    "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                },
            },
            source="source",
        )
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_execution_report(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_execution_report(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_order(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_order_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "cost": 0,
                "created_at": 1703052635110,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
                "filled": 0,
                "order_side": "BUY",
                "order_type": "MARKET",
                "quantity": 0,
                "status": "SUBMITTED",
                "symbol": "BTC/USDT",
                "time_in_force": "DAY",
                "updated_at": 1703052635111,
                "base_currency": "BTC",
                "fee": 0,
                "fee_currency": "USDT",
                "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "price": 0,
                "quote_currency": "USDT",
                "quote_quantity": 0,
                "tenant_id": "tenantId",
                "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            },
            source="source",
        )
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_order(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_order(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_place_order_request_ack(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyPlaceOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_place_order_request_ack_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "route_policy": "PRIORITY",
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "leverage": 0,
                "order_side": "BUY",
                "order_type": "MARKET",
                "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "price": 0,
                "price_slippage_tolerance": 0,
                "priority": ["exchange_account_id_1", "exchange_account_id_2", "exchange_account_id_3"],
                "quantity": 0,
                "quote_id": "quoteId",
                "quote_quantity": 0,
                "quote_request_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "symbol": "BTC/USDT",
                "tenant_id": "tenantId",
                "time_in_force": "DAY",
            },
            source="source",
        )
        assert_matches_type(DropCopyPlaceOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_place_order_request_ack(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyPlaceOrderRequestAck, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_place_order_request_ack(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyPlaceOrderRequestAck, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_portfolio(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_portfolio_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "credit": {
                    "account_type": "SPOT",
                    "credit": 10000,
                    "currency": "USDT",
                    "exchange_account_id": "018e41a1-cebc-7b49-a729-ae2c1c41e297",
                    "exchange_type": "BINANCE",
                    "leverage": 1,
                    "margin": 5000,
                    "margin_level": 0.89,
                    "margin_loan": 3000,
                    "margin_requirement": 1500,
                    "margin_usage": 0.5,
                    "max_risk_exposure": 5000000,
                    "risk_exposure": 5677517.76,
                    "risk_exposure_rate": 0.89,
                },
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
                "updated_at": 1632933600000,
                "balances": [
                    {
                        "asset": "BTC",
                        "borrowed": 3,
                        "free": 1,
                        "locked": 0,
                        "net": -2,
                        "total": 1,
                    },
                    {
                        "asset": "BTC",
                        "borrowed": 3,
                        "free": 1,
                        "locked": 0,
                        "net": -2,
                        "total": 1,
                    },
                    {
                        "asset": "BTC",
                        "borrowed": 3,
                        "free": 1,
                        "locked": 0,
                        "net": -2,
                        "total": 1,
                    },
                ],
                "positions": [
                    {
                        "amount": 0,
                        "position_side": "LONG",
                        "status": "OPEN",
                        "symbol": "BTC/USDT",
                        "cost": 0,
                        "entry_price": 0,
                    },
                    {
                        "amount": 0,
                        "position_side": "LONG",
                        "status": "OPEN",
                        "symbol": "BTC/USDT",
                        "cost": 0,
                        "entry_price": 0,
                    },
                    {
                        "amount": 0,
                        "position_side": "LONG",
                        "status": "OPEN",
                        "symbol": "BTC/USDT",
                        "cost": 0,
                        "entry_price": 0,
                    },
                ],
            },
            source="source",
        )
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_portfolio(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_portfolio(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_quote(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_quote_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
            payload={
                "base_currency": "BTC",
                "quote_currency": "USDT",
                "quote_request_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "timestamp": 1632933600000,
                "valid_until": 1632933600000,
                "ask_price": 42859.99,
                "ask_quantity": 1,
                "bid_price": 42859.71,
                "bid_quantity": 1,
                "created_at": 1632933600000,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
                "expired_at": 1632933600000,
            },
            source="source",
        )
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_quote(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_quote(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_quote_request_ack(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyRequestAck, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_quote_request_ack_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_quote_request_ack(
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
        assert_matches_type(DropCopyRequestAck, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_quote_request_ack(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyRequestAck, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_quote_request_ack(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quote",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyRequestAck, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True
