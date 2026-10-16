"""
Pydantic models for Roles API responses.
"""
from .base import BaseResolverModel, User, UserGroup

from pydantic import Field

class UserDetails(User):
    jobTitle : str | None = None
    isActive : bool
    superAdmin : bool
    acceptedTos : bool
    ssoBypass : bool
    lang : str
    internalUser : bool
    workatoSuperAdmin : bool

class RoleDetails(BaseResolverModel):
    id : int
    name : str
    description : str | None = None
    isGlobal : bool
    created : str
    modified : str | None = None
    org : int
    canPerformSearch : bool
    canQuickCreate : bool
    canGetHelp : bool
    canSearchArchive : bool
    externalRefId : str


class RoleMembers(BaseResolverModel):
    users : list[UserDetails]
    groups : list[UserGroup]

class LifecycleId(BaseResolverModel):
    objectLifeCycleId : int

class RolePermissions(BaseResolverModel):
    id : int
    permission : int
    canBulkLaunch : bool
    canCreate : bool
    canDelete : bool
    canMerge : bool
    canManageRole : bool
    roleId : int
    objectTypeId : int
    objectLifeCycleId : int
    stateId : int = Field(alias="objectLifeCycleStateId")
    formId : str | int | None = None
    org : int
    assigned : bool
    created : str
    modified : str | None = None
    createdBy : int | None = None
    modifiedBy : int | None = None
    externalRefId : str