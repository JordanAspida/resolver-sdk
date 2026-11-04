"""
Pydantic models for Reports API responses.
"""
from typing import Any, Optional

from pydantic import Field

from .base import BaseResolverModel


class ReportsListResponse(BaseResolverModel):
    id : int
    name : str
    description : str | None = None
    objectTypeId : int
    created : str
    modified : str | None = None
    org : int
    nextReportComponentOrdinal : int
    type : int
    showArchiveData : bool
    enableReportExports : bool
    orientation : int
    externalRefId : str

class TableColumn(BaseResolverModel):
    id : int 
    componentId : int
    nodeId : int
    type : int
    ordinal : int | None = None
    subtype : int | None = None
    identifier : str | int | None = None
    objectTypeId : int | list[int] |None = None
    created : str
    modified : str | None = None
    org : int
    readOnly : bool
    reportId : int | str | None = None
    defaultSortColumn : int | str | bool | None = None
    defaultSortDirection : str | None = None
    path : str | None = None
    externalRefId : str

class Series(BaseResolverModel):
    series : int | None = None
    xAxisType : int | None = None
    xValue : int | str | None = None
    yAxisType : int | None = None
    yValue : int | str | None = None
    label : str | None = None

class ComponentProperties(BaseResolverModel):
    enabledForms : dict = Field(default_factory=dict)
    forms : dict = Field(default_factory=dict)
    columns : list[TableColumn] = Field(default_factory=list)
    parameters : list[Any] = Field(default_factory=list)
    titles : dict = Field(default_factory=dict)
    subtype : int | None = None
    componentDataDefinitionId : int | None = None
    reportDataDefinitionId : int | None = None
    showTotals : Optional[bool] = None
    content : str | None = None
    xAxisLabel : str | None = None
    yAxisLabel : str | None = None
    groupByType : Optional[int] = None
    groupById : Optional[int] = None
    displayColourMode : Optional[int] = Field(default=None, alias="displayColorMode")
    series : Optional[list[Series]] = None

class ReportComponentsListResponse(BaseResolverModel):
    id : int
    reportId : int
    reportDataDefinitionId : int | None = None
    componentDataDefinitionId : int | None = None
    dataProperties : ComponentProperties | None = None
    displayProperties : dict = Field(default_factory=dict)
    showTotals : Optional[bool] = None
    allData : Optional[bool] = None
    libraryData : Optional[bool] = None
    content : str | None = None
    groupByType : Optional[int] = None
    groupByRelationshipId : Optional[int] = None
    groupByObjectTypeId : Optional[int] = None
    type : int
    subType : int | None = None
    ordinal : int
    created : str
    modified : str | None = None
    org : int
    displayColourMode : Optional[int] = Field(default=None, alias="displayColorMode")
    externalRefId : str
