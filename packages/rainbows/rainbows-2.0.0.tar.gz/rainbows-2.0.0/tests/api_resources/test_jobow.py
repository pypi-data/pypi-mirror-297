# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from rainbows import Rainbows, AsyncRainbows
from tests.utils import assert_matches_type
from rainbows.types import JobowSearchResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestJobow:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_search(self, client: Rainbows) -> None:
        jobow = client.jobow.search()
        assert_matches_type(JobowSearchResponse, jobow, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: Rainbows) -> None:
        jobow = client.jobow.search(
            board_url_contains="board_url_contains",
            board_urls=["string", "string", "string"],
            countries=["string", "string", "string"],
            description_include_mode="description_include_mode",
            description_keywords_exclude=["string", "string", "string"],
            description_keywords_include=["string", "string", "string"],
            last_scraped_date_end="last_scraped_date_end",
            last_scraped_date_start="last_scraped_date_start",
            null_columns=["string", "string", "string"],
            page_number=0,
            page_size=0,
            title_criteria_combination_mode="title_criteria_combination_mode",
            title_search_criteria=[
                {
                    "exclude": ["string", "string", "string"],
                    "include": ["string", "string", "string"],
                    "mode": "mode",
                },
                {
                    "exclude": ["string", "string", "string"],
                    "include": ["string", "string", "string"],
                    "mode": "mode",
                },
                {
                    "exclude": ["string", "string", "string"],
                    "include": ["string", "string", "string"],
                    "mode": "mode",
                },
            ],
            urls=["string", "string", "string"],
        )
        assert_matches_type(JobowSearchResponse, jobow, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: Rainbows) -> None:
        response = client.jobow.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        jobow = response.parse()
        assert_matches_type(JobowSearchResponse, jobow, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: Rainbows) -> None:
        with client.jobow.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            jobow = response.parse()
            assert_matches_type(JobowSearchResponse, jobow, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncJobow:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_search(self, async_client: AsyncRainbows) -> None:
        jobow = await async_client.jobow.search()
        assert_matches_type(JobowSearchResponse, jobow, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncRainbows) -> None:
        jobow = await async_client.jobow.search(
            board_url_contains="board_url_contains",
            board_urls=["string", "string", "string"],
            countries=["string", "string", "string"],
            description_include_mode="description_include_mode",
            description_keywords_exclude=["string", "string", "string"],
            description_keywords_include=["string", "string", "string"],
            last_scraped_date_end="last_scraped_date_end",
            last_scraped_date_start="last_scraped_date_start",
            null_columns=["string", "string", "string"],
            page_number=0,
            page_size=0,
            title_criteria_combination_mode="title_criteria_combination_mode",
            title_search_criteria=[
                {
                    "exclude": ["string", "string", "string"],
                    "include": ["string", "string", "string"],
                    "mode": "mode",
                },
                {
                    "exclude": ["string", "string", "string"],
                    "include": ["string", "string", "string"],
                    "mode": "mode",
                },
                {
                    "exclude": ["string", "string", "string"],
                    "include": ["string", "string", "string"],
                    "mode": "mode",
                },
            ],
            urls=["string", "string", "string"],
        )
        assert_matches_type(JobowSearchResponse, jobow, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncRainbows) -> None:
        response = await async_client.jobow.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        jobow = await response.parse()
        assert_matches_type(JobowSearchResponse, jobow, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncRainbows) -> None:
        async with async_client.jobow.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            jobow = await response.parse()
            assert_matches_type(JobowSearchResponse, jobow, path=["response"])

        assert cast(Any, response.is_closed) is True
