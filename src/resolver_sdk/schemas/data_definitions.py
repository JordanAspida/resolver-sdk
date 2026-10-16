"""
Pydantic models for Data Definitions API responses.
"""
from typing import Any
from pydantic import Field

from .base import BaseResolverModel

# DataPath model used in data definitions endpoint responses to represent the structure of a data definition
class DataPath(BaseResolverModel):
    objectType : int
    relationshipType : int | None = None
    relationshipExtRefId : str | None = None
    inverse : bool | None = None
    nodeId : int | None = None
    children : list[DataPath] | None = None

# Data Definition model used in data definitions endpoint responses to represent data definition details
class DataDefinitionDetails(BaseResolverModel):
    id : int
    name : str
    description : str | None
    definition : DataPath
    objectTypeId : int
    created : str | None
    externalRefId : str | None

class ReportFocus(BaseResolverModel):
    id : int
    reportId : int
    dataDefinitionId : int
    org : int

class ReportComponent(BaseResolverModel):
    id : int
    reportId : int
    reportDataDefinitionId : int
    componentDataDefinitionId : int
    type : int
    subtype : int
    ordinal : int
    externalRefId : str

class OrchestrationEventAction(BaseResolverModel):
    id : int
    name : str
    objectTypeId : int
    transitionId : int
    created : str
    modified : str | None = None
    org : int
    externalRefId : str
    dataDefinitionId : int
    objectLifeCycleId : int
    type : int

class FormRef(BaseResolverModel):
    id : int
    name : str

class AiConfig(BaseResolverModel):
    id : int
    org : int
    dataDefinitionId : int
    externalRefId : str
    name : str
    description : str | None = None

class AssessmentType(BaseResolverModel):
    id : int
    name : str
    description : str | None = None
    monogram : str
    objectLifeCycleId : int
    externalRefId : str
    assessment : bool = True
    anchor : int 
    anchorRelationship : int
    dataDefinitionId : int

class NavFormRef(FormRef):
    description : str | None = None
    type : int
    objectTypeId : int
    dataDefinitionId : int
    externalRefId : str

class ValueConcat(BaseResolverModel):
    id : int
    objectTypeId : int | None = None
    fieldId : int | None = None
    dataDefinitionId: int
    property : int | None = None
    expression : str | None = None
    type : int
    created : str
    modified : str | None = None
    org : int
    externalRefId : str


class DataDefinitionDependents(BaseResolverModel):
    assessmentTypes : list[AssessmentType] = Field(default_factory=list, alias="Assessment Types")
    navForms : list[NavFormRef] = Field(default_factory=list, alias="Nav Forms")
    reportFocuses : list[ReportFocus] = Field(default_factory=list, alias="Report Focuses")
    reportComponents : list[ReportComponent] = Field(default_factory=list, alias="Report Components")
    orchestrationEventActions : list[OrchestrationEventAction] = Field(default_factory=list, alias = "Orchestration Event Actions")
    valueConcatenations : list[ValueConcat] = Field(default_factory=list, alias="Value Concatenations")
    aiSummarisationForms : list[FormRef] = Field(default_factory=list, alias="Forms Using AI Summarizations")
    aiSummaryConfigs : list[AiConfig] = Field(default_factory=list)
