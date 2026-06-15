"""
Pydantic models for Roles API responses.
"""
from .base import BaseResolverModel


class RolesListResponse(BaseResolverModel):
    pass


class RoleMembersResponse(BaseResolverModel):
    pass


class RoleDetailResponse(BaseResolverModel):
    pass


class RoleDeleteResponse(BaseResolverModel):
    pass
