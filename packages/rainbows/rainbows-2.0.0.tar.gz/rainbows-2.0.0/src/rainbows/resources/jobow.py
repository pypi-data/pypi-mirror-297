# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional

import httpx

from ..types import jobow_search_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.jobow_search_response import JobowSearchResponse

__all__ = ["JobowResource", "AsyncJobowResource"]


class JobowResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> JobowResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/pilfo/rainbows#accessing-raw-response-data-eg-headers
        """
        return JobowResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> JobowResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/pilfo/rainbows#with_streaming_response
        """
        return JobowResourceWithStreamingResponse(self)

    def search(
        self,
        *,
        board_url_contains: Optional[str] | NotGiven = NOT_GIVEN,
        board_urls: Optional[List[str]] | NotGiven = NOT_GIVEN,
        countries: Optional[List[str]] | NotGiven = NOT_GIVEN,
        description_include_mode: str | NotGiven = NOT_GIVEN,
        description_keywords_exclude: Optional[List[str]] | NotGiven = NOT_GIVEN,
        description_keywords_include: Optional[List[str]] | NotGiven = NOT_GIVEN,
        last_scraped_date_end: Optional[str] | NotGiven = NOT_GIVEN,
        last_scraped_date_start: Optional[str] | NotGiven = NOT_GIVEN,
        null_columns: Optional[List[str]] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        title_criteria_combination_mode: str | NotGiven = NOT_GIVEN,
        title_search_criteria: Optional[Iterable[jobow_search_params.TitleSearchCriterion]] | NotGiven = NOT_GIVEN,
        urls: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JobowSearchResponse:
        """
        Search for jobs based on various criteria.

        This endpoint allows you to search for jobs using multiple parameters such as
        board URLs, job titles, descriptions, and more. The results are paginated for
        easier navigation.

        Args:
          board_url_contains: Selects for all board urls which contain it

          board_urls: Board urls to search

          countries: List of countries to filter jobs

          description_include_mode: Mode for combining description include keywords: 'and' or 'or'

          description_keywords_exclude: Keywords to exclude from description search

          description_keywords_include: Keywords to include in description search

          last_scraped_date_end: End date for last_scraped_date column (format: YYYY-MM-DD)

          last_scraped_date_start: Start date for last_scraped_date column (format: YYYY-MM-DD)

          null_columns: List of columns that should be null

          page_number: Page number for pagination

          page_size: Number of results per page

          title_criteria_combination_mode: Mode for combining title search criteria, in the case of more than one criteria.

          title_search_criteria: List of criteria applied to the title.

          urls: Specific job urls to fetch. If not `None`, all other parameters are ignored.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/jobow/search",
            body=maybe_transform(
                {
                    "board_url_contains": board_url_contains,
                    "board_urls": board_urls,
                    "countries": countries,
                    "description_include_mode": description_include_mode,
                    "description_keywords_exclude": description_keywords_exclude,
                    "description_keywords_include": description_keywords_include,
                    "last_scraped_date_end": last_scraped_date_end,
                    "last_scraped_date_start": last_scraped_date_start,
                    "null_columns": null_columns,
                    "page_number": page_number,
                    "page_size": page_size,
                    "title_criteria_combination_mode": title_criteria_combination_mode,
                    "title_search_criteria": title_search_criteria,
                    "urls": urls,
                },
                jobow_search_params.JobowSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=JobowSearchResponse,
        )


class AsyncJobowResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncJobowResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/pilfo/rainbows#accessing-raw-response-data-eg-headers
        """
        return AsyncJobowResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncJobowResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/pilfo/rainbows#with_streaming_response
        """
        return AsyncJobowResourceWithStreamingResponse(self)

    async def search(
        self,
        *,
        board_url_contains: Optional[str] | NotGiven = NOT_GIVEN,
        board_urls: Optional[List[str]] | NotGiven = NOT_GIVEN,
        countries: Optional[List[str]] | NotGiven = NOT_GIVEN,
        description_include_mode: str | NotGiven = NOT_GIVEN,
        description_keywords_exclude: Optional[List[str]] | NotGiven = NOT_GIVEN,
        description_keywords_include: Optional[List[str]] | NotGiven = NOT_GIVEN,
        last_scraped_date_end: Optional[str] | NotGiven = NOT_GIVEN,
        last_scraped_date_start: Optional[str] | NotGiven = NOT_GIVEN,
        null_columns: Optional[List[str]] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        title_criteria_combination_mode: str | NotGiven = NOT_GIVEN,
        title_search_criteria: Optional[Iterable[jobow_search_params.TitleSearchCriterion]] | NotGiven = NOT_GIVEN,
        urls: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JobowSearchResponse:
        """
        Search for jobs based on various criteria.

        This endpoint allows you to search for jobs using multiple parameters such as
        board URLs, job titles, descriptions, and more. The results are paginated for
        easier navigation.

        Args:
          board_url_contains: Selects for all board urls which contain it

          board_urls: Board urls to search

          countries: List of countries to filter jobs

          description_include_mode: Mode for combining description include keywords: 'and' or 'or'

          description_keywords_exclude: Keywords to exclude from description search

          description_keywords_include: Keywords to include in description search

          last_scraped_date_end: End date for last_scraped_date column (format: YYYY-MM-DD)

          last_scraped_date_start: Start date for last_scraped_date column (format: YYYY-MM-DD)

          null_columns: List of columns that should be null

          page_number: Page number for pagination

          page_size: Number of results per page

          title_criteria_combination_mode: Mode for combining title search criteria, in the case of more than one criteria.

          title_search_criteria: List of criteria applied to the title.

          urls: Specific job urls to fetch. If not `None`, all other parameters are ignored.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/jobow/search",
            body=await async_maybe_transform(
                {
                    "board_url_contains": board_url_contains,
                    "board_urls": board_urls,
                    "countries": countries,
                    "description_include_mode": description_include_mode,
                    "description_keywords_exclude": description_keywords_exclude,
                    "description_keywords_include": description_keywords_include,
                    "last_scraped_date_end": last_scraped_date_end,
                    "last_scraped_date_start": last_scraped_date_start,
                    "null_columns": null_columns,
                    "page_number": page_number,
                    "page_size": page_size,
                    "title_criteria_combination_mode": title_criteria_combination_mode,
                    "title_search_criteria": title_search_criteria,
                    "urls": urls,
                },
                jobow_search_params.JobowSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=JobowSearchResponse,
        )


class JobowResourceWithRawResponse:
    def __init__(self, jobow: JobowResource) -> None:
        self._jobow = jobow

        self.search = to_raw_response_wrapper(
            jobow.search,
        )


class AsyncJobowResourceWithRawResponse:
    def __init__(self, jobow: AsyncJobowResource) -> None:
        self._jobow = jobow

        self.search = async_to_raw_response_wrapper(
            jobow.search,
        )


class JobowResourceWithStreamingResponse:
    def __init__(self, jobow: JobowResource) -> None:
        self._jobow = jobow

        self.search = to_streamed_response_wrapper(
            jobow.search,
        )


class AsyncJobowResourceWithStreamingResponse:
    def __init__(self, jobow: AsyncJobowResource) -> None:
        self._jobow = jobow

        self.search = async_to_streamed_response_wrapper(
            jobow.search,
        )
