# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import TypedDict

__all__ = ["JobRetrieveJobsParams", "TitleSearchCriterion"]


class JobRetrieveJobsParams(TypedDict, total=False):
    board_url_contains: Optional[str]

    board_urls: Optional[List[str]]

    countries: Optional[List[str]]

    description_include_mode: str

    description_keywords_exclude: Optional[List[str]]

    description_keywords_include: Optional[List[str]]

    last_scraped_date_end: Optional[str]

    last_scraped_date_start: Optional[str]

    null_columns: Optional[List[str]]

    page_number: int

    page_size: int

    title_criteria_combination_mode: str

    title_search_criteria: Optional[Iterable[TitleSearchCriterion]]

    urls: Optional[List[str]]


class TitleSearchCriterion(TypedDict, total=False):
    exclude: Optional[List[str]]

    include: Optional[List[str]]

    mode: str
