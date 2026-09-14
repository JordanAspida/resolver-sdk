"""
Pydantic models for UserGroups API responses.
"""
from .base import *
from pydantic import Field
from typing import Optional

class UserInfo(BaseModel):
    userId : int = Field(alias="id")
    firstName : str = Field(alias="first")
    lastName : str = Field(alias="last")
    email : str
    externalRefId : str = Field(alias="externalRefId")
    isActive : bool
    userType : int
    isAdmin : bool
    isPortalUrlAccess : bool
    hasAdvancedPermissions : bool
    advancedPermissions : list[Any] = Field(default_factory=list)
    lastLogin : str | None
    lang : str | None


