# src/smartscout/models/requests.py

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .base import BaseSearchRequest, BaseHistoryRequest, RangeDecimal, RangeFilter, RangeInt, TextFilter, ListFilter, DateRangeFilter
from .enums import ProductCondition, FulfillmentChannel, BrandType, Intent, AdType

class SearchBrandsRequest(BaseSearchRequest):
    brand_names: Optional[ListFilter] = Field(None, alias="brandNames")
    brand_name: Optional[TextFilter] = Field(None, alias="brandName")
    amazon_isr: Optional[RangeFilter] = Field(None, alias="amazonIsr")
    avg_sellers: Optional[RangeFilter] = Field(None, alias="avgSellers")
    avg_price: Optional[RangeFilter] = Field(None, alias="avgPrice")
    avg_volume: Optional[RangeFilter] = Field(None, alias="avgVolume")
    review_rating: Optional[RangeFilter] = Field(None, alias="reviewRating")
    total_reviews: Optional[RangeInt] = Field(None, alias="totalReviews")
    total_products: Optional[RangeInt] = Field(None, alias="totalProducts")
    avg_fba_sellers: Optional[RangeFilter] = Field(None, alias="avgFbaSellers")
    brand_score: Optional[RangeFilter] = Field(None, alias="brandScore")
    monthly_revenue: Optional[RangeFilter] = Field(None, alias="monthlyRevenue")
    note: Optional[TextFilter] = None
    category: Optional[TextFilter] = None
    category_name: Optional[TextFilter] = Field(None, alias="categoryName")
    subcategory_name: Optional[TextFilter] = Field(None, alias="subcategoryName")
    has_storefront: Optional[bool] = Field(None, alias="hasStorefront")
    search_terms: Optional[RangeInt] = Field(None, alias="searchTerms")
    sponsored_products: Optional[RangeInt] = Field(None, alias="sponsoredProducts")
    sponsored_brand_win_rate: Optional[RangeDecimal] = Field(None, alias="sponsoredBrandWinRate")
    sponsored_video_win_rate: Optional[RangeDecimal] = Field(None, alias="sponsoredVideoWinRate")
    top_spot_win_rate: Optional[RangeDecimal] = Field(None, alias="topSpotWinRate")
    top_group_win_rate: Optional[RangeDecimal] = Field(None, alias="topGroupWinRate")
    month_growth: Optional[RangeDecimal] = Field(None, alias="monthGrowth")
    month_growth_12: Optional[RangeDecimal] = Field(None, alias="monthGrowth12")
    trailing_12_months: Optional[RangeDecimal] = Field(None, alias="trailing12Months")

class SearchProductsRequest(BaseSearchRequest):
    subcategory_id: Optional[int] = Field(None, alias="subcategoryId")
    brand_name: Optional[TextFilter] = Field(None, alias="brandName")
    category_name: Optional[TextFilter] = Field(None, alias="categoryName")
    subcategory_name: Optional[TextFilter] = Field(None, alias="subcategoryName")
    rank: Optional[RangeInt] = None
    monthly_revenue_estimate: Optional[RangeFilter] = Field(None, alias="monthlyRevenueEstimate")
    amazon_isr: Optional[RangeFilter] = Field(None, alias="amazonIsr")
    number_of_sellers: Optional[RangeInt] = Field(None, alias="numberOfSellers")
    number_fba_sellers: Optional[RangeInt] = Field(None, alias="numberFbaSellers")
    review_count: Optional[RangeInt] = Field(None, alias="reviewCount")
    review_rating: Optional[RangeFilter] = Field(None, alias="reviewRating")
    buy_box_price: Optional[RangeFilter] = Field(None, alias="buyBoxPrice")
    product_page_score: Optional[RangeFilter] = Field(None, alias="productPageScore")
    out_of_stock_now: Optional[bool] = Field(None, alias="outOfStockNow")
    is_variation: Optional[bool] = Field(None, alias="isVariation")
    asins: Optional[ListFilter] = None
    asin: Optional[TextFilter] = None
    parent_asin: Optional[TextFilter] = Field(None, alias="parentAsin")
    title: Optional[TextFilter] = None
    note: Optional[TextFilter] = None
    buy_box_equity: Optional[RangeFilter] = Field(None, alias="buyBoxEquity")
    number_of_items: Optional[RangeInt] = Field(None, alias="numberOfItems")
    total_ratings: Optional[RangeInt] = Field(None, alias="totalRatings")

class SearchSearchTermsRequest(BaseSearchRequest):
    search_term_value: Optional[TextFilter] = Field(None, alias="searchTermValue")
    estimate_searches: Optional[RangeInt] = Field(None, alias="estimateSearches")
    brands: Optional[RangeInt] = None
    products: Optional[RangeInt] = None
    estimated_cpc: Optional[RangeFilter] = Field(None, alias="estimatedCpc")
    super_charge: Optional[bool] = Field(None, alias="superCharge")

class SearchSellersRequest(BaseSearchRequest):
    category_name: Optional[TextFilter] = Field(None, alias="categoryName")
    subcategory_name: Optional[TextFilter] = Field(None, alias="subcategoryName")
    amazon_seller_id: Optional[TextFilter] = Field(None, alias="amazonSellerId")
    amazon_seller_ids: Optional[ListFilter] = Field(None, alias="amazonSellerIds")
    seller_names: Optional[ListFilter] = Field(None, alias="sellerNames")
    business_names: Optional[ListFilter] = Field(None, alias="businessNames")
    include_products: Optional[bool] = Field(None, alias="includeProducts")
    estimate_sales: Optional[RangeFilter] = Field(None, alias="estimateSales")
    seller_name: Optional[TextFilter] = Field(None, alias="sellerName")
    percent_fba: Optional[RangeFilter] = Field(None, alias="percentFba")
    number_winning_brands: Optional[RangeInt] = Field(None, alias="numberWinningBrands")
    number_asins: Optional[RangeInt] = Field(None, alias="numberAsins")
    number_top_asins: Optional[RangeInt] = Field(None, alias="numberTopAsins")
    num_brands_1000: Optional[RangeInt] = Field(None, alias="numBrands1000")
    mom_growth: Optional[RangeFilter] = Field(None, alias="moMGrowth")
    three_month_growth: Optional[RangeFilter] = Field(None, alias="threeMonthGrowth")
    six_month_growth: Optional[RangeFilter] = Field(None, alias="sixMonthGrowth")
    year_growth: Optional[RangeFilter] = Field(None, alias="yearGrowth")
    mom_growth_count: Optional[RangeInt] = Field(None, alias="moMGrowthCount")
    six_month_growth_count: Optional[RangeInt] = Field(None, alias="sixMonthGrowthCount")
    street: Optional[TextFilter] = None
    city: Optional[TextFilter] = None
    state: Optional[TextFilter] = None
    country: Optional[TextFilter] = None
    zip_code: Optional[TextFilter] = Field(None, alias="zipCode")
    business_name: Optional[TextFilter] = Field(None, alias="businessName")
    number_reviews_lifetime: Optional[RangeInt] = Field(None, alias="numberReviewsLifetime")
    number_reviews_30_days: Optional[RangeInt] = Field(None, alias="numberReviews30Days")
    is_suspended: Optional[bool] = Field(None, alias="isSuspended")
    last_suspended_date: Optional[datetime] = Field(None, alias="lastSuspendedDate")

class GetOrganicRanksRequest(BaseSearchRequest):
    asin: Optional[str] = None
    exclude_variants: bool = Field(..., alias="excludeVariants")
    include_rank_history: bool = Field(..., alias="includeRankHistory")
    intent: Optional[Intent] = None
    search_term: Optional[TextFilter] = Field(None, alias="searchTerm")
    avg_rank: Optional[RangeDecimal] = Field(None, alias="avgRank")
    latest_rank: Optional[RangeInt] = Field(None, alias="latestRank")
    rank_score: Optional[RangeInt] = Field(None, alias="rankScore")
    smart_score: Optional[RangeInt] = Field(None, alias="smartScore")
    estimate_searches: Optional[RangeInt] = Field(None, alias="estimateSearches")

class GetProductHistoryScopeRequest(BaseHistoryRequest):
    pass

class GetRelevantProductsRequest(BaseSearchRequest):
    parent_asin: str = Field(..., alias="parentAsin")
    relevancy_score: Optional[RangeDecimal] = Field(None, alias="relevancyScore")
    common_search_terms: Optional[RangeInt] = Field(None, alias="commonSearchTerms")

class GetSubcategoryBrandsRequest(BaseSearchRequest):
    brand_name: Optional[str] = Field(None, alias="brandName")

class GetBrandSalesHistoryRequest(BaseHistoryRequest):
    subcategory_id: Optional[int] = Field(None, alias="subcategoryId")

class GetBrandSalesHistoryBySubcategoriesRequest(BaseHistoryRequest):
    brand_name: str = Field(..., alias="brandName")
    subcategory_id: Optional[int] = Field(None, alias="subcategoryId")

class GetBrandScopeRequest(BaseHistoryRequest):
    brand_name: str = Field(..., alias="brandName")
    subcategory_id: Optional[int] = Field(None, alias="subcategoryId")

class GetBrandScopeTopProductsRequest(BaseHistoryRequest):
    brand_name: str = Field(..., alias="brandName")
    top_by: str = Field(..., alias="topBy")
    top: int
    subcategory_id: Optional[int] = Field(None, alias="subcategoryId")

class GetRelevantSearchTermsRequest(BaseSearchRequest):
    parent_asin: str = Field(..., alias="parentAsin")
    search_term: Optional[TextFilter] = Field(None, alias="searchTerm")
    intent: Optional[Intent] = None
    relevancy: Optional[RangeDecimal] = None
    estimated_searches: Optional[RangeInt] = Field(None, alias="estimatedSearches")

class GetSearchTermHistoryRequest(BaseHistoryRequest):
    search_term: str = Field(..., alias="searchTerm")

# Add more request models as needed based on the API documentation and requirements