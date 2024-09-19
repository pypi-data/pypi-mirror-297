# SmartScout API Python Package

This Python package provides a convenient wrapper for the SmartScout API, allowing you to easily interact with SmartScout's powerful e-commerce analytics tools in your Python projects.

## Features

- Easy-to-use client for all SmartScout API endpoints
- Type-safe request and response models
- Automatic pagination handling
- Comprehensive error handling

## Installation

You can install the SmartScout API Python package using pip:

```bash
pip install smartscout-api
```

## Quick Start

Here's a quick example of how to use the SmartScout API client:

```python
from smartscout import SmartScoutAPIClient
from smartscout.models import SearchProductsRequest, MarketplaceId

# Initialize the client with your API key
client = SmartScoutAPIClient(api_key="your_api_key_here")

# Create a request to search for products
request = SearchProductsRequest(
    marketplace=MarketplaceId.US,
    brand_name="Example Brand",
    review_count={"min": 100}
)

# Make the API call
response = client.search_products(request)

# Process the results
for product in response.data:
    print(f"Product: {product.asin}, Title: {product.title}, Price: ${product.price}")

# If there are more pages, you can access them like this:
while response.paging.has_more_records:
    request.page.id = response.paging.next_page_id
    response = client.search_products(request)
    # Process the next page of results...
```

## Available Methods

The `SmartScoutAPIClient` provides methods for all SmartScout API endpoints, including:

- `search_brands()`
- `search_products()`
- `search_search_terms()`
- `search_sellers()`
- `get_organic_ranks()`
- `get_product_history_scope()`
- `get_relevant_products()`
- `get_subcategory_brands()`
- `get_brand_sales_history()`
- `get_brand_sales_history_by_subcategories()`
- `get_brand_scope()`
- `get_brand_scope_top_products()`
- `get_relevant_search_terms()`
- `get_search_term_history()`

Each method corresponds to a specific API endpoint and accepts a request model as its parameter.

## Error Handling

The package includes custom exceptions for various error scenarios:

- `SmartScoutAPIError`: General API errors
- `AuthenticationError`: Issues with API key authentication
- `RateLimitError`: API rate limit exceeded
- `ValidationError`: Request validation errors
- `ResourceNotFoundError`: Requested resource not found
- `InsufficientPermissionsError`: Lack of permissions for an action
- `ServiceUnavailableError`: SmartScout service unavailable
- `RequestTimeoutError`: API request timeout
- `InvalidRequestError`: Invalid request parameters
- `UnexpectedResponseError`: Unexpected API response format

You can catch these exceptions to handle different error scenarios in your code:

```python
from smartscout.exceptions import SmartScoutAPIError, RateLimitError

try:
    response = client.search_products(request)
except RateLimitError:
    print("Rate limit exceeded. Please wait before making more requests.")
except SmartScoutAPIError as e:
    print(f"An API error occurred: {e.message}")
```

## Documentation

For detailed information about the SmartScout API, including all available endpoints and request/response models, please refer to the [official SmartScout API documentation](https://api.smartscout.com/docs).

## Contributing

We welcome contributions to the SmartScout API Python package! Please see our [contribution guidelines](CONTRIBUTING.md) for more information on how to get started.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions about using the SmartScout API Python package, please [open an issue](https://github.com/yourusername/smartscout-api-python/issues) on our GitHub repository.

For questions related to the SmartScout API itself or your SmartScout account, please contact SmartScout support directly.

## Disclaimer

This package is not officially maintained by SmartScout. It is a community-developed wrapper for the SmartScout API.