# src/smartscout/client.py

import requests
from typing import Dict, Any, Type, TypeVar, Generic
from .models.base import BaseRequest, BaseResponse, PagedResponse
from .models.enums import MarketplaceId
from .models.requests import (
    SearchBrandsRequest,
    SearchProductsRequest,
    SearchSearchTermsRequest,
    SearchSellersRequest,
    GetOrganicRanksRequest,
    GetProductHistoryScopeRequest,
    GetRelevantProductsRequest,
    GetSubcategoryBrandsRequest,
    GetBrandSalesHistoryRequest,
    GetBrandSalesHistoryBySubcategoriesRequest,
    GetBrandScopeRequest,
    GetBrandScopeTopProductsRequest,
    GetRelevantSearchTermsRequest,
    GetSearchTermHistoryRequest,
)
from .models.responses import (
    Brand,
    Product,
    SearchTerm,
    Seller,
    BrandSalesHistory,
    ProductSalesHistory,
    SellerPerformance,
    CategoryTrend,
    CompetitorAnalysis,
)
from .exceptions import SmartScoutAPIError, RateLimitError, AuthenticationError

T = TypeVar('T', bound=BaseResponse)

class SmartScoutClient:
    """
    A client for interacting with the SmartScout API.
    """

    BASE_URL = "https://api.smartscout.com/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a request to the SmartScout API.
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            elif e.response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            else:
                raise SmartScoutAPIError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise SmartScoutAPIError(f"An error occurred: {e}")

    def _paged_request(self, endpoint: str, request: BaseRequest, response_model: Type[T]) -> PagedResponse[T]:
        """
        Make a paged request to the SmartScout API.
        """
        data = request.dict(exclude_none=True)
        response_data = self._make_request("POST", endpoint, data=data)
        return PagedResponse[response_model](**response_data)

    def search_brands(self, request: SearchBrandsRequest) -> PagedResponse[Brand]:
        """
        Search for brands based on the given criteria.
        """
        return self._paged_request("/brands/search", request, Brand)

    def search_products(self, request: SearchProductsRequest) -> PagedResponse[Product]:
        """
        Search for products based on the given criteria.
        """
        return self._paged_request("/products/search", request, Product)

    def search_search_terms(self, request: SearchSearchTermsRequest) -> PagedResponse[SearchTerm]:
        """
        Search for search terms based on the given criteria.
        """
        return self._paged_request("/search-terms/search", request, SearchTerm)

    def search_sellers(self, request: SearchSellersRequest) -> PagedResponse[Seller]:
        """
        Search for sellers based on the given criteria.
        """
        return self._paged_request("/sellers/search", request, Seller)

    def get_organic_ranks(self, request: GetOrganicRanksRequest) -> PagedResponse[Product]:
        """
        Get organic ranks for products based on the given criteria.
        """
        return self._paged_request("/products/organic-ranks", request, Product)

    def get_product_history_scope(self, request: GetProductHistoryScopeRequest) -> PagedResponse[ProductSalesHistory]:
        """
        Get product history scope based on the given criteria.
        """
        return self._paged_request("/products/history/scope", request, ProductSalesHistory)

    def get_relevant_products(self, request: GetRelevantProductsRequest) -> PagedResponse[Product]:
        """
        Get relevant products based on the given criteria.
        """
        return self._paged_request("/products/relevant", request, Product)

    def get_subcategory_brands(self, request: GetSubcategoryBrandsRequest) -> PagedResponse[Brand]:
        """
        Get brands in a subcategory based on the given criteria.
        """
        return self._paged_request("/subcategories/brands", request, Brand)

    def get_brand_sales_history(self, request: GetBrandSalesHistoryRequest) -> PagedResponse[BrandSalesHistory]:
        """
        Get brand sales history based on the given criteria.
        """
        return self._paged_request("/brands/history/sales", request, BrandSalesHistory)

    def get_brand_sales_history_by_subcategories(self, request: GetBrandSalesHistoryBySubcategoriesRequest) -> PagedResponse[BrandSalesHistory]:
        """
        Get brand sales history by subcategories based on the given criteria.
        """
        return self._paged_request("/brands/history/sales-by-subcategories", request, BrandSalesHistory)

    def get_brand_scope(self, request: GetBrandScopeRequest) -> PagedResponse[Brand]:
        """
        Get brand scope based on the given criteria.
        """
        return self._paged_request("/brands/scope", request, Brand)

    def get_brand_scope_top_products(self, request: GetBrandScopeTopProductsRequest) -> PagedResponse[Product]:
        """
        Get top products in a brand scope based on the given criteria.
        """
        return self._paged_request("/brands/scope/top-products", request, Product)

    def get_relevant_search_terms(self, request: GetRelevantSearchTermsRequest) -> PagedResponse[SearchTerm]:
        """
        Get relevant search terms based on the given criteria.
        """
        return self._paged_request("/search-terms/relevant", request, SearchTerm)

    def get_search_term_history(self, request: GetSearchTermHistoryRequest) -> PagedResponse[SearchTerm]:
        """
        Get search term history based on the given criteria.
        """
        return self._paged_request("/search-terms/history", request, SearchTerm)

    # Add more methods for other API endpoints as needed

# Example usage
if __name__ == "__main__":
    client = SmartScoutClient(api_key="your_api_key_here")
    
    # Search for brands
    brand_request = SearchBrandsRequest(marketplace=MarketplaceId.US, brand_name="Example Brand")
    brand_response = client.search_brands(brand_request)
    
    for brand in brand_response.data:
        print(f"Brand: {brand.brand_name}, Monthly Revenue: ${brand.monthly_revenue}")

    # Search for products
    product_request = SearchProductsRequest(marketplace=MarketplaceId.US, brand_name="Example Brand")
    product_response = client.search_products(product_request)
    
    for product in product_response.data:
        print(f"Product: {product.asin}, Title: {product.title}")

    # Add more examples for other API endpoints as needed