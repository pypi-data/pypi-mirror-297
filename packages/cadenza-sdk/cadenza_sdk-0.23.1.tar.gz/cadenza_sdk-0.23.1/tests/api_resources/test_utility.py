# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import Cadenza, AsyncCadenza
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUtility:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_health(self, client: Cadenza) -> None:
        utility = client.utility.health()
        assert_matches_type(str, utility, path=["response"])

    @parametrize
    def test_raw_response_health(self, client: Cadenza) -> None:
        response = client.utility.with_raw_response.health()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        utility = response.parse()
        assert_matches_type(str, utility, path=["response"])

    @parametrize
    def test_streaming_response_health(self, client: Cadenza) -> None:
        with client.utility.with_streaming_response.health() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            utility = response.parse()
            assert_matches_type(str, utility, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUtility:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_health(self, async_client: AsyncCadenza) -> None:
        utility = await async_client.utility.health()
        assert_matches_type(str, utility, path=["response"])

    @parametrize
    async def test_raw_response_health(self, async_client: AsyncCadenza) -> None:
        response = await async_client.utility.with_raw_response.health()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        utility = await response.parse()
        assert_matches_type(str, utility, path=["response"])

    @parametrize
    async def test_streaming_response_health(self, async_client: AsyncCadenza) -> None:
        async with async_client.utility.with_streaming_response.health() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            utility = await response.parse()
            assert_matches_type(str, utility, path=["response"])

        assert cast(Any, response.is_closed) is True
