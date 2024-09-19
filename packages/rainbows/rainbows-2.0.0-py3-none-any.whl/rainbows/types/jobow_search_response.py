# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["JobowSearchResponse", "Job"]


class Job(BaseModel):
    url: str

    board_url: Optional[str] = None

    countries: Optional[List[str]] = None

    description: Optional[str] = None

    last_scraped_date: Optional[str] = None

    location: Optional[str] = None

    title: Optional[str] = None


class JobowSearchResponse(BaseModel):
    jobs: List[Job]
    """List of jobs matching the search criteria"""

    pagination: object
    """Pagination information"""
