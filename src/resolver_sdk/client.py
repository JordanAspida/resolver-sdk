from .resources.forms import FormsAPI
from .resources.applications import ApplicationsAPI
from .resources.reports import ReportsAPI
from .resources.lifecycle import LifecycleAPI
from .resources.roles import RolesAPI
from .resources.objects import ObjectsAPI
from .resources.utility import UtilityAPI
from .transport import ResolverTransport


class ResolverClient:
    # Initializes the Resolver client with base URL, API key, and transport configuration
    def __init__(self, base_url, api_key, transport=None):
        self.transport = transport or ResolverTransport(base_url, api_key)
        self.base_url = self.transport.base_url
        self.api_calls = 0
        self.cache = {
            "all_forms": None,
            "all_applications": None,
            "all_reports": None,
            "all_lifecycles": None,
            "all_user_groups": None,
            "all_fields": None,
            "all_formula": None,
            "invalid_formula": None,
            "all_roles": None,
            "all_object_type_groups": None,
            "all_object_types": None,
            "all_data_defs": None,
            "all_webhooks": None,
        }
        self.cache_derived = {}

        self.forms = FormsAPI(self)
        self.applications = ApplicationsAPI(self)
        self.reports = ReportsAPI(self)
        self.lifecycle = LifecycleAPI(self)
        self.roles = RolesAPI(self)
        self.objects = ObjectsAPI(self)
        self.utility = UtilityAPI(self)

    # Delegates HTTP request to transport layer and tracks API call count
    def request(self, *args, **kwargs):
        result = self.transport.request(*args, **kwargs)
        self.api_calls = self.transport.api_calls
        return result

    # Performs a GET request to the specified endpoint with optional query parameters
    def safe_get(self, endpoint, params=None):
        return self.request("GET", endpoint, params=params)

    # Performs a POST request to the specified endpoint with optional parameters and body
    def safe_post(self, endpoint, params=None, body=None):
        return self.request("POST", endpoint, body=body, params=params)

    # Performs a PUT request to the specified endpoint with optional parameters and body
    def safe_put(self, endpoint, params=None, body=None):
        return self.request("PUT", endpoint, body=body, params=params)

    # Performs a DELETE request to the specified endpoint with optional parameters
    def safe_delete(self, endpoint, params=None):
        return self.request("DELETE", endpoint, params=params)

    # Returns the total count of API calls made by the transport layer
    def get_api_calls(self):
        return self.transport.api_calls

    # Stores a derived cache value for improved performance on subsequent operations
    def set_derived_cache(self, key, value):
        self.cache_derived[key] = value

    # Retrieves a previously stored derived cache value
    def get_derived_cache(self, key):
        return self.cache_derived.get(key)

