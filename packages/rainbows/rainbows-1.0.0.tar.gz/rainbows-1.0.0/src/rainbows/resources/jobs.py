# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional

import httpx

from ..types import job_retrieve_jobs_params
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
from ..types.job_retrieve_jobs_response import JobRetrieveJobsResponse

__all__ = ["JobsResource", "AsyncJobsResource"]


class JobsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> JobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/pilfo/rainbows#accessing-raw-response-data-eg-headers
        """
        return JobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> JobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/pilfo/rainbows#with_streaming_response
        """
        return JobsResourceWithStreamingResponse(self)

    def retrieve_jobs(
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
        title_search_criteria: Optional[Iterable[job_retrieve_jobs_params.TitleSearchCriterion]] | NotGiven = NOT_GIVEN,
        urls: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JobRetrieveJobsResponse:
        """
        Api Get Jobs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/get_jobs",
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
                job_retrieve_jobs_params.JobRetrieveJobsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=JobRetrieveJobsResponse,
        )


class AsyncJobsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncJobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/pilfo/rainbows#accessing-raw-response-data-eg-headers
        """
        return AsyncJobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncJobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/pilfo/rainbows#with_streaming_response
        """
        return AsyncJobsResourceWithStreamingResponse(self)

    async def retrieve_jobs(
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
        title_search_criteria: Optional[Iterable[job_retrieve_jobs_params.TitleSearchCriterion]] | NotGiven = NOT_GIVEN,
        urls: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JobRetrieveJobsResponse:
        """
        Api Get Jobs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/get_jobs",
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
                job_retrieve_jobs_params.JobRetrieveJobsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=JobRetrieveJobsResponse,
        )


class JobsResourceWithRawResponse:
    def __init__(self, jobs: JobsResource) -> None:
        self._jobs = jobs

        self.retrieve_jobs = to_raw_response_wrapper(
            jobs.retrieve_jobs,
        )


class AsyncJobsResourceWithRawResponse:
    def __init__(self, jobs: AsyncJobsResource) -> None:
        self._jobs = jobs

        self.retrieve_jobs = async_to_raw_response_wrapper(
            jobs.retrieve_jobs,
        )


class JobsResourceWithStreamingResponse:
    def __init__(self, jobs: JobsResource) -> None:
        self._jobs = jobs

        self.retrieve_jobs = to_streamed_response_wrapper(
            jobs.retrieve_jobs,
        )


class AsyncJobsResourceWithStreamingResponse:
    def __init__(self, jobs: AsyncJobsResource) -> None:
        self._jobs = jobs

        self.retrieve_jobs = async_to_streamed_response_wrapper(
            jobs.retrieve_jobs,
        )
