class VyperApiException(Exception):
    """Base exception for Vyper API errors."""
    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

class VyperWebsocketException(Exception):
    """Base exception for Vyper WebSocket errors."""
    def __init__(self, message, status_code=None, connection_info=None):
        self.message = message
        self.status_code = status_code
        self.connection_info = connection_info
        super().__init__(self.message)

class AuthenticationError(VyperApiException):
    """Raised when there's an authentication problem."""

class RateLimitError(VyperApiException):
    """Raised when the rate limit is exceeded."""
    def __init__(self, message, retry_after):
        super().__init__(message)
        self.retry_after = retry_after

class ServerError(VyperApiException):
    """Raised when the server returns a 5xx status code."""