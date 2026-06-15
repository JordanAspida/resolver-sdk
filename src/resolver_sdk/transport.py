import logging
import time
from typing import Any
import requests

from .exceptions import (
    ResolverBadRequestError,
    ResolverConflictError,
    ResolverForbiddenError,
    ResolverHTTPError,
    ResolverNotFoundError,
    ResolverRateLimitError,
    ResolverServerError,
    ResolverTransportError,
    ResolverUnauthorizedError,
    format_response_body,
)

logger = logging.getLogger(__name__)


class ResolverTransport:
    # Initializes the transport layer with base URL, API key, timeout, and retry configuration
    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        timeout: int = 30,
        retries: int = 3,
        backoff: int = 2,
        session: requests.Session | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self.session = session or requests.Session()
        self.session.headers.update({"x-api-key": api_key, "Accept": "application/json"})
        self.api_calls = 0

    # Executes HTTP request with automatic retry logic and error handling for transient failures
    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict | None = None,
        body: dict | None = None,
        timeout: int | None = None,
        retries: int | None = None,
        backoff: int | None = None,
        return_json: bool = True,
    ) -> Any:
        # ============================================================================
        # SECTION 1: SETUP - Prepare request parameters
        # ============================================================================
        
        # Construct the full URL by combining base URL with endpoint path
        url = f"{self.base_url}{endpoint}"
        
        # Use provided parameters or fall back to instance defaults if not provided
        # This allows per-request customization while maintaining sane defaults
        timeout = timeout if timeout is not None else self.timeout
        retries = retries if retries is not None else self.retries
        backoff = backoff if backoff is not None else self.backoff

        # Initialize attempt counter for retry logic
        attempt = 0
        
        # ============================================================================
        # SECTION 2: RETRY LOOP - Attempt the request multiple times on failure
        # ============================================================================
        
        while attempt < retries:
            try:
                # ====================================================================
                # SECTION 2A: MAKE REQUEST - Execute the HTTP request
                # ====================================================================
                
                # Use the persistent session to send the HTTP request
                # The session maintains headers (including API key) across requests
                response = self.session.request(
                    method=method, url=url, params=params, json=body, timeout=timeout
                )
                
                # Increment counter to track total API calls made
                self.api_calls += 1

                # ====================================================================
                # SECTION 2B: CHECK STATUS - Validate HTTP response status code
                # ====================================================================
                
                # raise_for_status() throws HTTPError for 4xx and 5xx status codes
                # If the request succeeds (2xx-3xx), execution continues
                response.raise_for_status()

                # ====================================================================
                # SECTION 2C: HANDLE SUCCESS - Return the response
                # ====================================================================
                
                # 204 No Content is a success response but with no body
                # Return None to indicate successful operation with no data
                if response.status_code == 204:
                    return None
                
                # Check if caller expects JSON response or raw text
                if return_json:
                    try:
                        # Parse response as JSON object/list
                        return response.json()
                    except ValueError:
                        # If JSON parsing fails, fall back to returning raw text
                        # This handles cases where server returns text instead of JSON
                        return response.text
                
                # Caller requested raw text response, return it as-is
                return response.text
                
            except requests.exceptions.HTTPError as e:
                # ====================================================================
                # SECTION 3: HANDLE HTTP ERRORS - Process 4xx and 5xx responses
                # ====================================================================
                
                # Extract status code from the exception's response object
                # Use None if response object is missing (defensive programming)
                status_code = e.response.status_code if e.response is not None else None
                
                # ====================================================================
                # SECTION 3A: HANDLE 5xx ERRORS - Retry on server errors
                # ====================================================================
                
                # 5xx errors (500-599) are temporary server issues that may resolve
                # These errors should be retried with exponential backoff
                if status_code is not None and 500 <= status_code < 600:
                    # Increment attempt counter to track retry progress
                    attempt += 1
                    
                    # Check if we've exhausted all retry attempts
                    if attempt >= retries:
                        # All retries exhausted, convert HTTP error to SDK exception
                        mapped_error = self._map_http_error(
                            e, method=method, url=url, attempts=attempt
                        )
                        logger.error("%s", mapped_error)
                        # Re-raise as SDK exception for consistent error handling
                        raise mapped_error from e
                    
                    # Log warning about server error and retry plan
                    logger.warning(
                        "Resolver API server error with status %s on attempt %s/%s for "
                        "%s %s. Retrying in %s seconds. Response: %s",
                        status_code,
                        attempt,
                        retries,
                        method,
                        url,
                        backoff,
                        self._response_body_for_log(e.response),
                    )
                    
                    # Wait before retrying to give server time to recover
                    time.sleep(backoff)
                    
                    # Increase wait time for next attempt (exponential backoff)
                    # This prevents overwhelming a recovering server with rapid requests
                    backoff *= 2
                    
                    # Continue to next iteration of retry loop
                    continue
                
                # ====================================================================
                # SECTION 3B: HANDLE 4xx ERRORS - Do not retry, fail immediately
                # ====================================================================
                
                # 4xx errors (400-499) are client errors that won't be fixed by retrying
                # Examples: 401 Unauthorized, 403 Forbidden, 404 Not Found, 400 Bad Request
                # These indicate the request itself is invalid or authentication failed
                mapped_error = self._map_http_error(e, method=method, url=url)
                logger.error("%s", mapped_error)
                # Raise immediately without retry
                raise mapped_error from e
                
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                # ====================================================================
                # SECTION 4: HANDLE NETWORK ERRORS - Retry on connection/timeout failures
                # ====================================================================
                
                # These exceptions indicate temporary network issues, not API errors
                # They should be retried similar to 5xx errors
                attempt += 1
                
                # Check if we've exhausted all retry attempts
                if attempt >= retries:
                    # All retries exhausted, create descriptive error message
                    message = (
                        f"Resolver API transport error after {attempt} attempts "
                        f"for {method} {url}: {e}"
                    )
                    logger.error("%s", message)
                    # Raise SDK transport exception for consistent error handling
                    raise ResolverTransportError(message) from e
                
                # Log warning about network error and retry plan
                logger.warning(
                    "Resolver API transport error on attempt %s/%s for %s %s. "
                    "Retrying in %s seconds: %s",
                    attempt,
                    retries,
                    method,
                    url,
                    backoff,
                    e,
                )
                
                # Wait before retrying to give network time to recover
                time.sleep(backoff)
                
                # Increase wait time for next attempt (exponential backoff)
                backoff *= 2

        # ============================================================================
        # SECTION 5: EXHAUSTED RETRIES - All retry attempts failed
        # ============================================================================
        
        # This code is reached if the while loop completes without returning/raising
        # This means we've tried the request 'retries' times and all failed
        message = f"Request failed after {retries} attempts: {method} {url}"
        logger.error("%s", message)
        # Raise transport error to indicate the request ultimately failed
        raise ResolverTransportError(message)

    # Maps HTTP error responses to appropriate SDK exception classes with detailed context
    def _map_http_error(
        self,
        err: requests.exceptions.HTTPError,
        *,
        method: str | None = None,
        url: str | None = None,
        attempts: int | None = None,
    ) -> ResolverHTTPError:
        status = err.response.status_code if err.response is not None else None
        body = self._response_body(err.response)

        mapping = {
            400: ResolverBadRequestError,
            401: ResolverUnauthorizedError,
            403: ResolverForbiddenError,
            404: ResolverNotFoundError,
            409: ResolverConflictError,
            429: ResolverRateLimitError
        }
        
        # Check for server errors (5xx) first, then check mapping, default to ResolverHTTPError
        if status is not None and 500 <= status < 600:
            exc = ResolverServerError
        elif status is not None:
            exc = mapping.get(status, ResolverHTTPError)
        else:
            exc = ResolverHTTPError

        request_description = "Resolver API request"
        if method and url:
            request_description = f"Resolver API request {method} {url}"

        retry_description = ""
        if attempts is not None:
            retry_description = f" after {attempts} attempts"

        return exc(
            f"{request_description} failed with status {status}{retry_description}",
            status_code=status,
            response_body=body,
        )

    # Extracts and parses the response body from an HTTP response object
    def _response_body(self, response: requests.Response | None):
        if response is None:
            return None
        try:
            return response.json()
        except ValueError:
            return response.text

    # Formats response body into a readable string for logging purposes
    def _response_body_for_log(self, response: requests.Response | None) -> str:
        return format_response_body(self._response_body(response))
