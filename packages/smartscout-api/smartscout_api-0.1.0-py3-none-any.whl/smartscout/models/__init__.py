# src/smartscout/models/__init__.py

# Import enums
from .enums import MarketplaceId, SortOrder, TextFilterType

# Import base models and utilities
from .base import ListFilter, RangeDecimal, RangeFilter, RangeInt, TextFilter, Paging

# Import request models
from .requests import (
    SearchBrandsRequest,
    SearchProductsRequest,
    SearchSearchTermsRequest,
    SearchSellersRequest,
    SearchSubcategoriesRequest,
    GetOrganicRanksRequest,
    GetProductHistoryScopeRequest,
    GetRelevantProductsRequest,
    GetSubcategoryBrandsRequest,
    GetSubcategorySalesHistoryByBrandsRequest,
    GetSubcategorySalesHistoryRequest,
    GetSubcategoryScopeByBrandsRequest,
    GetSubcategoryScopeRequest,
    GetSubcategoryScopeTopProductsRequest,
    GetSubcategoryTopProductsSalesHistoryRequest,
    GetSubcategoryTopProductsSalesRankHistoryRequest,
    GetRelevantSearchTermsRequest,
    GetSearchTermHistoryRequest,
)

# Import response models
from .responses import (
    Brand,
    BrandCoverage,
    BrandSalesHistory,
    BrandScope,
    BrandScopeBySubcategory,
    BrandSearchTerm,
    DailyRank,
    EstimatedUnitSalesHistory,
    Product,
    ProductHistory,
    ProductOffer,
    ProductSalesHistory,
    ProductSalesRankHistory,
    RelevantProduct,
    RelevantSearchTerm,
    SalesEstimate,
    ScopeHistory,
    SearchTerm,
    SearchTermBrand,
    SearchTermHistory,
    SearchTermProductRank,
    Seller,
    SellerHistory,
    SellerOffer,
    Subcategory,
    SubcategoryBrand,
    SubcategorySalesHistory,
    SubcategoryScope,
    SubcategoryScopeByBrand,
    TopProductScope,
)

# Define __all__ to specify what gets imported with "from smartscout.models import *"
__all__ = [
    # Enums
    "MarketplaceId",
    "SortOrder",
    "TextFilterType",
    
    # Base models and utilities
    "ListFilter",
    "RangeDecimal",
    "RangeFilter",
    "RangeInt",
    "TextFilter",
    "Paging",
    
    # Request models
    "SearchBrandsRequest",
    "SearchProductsRequest",
    "SearchSearchTermsRequest",
    "SearchSellersRequest",
    "SearchSubcategoriesRequest",
    "GetOrganicRanksRequest",
    "GetProductHistoryScopeRequest",
    "GetRelevantProductsRequest",
    "GetSubcategoryBrandsRequest",
    "GetSubcategorySalesHistoryByBrandsRequest",
    "GetSubcategorySalesHistoryRequest",
    "GetSubcategoryScopeByBrandsRequest",
    "GetSubcategoryScopeRequest",
    "GetSubcategoryScopeTopProductsRequest",
    "GetSubcategoryTopProductsSalesHistoryRequest",
    "GetSubcategoryTopProductsSalesRankHistoryRequest",
    "GetRelevantSearchTermsRequest",
    "GetSearchTermHistoryRequest",
    
    # Response models
    "Brand",
    "BrandCoverage",
    "BrandSalesHistory",
    "BrandScope",
    "BrandScopeBySubcategory",
    "BrandSearchTerm",
    "DailyRank",
    "EstimatedUnitSalesHistory",
    "Product",
    "ProductHistory",
    "ProductOffer",
    "ProductSalesHistory",
    "ProductSalesRankHistory",
    "RelevantProduct",
    "RelevantSearchTerm",
    "SalesEstimate",
    "ScopeHistory",
    "SearchTerm",
    "SearchTermBrand",
    "SearchTermHistory",
    "SearchTermProductRank",
    "Seller",
    "SellerHistory",
    "SellerOffer",
    "Subcategory",
    "SubcategoryBrand",
    "SubcategorySalesHistory",
    "SubcategoryScope",
    "SubcategoryScopeByBrand",
    "TopProductScope",
]