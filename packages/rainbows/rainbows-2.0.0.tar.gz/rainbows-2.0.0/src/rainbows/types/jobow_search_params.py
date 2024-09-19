# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import TypedDict

__all__ = ["JobowSearchParams", "TitleSearchCriterion"]


class JobowSearchParams(TypedDict, total=False):
    board_url_contains: Optional[str]
    """Selects for all board urls which contain it"""

    board_urls: Optional[List[str]]
    """Board urls to search"""

    countries: Optional[List[str]]
    """List of countries to filter jobs"""

    description_include_mode: str
    """Mode for combining description include keywords: 'and' or 'or'"""

    description_keywords_exclude: Optional[List[str]]
    """Keywords to exclude from description search"""

    description_keywords_include: Optional[List[str]]
    """Keywords to include in description search"""

    last_scraped_date_end: Optional[str]
    """End date for last_scraped_date column (format: YYYY-MM-DD)"""

    last_scraped_date_start: Optional[str]
    """Start date for last_scraped_date column (format: YYYY-MM-DD)"""

    null_columns: Optional[List[str]]
    """List of columns that should be null"""

    page_number: int
    """Page number for pagination"""

    page_size: int
    """Number of results per page"""

    title_criteria_combination_mode: str
    """
    Mode for combining title search criteria, in the case of more than one criteria.
    """

    title_search_criteria: Optional[Iterable[TitleSearchCriterion]]
    """List of criteria applied to the title."""

    urls: Optional[List[str]]
    """Specific job urls to fetch. If not `None`, all other parameters are ignored."""


class TitleSearchCriterion(TypedDict, total=False):
    exclude: Optional[List[str]]
    """Keywords to exclude from the title search"""

    include: Optional[List[str]]
    """Keywords to include in the title search"""

    mode: str
    """Mode for combining the inclusion keywords: 'and' or 'or'"""
