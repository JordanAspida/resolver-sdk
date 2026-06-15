"""
Pydantic models for Forms API responses.
"""
from .base import BaseResolverModel


class FormsListResponse(BaseResolverModel):
    pass


class FormStructureResponse(BaseResolverModel):
    pass


class FormDeleteResponse(BaseResolverModel):
    pass


class FormReportsResponse(BaseResolverModel):
    pass


class FormFormulasResponse(BaseResolverModel):
    pass


class FormRolesResponse(BaseResolverModel):
    pass


class NavFormLoadResponse(BaseResolverModel):
    pass
