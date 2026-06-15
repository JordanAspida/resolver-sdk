"""
Pydantic models for Lifecycle API responses.
"""
from .base import BaseResolverModel


class LifecyclesListResponse(BaseResolverModel):
    pass


class StatesAndTransitionsResponse(BaseResolverModel):
    pass


class StateActionsResponse(BaseResolverModel):
    pass


class TransitionsListResponse(BaseResolverModel):
    pass


class TransitionActionsResponse(BaseResolverModel):
    pass
