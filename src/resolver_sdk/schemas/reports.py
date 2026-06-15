"""
Pydantic models for Reports API responses.
"""
from .base import BaseResolverModel


class ReportsListResponse(BaseResolverModel):
    pass


class ReportComponentsListResponse(BaseResolverModel):
    pass


class ReportDeleteResponse(BaseResolverModel):
    pass
