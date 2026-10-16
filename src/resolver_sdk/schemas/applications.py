"""
Pydantic models for Applications API responses.
"""
from .base import BaseResolverModel
from typing import Any, Optional

class BaseAppInfo(BaseResolverModel):
    id : int
    name : str
    description : Optional[str] = None
    ordinal : int
    created : str
    modified : str | None = None
    org : int 
    externalRefId : str

class ApplicationsListResponse(BaseAppInfo):
    nextActivityOrdinal : int | None = None


class ActivitiesListResponse(BaseAppInfo):
    applicationId : int
    nextActionOrdinal : int | None = None
    nextViewOrdinal : int | None = None
    embeddedBiUrl : str | None = None


class ActionsListResponse(BaseAppInfo):
    activityId : int
    applicationId : int
    actionType : int
    objectTypeId : int | None = None
    reportId : int | None = None
    properties : dict[str, Any] | None = None
    reportRef : Optional[str] = None
    formId : Optional[int] = None
    formRef : Optional[str] = None


class ViewsListResponse(BaseAppInfo):
    activityId : int
    applicationId : int
    objectTypeId : int
    formId : Optional[int] = None
    formRef : Optional[str] = None
    reportId : Optional[int] = None
    reportRef : Optional[str] = None
    type : int
    hideIfEmpty : bool
    sortType : str | None = None
    sortProperty : str | None = None
    isAscending : bool
    sortField : str | int | None = None
    sortFormula : str | int | None = None
    maxItemsPerPage : int | None = None
