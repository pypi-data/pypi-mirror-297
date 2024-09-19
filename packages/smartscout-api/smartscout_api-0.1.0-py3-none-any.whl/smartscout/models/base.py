# src/smartscout/models/base.py

from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime
from .enums import SortOrder, TextFilterType

T = TypeVar('T')

class ListFilter(BaseModel):
    """Model for list filters."""
    filter: Optional[List[str]] = None

class RangeDecimal(BaseModel):
    """Model for decimal range filters."""
    min: Optional[float] = None
    max: Optional[float] = None

class RangeFilter(BaseModel):
    """Model for general range filters."""
    min: Optional[float] = None
    max: Optional[float] = None

class RangeInt(BaseModel):
    """Model for integer range filters."""
    min: Optional[int] = None
    max: Optional[int] = None

class TextFilter(BaseModel):
    """Model for text filters."""
    type: Optional[TextFilterType] = None
    filter: Optional[str] = None

class DateRangeFilter(BaseModel):
    """Model for date range filters."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class Paging(BaseModel):
    """Model for pagination information."""
    next_page_id: Optional[str] = Field(None, alias="nextPageId")
    has_more_records: bool = Field(..., alias="hasMoreRecords")

class SortOptions(BaseModel):
    """Model for sorting options."""
    by: Optional[str] = Field(None, alias="sort[by]")
    order: Optional[SortOrder] = Field(None, alias="sort[order]")

class PageOptions(BaseModel):
    """Model for pagination options."""
    id: Optional[str] = Field(None, alias="page[id]")
    size: Optional[int] = Field(None, alias="page[size]")

class BaseRequest(BaseModel):
    """Base model for all API requests."""
    marketplace: str

class BaseResponse(BaseModel):
    """Base model for all API responses."""
    pass

class PagedResponse(BaseResponse, Generic[T]):
    """Generic model for paginated API responses."""
    data_count: int
    paging: Paging
    data: Optional[List[T]] = None

class BaseSearchRequest(BaseRequest):
    """Base model for search requests."""
    sort: Optional[SortOptions] = None
    page: Optional[PageOptions] = None

class BaseHistoryRequest(BaseRequest):
    """Base model for history requests."""
    date_range: DateRangeFilter
    sort: Optional[SortOptions] = None
    page: Optional[PageOptions] = None

class Money(BaseModel):
    """Model for monetary values."""
    amount: float
    currency: str

class Dimension(BaseModel):
    """Model for product dimensions."""
    length: float
    width: float
    height: float
    unit: str

class Weight(BaseModel):
    """Model for product weight."""
    value: float
    unit: str

class ImageUrl(BaseModel):
    """Model for image URLs."""
    small: Optional[str] = None
    medium: Optional[str] = None
    large: Optional[str] = None

class ReviewSummary(BaseModel):
    """Model for review summaries."""
    average_rating: float = Field(..., alias="averageRating")
    total_reviews: int = Field(..., alias="totalReviews")

class CategoryInfo(BaseModel):
    """Model for category information."""
    id: str
    name: str
    path: List[str]

# Add more base models and utility classes as needed