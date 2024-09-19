# src/smartscout/models/responses.py

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .base import BaseResponse, PagedResponse, Money, Dimension, Weight, ImageUrl, ReviewSummary, CategoryInfo
from .enums import ProductCondition, FulfillmentChannel, BuyBoxOwner, SellerType, BrandType

class Brand(BaseResponse):
    brand_name: str = Field(..., alias="brandName")
    amazon_isr: Optional[float] = Field(None, alias="amazonIsr")
    avg_fba_sellers: Optional[float] = Field(None, alias="avgFbaSellers")
    avg_sellers: Optional[float] = Field(None, alias="avgSellers")
    avg_price: Optional[float] = Field(None, alias="avgPrice")
    avg_volume: Optional[float] = Field(None, alias="avgVolume")
    review_rating: Optional[float] = Field(None, alias="reviewRating")
    total_products: Optional[int] = Field(None, alias="totalProducts")
    total_reviews: Optional[int] = Field(None, alias="totalReviews")
    monthly_revenue: Optional[float] = Field(None, alias="monthlyRevenue")
    monthly_units_sold: Optional[int] = Field(None, alias="monthlyUnitsSold")
    brand_score: Optional[float] = Field(None, alias="brandScore")
    has_storefront: bool = Field(..., alias="hasStorefront")
    has_single_seller: bool = Field(..., alias="hasSingleSeller")
    dominant_seller_profile_id: Optional[int] = Field(None, alias="dominantSellerProfileId")
    dominant_seller_brand_coverage: Optional[float] = Field(None, alias="dominantSellerBrandCoverage")
    category_name: Optional[str] = Field(None, alias="categoryName")
    subcategory_name: Optional[str] = Field(None, alias="subcategoryName")
    month_growth: Optional[float] = Field(None, alias="monthGrowth")
    month_growth_12: Optional[float] = Field(None, alias="monthGrowth12")
    trailing_12_months: Optional[float] = Field(None, alias="trailing12Months")

class Product(BaseResponse):
    asin: str
    title: str
    brand: Optional[str] = None
    category: CategoryInfo
    subcategory: CategoryInfo
    price: Money
    list_price: Optional[Money] = Field(None, alias="listPrice")
    currency: str
    condition: ProductCondition
    availability: str
    fulfillment_channel: FulfillmentChannel = Field(..., alias="fulfillmentChannel")
    is_prime: bool = Field(..., alias="isPrime")
    is_amazon_fulfilled: bool = Field(..., alias="isAmazonFulfilled")
    is_fba: bool = Field(..., alias="isFBA")
    sales_rank: Optional[int] = Field(None, alias="salesRank")
    reviews: ReviewSummary
    rating: Optional[float] = None
    total_ratings: Optional[int] = Field(None, alias="totalRatings")
    dimensions: Optional[Dimension] = None
    weight: Optional[Weight] = None
    images: ImageUrl
    features: Optional[List[str]] = None
    description: Optional[str] = None
    is_variation: bool = Field(..., alias="isVariation")
    parent_asin: Optional[str] = Field(None, alias="parentAsin")
    variation_attributes: Optional[List[str]] = Field(None, alias="variationAttributes")
    estimated_monthly_sales: Optional[int] = Field(None, alias="estimatedMonthlySales")
    estimated_monthly_revenue: Optional[Money] = Field(None, alias="estimatedMonthlyRevenue")
    buy_box_price: Optional[Money] = Field(None, alias="buyBoxPrice")
    buy_box_owner: Optional[BuyBoxOwner] = Field(None, alias="buyBoxOwner")
    number_of_sellers: Optional[int] = Field(None, alias="numberOfSellers")
    number_of_fba_sellers: Optional[int] = Field(None, alias="numberOfFBASellers")

class Seller(BaseResponse):
    seller_id: str = Field(..., alias="sellerId")
    seller_name: str = Field(..., alias="sellerName")
    seller_type: SellerType = Field(..., alias="sellerType")
    is_fba: bool = Field(..., alias="isFBA")
    feedback_count: Optional[int] = Field(None, alias="feedbackCount")
    positive_feedback_percent: Optional[float] = Field(None, alias="positiveFeedbackPercent")
    seller_rating: Optional[float] = Field(None, alias="sellerRating")
    ships_from: Optional[List[str]] = Field(None, alias="shipsFrom")
    ships_from_country: Optional[str] = Field(None, alias="shipsFromCountry")
    delivery_time: Optional[str] = Field(None, alias="deliveryTime")
    business_name: Optional[str] = Field(None, alias="businessName")
    business_address: Optional[str] = Field(None, alias="businessAddress")
    year_established: Optional[int] = Field(None, alias="yearEstablished")
    total_revenue: Optional[Money] = Field(None, alias="totalRevenue")
    average_rating: Optional[float] = Field(None, alias="averageRating")
    total_ratings: Optional[int] = Field(None, alias="totalRatings")
    products_offered: Optional[int] = Field(None, alias="productsOffered")

class SearchTerm(BaseResponse):
    search_term: str = Field(..., alias="searchTerm")
    search_volume: int = Field(..., alias="searchVolume")
    trend: Optional[str] = None
    cpc: Optional[float] = None
    competition: Optional[str] = None
    num_results: Optional[int] = Field(None, alias="numResults")
    organic_product_count: Optional[int] = Field(None, alias="organicProductCount")
    sponsored_product_count: Optional[int] = Field(None, alias="sponsoredProductCount")
    brands: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    related_search_terms: Optional[List[str]] = Field(None, alias="relatedSearchTerms")

class BrandSalesHistory(BaseResponse):
    date: datetime
    brand: str
    sales: float
    units_sold: int = Field(..., alias="unitsSold")
    average_price: float = Field(..., alias="averagePrice")

class ProductSalesHistory(BaseResponse):
    date: datetime
    asin: str
    sales: float
    units_sold: int = Field(..., alias="unitsSold")
    price: float
    sales_rank: Optional[int] = Field(None, alias="salesRank")

class SellerPerformance(BaseResponse):
    date: datetime
    seller_id: str = Field(..., alias="sellerId")
    order_defect_rate: float = Field(..., alias="orderDefectRate")
    pre_fulfillment_cancel_rate: float = Field(..., alias="preFulfillmentCancelRate")
    late_shipment_rate: float = Field(..., alias="lateShipmentRate")
    valid_tracking_rate: float = Field(..., alias="validTrackingRate")
    customer_service_dissatisfaction_rate: float = Field(..., alias="customerServiceDissatisfactionRate")

class CategoryTrend(BaseResponse):
    category: CategoryInfo
    total_revenue: Money = Field(..., alias="totalRevenue")
    total_units_sold: int = Field(..., alias="totalUnitsSold")
    average_price: float = Field(..., alias="averagePrice")
    top_brands: List[str] = Field(..., alias="topBrands")
    growth_rate: float = Field(..., alias="growthRate")

class CompetitorAnalysis(BaseResponse):
    competitor_asin: str = Field(..., alias="competitorAsin")
    competitor_brand: str = Field(..., alias="competitorBrand")
    price_difference: float = Field(..., alias="priceDifference")
    rating_difference: float = Field(..., alias="ratingDifference")
    review_count_difference: int = Field(..., alias="reviewCountDifference")
    sales_rank_difference: Optional[int] = Field(None, alias="salesRankDifference")
    estimated_sales_difference: Optional[float] = Field(None, alias="estimatedSalesDifference")

# Paged response models
class BrandPagedResponse(PagedResponse[Brand]):
    pass

class ProductPagedResponse(PagedResponse[Product]):
    pass

class SellerPagedResponse(PagedResponse[Seller]):
    pass

class SearchTermPagedResponse(PagedResponse[SearchTerm]):
    pass

# Add more response models as needed based on the API documentation and requirements

__all__ = [
    'Brand', 'Product', 'Seller', 'SearchTerm', 'BrandSalesHistory',
    'ProductSalesHistory', 'SellerPerformance', 'CategoryTrend',
    'CompetitorAnalysis', 'BrandPagedResponse', 'ProductPagedResponse',
    'SellerPagedResponse', 'SearchTermPagedResponse',
    # Add 'OrganicRank' to this list if you define it
]