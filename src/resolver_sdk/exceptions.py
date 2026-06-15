import json
from typing import Any


class ResolverSDKError(Exception):
    """Base exception for Resolver SDK."""


# Formats HTTP error response body into a readable string for error messages
def format_response_body(response_body: Any) -> str:
    """Return a readable representation of a Resolver API error response."""
    if response_body is None:
        return ""
    if isinstance(response_body, str):
        return response_body
    try:
        return json.dumps(response_body, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return str(response_body)


# Exception raised when an HTTP error occurs during API communication
class ResolverHTTPError(ResolverSDKError):
    def __init__(self, message: str, status_code: int | None = None, response_body=None):
        self.status_code = status_code
        self.response_body = response_body
        self.api_error_message = format_response_body(response_body)
        self.message = message

        full_message = message
        if self.api_error_message:
            full_message = f"{message}. Resolver API response: {self.api_error_message}"

        super().__init__(full_message)


# Exception for HTTP 400 Bad Request errors
class ResolverBadRequestError(ResolverHTTPError):
    pass


# Exception for HTTP 401 Unauthorized errors
class ResolverUnauthorizedError(ResolverHTTPError):
    pass


# Exception for HTTP 403 Forbidden errors
class ResolverForbiddenError(ResolverHTTPError):
    pass


# Exception for HTTP 404 Not Found errors
class ResolverNotFoundError(ResolverHTTPError):
    pass


# Exception for HTTP 409 Conflict errors
class ResolverConflictError(ResolverHTTPError):
    pass


# Exception for HTTP 429 Rate Limit errors
class ResolverRateLimitError(ResolverHTTPError):
    pass


# Exception for HTTP 5xx Server errors
class ResolverServerError(ResolverHTTPError):
    pass


# Exception for network transport errors (connection failures, timeouts)
class ResolverTransportError(ResolverSDKError):
    pass
