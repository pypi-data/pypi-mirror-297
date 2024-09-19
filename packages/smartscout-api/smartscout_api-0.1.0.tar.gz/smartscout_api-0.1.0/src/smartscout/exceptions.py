# src/smartscout/exceptions.py

class SmartScoutException(Exception):
    """Base exception class for SmartScout API."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class SmartScoutAPIError(SmartScoutException):
    """Exception raised for general API errors."""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.status_code = status_code
        self.response = response
        super().__init__(f"API Error: {message}")

class AuthenticationError(SmartScoutException):
    """Exception raised for authentication errors."""
    def __init__(self, message: str = "Invalid API key or authentication failed"):
        super().__init__(f"Authentication Error: {message}")

class RateLimitError(SmartScoutException):
    """Exception raised when API rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(f"Rate Limit Error: {message}")

class ValidationError(SmartScoutException):
    """Exception raised for request validation errors."""
    def __init__(self, message: str, errors: dict = None):
        self.errors = errors
        super().__init__(f"Validation Error: {message}")

class ResourceNotFoundError(SmartScoutException):
    """Exception raised when a requested resource is not found."""
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(f"Resource Not Found: {resource_type} with id {resource_id} not found")

class InsufficientPermissionsError(SmartScoutException):
    """Exception raised when the API key doesn't have sufficient permissions for an action."""
    def __init__(self, action: str):
        super().__init__(f"Insufficient Permissions: Your API key doesn't have permission to {action}")

class ServiceUnavailableError(SmartScoutException):
    """Exception raised when the SmartScout service is unavailable."""
    def __init__(self, message: str = "SmartScout service is currently unavailable"):
        super().__init__(f"Service Unavailable: {message}")

class RequestTimeoutError(SmartScoutException):
    """Exception raised when a request to the API times out."""
    def __init__(self, timeout: float):
        super().__init__(f"Request Timeout: The request timed out after {timeout} seconds")

class InvalidRequestError(SmartScoutException):
    """Exception raised when the request is invalid."""
    def __init__(self, message: str):
        super().__init__(f"Invalid Request: {message}")

class UnexpectedResponseError(SmartScoutException):
    """Exception raised when the API returns an unexpected response."""
    def __init__(self, message: str, response: dict = None):
        self.response = response
        super().__init__(f"Unexpected Response: {message}")

# You can add more specific exceptions as needed based on the API's error responses