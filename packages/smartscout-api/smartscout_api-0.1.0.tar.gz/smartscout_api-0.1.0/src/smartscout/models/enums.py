# src/smartscout/models/enums.py

from enum import Enum

class MarketplaceId(Enum):
    """Enum for marketplace IDs."""
    NOT_SET = "NotSet"
    US = "US"
    UK = "UK"
    IT = "IT"
    DE = "DE"
    CA = "CA"
    MX = "MX"
    FR = "FR"
    ES = "ES"
    IN = "IN"
    AU = "AU"
    JP = "JP"

class SortOrder(Enum):
    """Enum for sort order."""
    ASCENDING = "asc"
    DESCENDING = "desc"

class TextFilterType(Enum):
    """Enum for text filter types."""
    CONTAINS = "contains"
    EXACT = "exact"
    STARTS_WITH = "startsWith"
    ENDS_WITH = "endsWith"

class ProductCondition(Enum):
    """Enum for product conditions."""
    NEW = "New"
    USED = "Used"
    REFURBISHED = "Refurbished"

class FulfillmentChannel(Enum):
    """Enum for fulfillment channels."""
    FBA = "FBA"
    FBM = "FBM"

class BuyBoxOwner(Enum):
    """Enum for Buy Box owner types."""
    AMAZON = "Amazon"
    FBA = "FBA"
    FBM = "FBM"

class ScopeMetric(Enum):
    """Enum for scope metrics."""
    REVENUE = "Revenue"
    UNIT_SALES = "UnitSales"
    SALES_RANK = "SalesRank"

class TimeFrame(Enum):
    """Enum for time frames."""
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"
    YEAR = "Year"

class ReviewRating(Enum):
    """Enum for review ratings."""
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class SellerType(Enum):
    """Enum for seller types."""
    FIRST_PARTY = "1P"
    THIRD_PARTY = "3P"

class BrandType(Enum):
    """Enum for brand types."""
    PRIVATE_LABEL = "PrivateLabel"
    RESELLER = "Reseller"

class TopProductSortBy(Enum):
    """Enum for sorting top products."""
    REVENUE = "Revenue"
    UNITS_SOLD = "UnitsSold"
    SALES_RANK = "SalesRank"

class Intent(Enum):
    """Enum for search intent."""
    INFORMATIONAL = "Informational"
    NAVIGATIONAL = "Navigational"
    TRANSACTIONAL = "Transactional"

class AdType(Enum):
    """Enum for ad types."""
    SPONSORED_PRODUCT = "SponsoredProduct"
    SPONSORED_BRAND = "SponsoredBrand"
    SPONSORED_DISPLAY = "SponsoredDisplay"

class CategoryLevel(Enum):
    """Enum for category levels."""
    ROOT = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5

# Add more enums as needed based on the API documentation and requirements