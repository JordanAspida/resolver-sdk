"""
Pydantic models for Applications API responses.
"""
from .base import BaseResolverModel


class ApplicationsListResponse(BaseResolverModel):
    pass


class ActivitiesListResponse(BaseResolverModel):
    pass


class ActionsListResponse(BaseResolverModel):
    pass


class ViewsListResponse(BaseResolverModel):
    pass
