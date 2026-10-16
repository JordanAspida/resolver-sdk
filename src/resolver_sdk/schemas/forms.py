"""
Pydantic models for Forms API responses.
"""
from .base import BaseResolverModel, FieldDetails, RelationshipDetails, FormulaDetails, RoleDetails, ReportDetails
from pydantic import Field
from typing import Any

# A model to map the details of a form
class FormDetails(BaseResolverModel):
    id : int
    name : str
    description : str | None = None
    priority : int
    type : int
    objectTypeId : int
    dataDefinitionId : int | None = None
    created : str
    modified : str | None = None
    hasObjectAssessments : bool
    hasComments : bool
    hasExternalMessages : bool
    title : str | None = None
    subTitle : str | None = None
    stateBar : bool
    stateControl : bool
    showUniqueId : bool
    showTranslate : bool
    showAnalyseText : bool = Field(alias="showAnalyzeText")
    showRelationshipGraph : bool
    showManageAssessments : bool
    historyTab : bool
    chatInterface : bool
    aiSummaryId : int | None = Field(default=None, alias="aiSummarizationSummaryId")
    hasAiSummaryExport : bool = Field(alias="aiSummarizationExportEnabled")
    externalRefId : str

# A model to map each rule in a form
class FormRules(BaseResolverModel):
    id : int
    sectionId : int 
    objectTypeId : int
    type : int
    identifier : int
    valueAnchorIds : list[int] = Field(default_factory=list)

# A model to map the configuration of each section in a form
class FormSection(BaseResolverModel):
    id : int
    name : str | None = None
    formId : int
    containerSectionId: int | None = None
    properties : dict[str, Any] | None = None
    ordinal : int | None = None
    nextSectionordinal : int | None = None
    nextComponentOrdinal : int | None = None
    created : str
    modified : str | None = None
    visibility : int | None = None
    title : str | None = None
    isSidebar : bool
    isCard : bool
    sectionIds : list[int] = Field(default_factory=list, alias="sections")
    componentIds : list[int] = Field(default_factory=list, alias="components")
    externalRefId : str

# A model to map each component in a form
class FormComponent(BaseResolverModel):
    id : int
    formId : int
    containerSectionId : int
    objectTypeId : int | None = None
    identifier : int | None = None
    type : int
    dataProperties : dict[str, Any] = Field(default_factory=dict)
    layoutProperties : Any | None = None
    subType : int
    ordinal : int
    created : str 
    modified : str | None = None
    sortType : str | int | None = None
    sortField : str | int | None = None
    sortProperty : int | None = None
    isAscending : bool

class NodeStateConfig(BaseResolverModel):
    id : int
    navFormConfigId : int | None = None
    stateId : int
    formId : int | None = None
    created : str
    modified : str | None = None
    navFormId : int
    externalRefId : str

class NavFormNode(BaseResolverModel):
    id : int
    navFormId : int
    objectTypeId : int
    dataDefinitionNodeId : int = Field(alias="dataDefinitionPathId")
    type : int
    formId : int | None = None
    reportId : int | None = None
    allWorkflows : bool
    created : str
    modified : str | None = None
    stateConfig : list[NodeStateConfig] = Field(default_factory=list)
    externalRefId : str

# A model to map the full structure of a form
class FormStructure(BaseResolverModel):
    sections : list[FormSection] = Field(default_factory=list)
    components : list[FormComponent] = Field(default_factory=list)
    form : FormDetails
    fields : list[FieldDetails] = Field(default_factory=list, alias="fieldType")
    relationships : list[RelationshipDetails] = Field(default_factory=list, alias="relationshipTypes")
    references : list[RelationshipDetails] = Field(default_factory=list, alias="incomingRelationshipTypes")
    formulas : dict[int, FormulaDetails] | list = Field(default_factory=list)
    roles : list[RoleDetails] = Field(default_factory=list)
    forms : list[FormDetails] = Field(default_factory=list)
    reports : list[ReportDetails] = Field(default_factory=list)
    rules : list[FormRules] = Field(default_factory=list)
