"""
Pydantic models for Formulas API responses & requests.
"""
from .base import BaseResolverModel
from typing import Any

"""
Responses
"""

class FormulaDetails(BaseResolverModel):
    id : int
    name : str
    description : str | None = None
    script : str | None = None
    format : int | str | None = None
    formatStyle : int | None = None
    formatCurrency : str | int | None = None
    rangeStyle : int | None = None
    objectTypeId : int | None = None
    objectLifeCycleId : int | None = None
    type : int 
    created : str
    modified : str | None = None
    org : int
    transitionId : int | None = None
    metadata : dict[Any, Any] | None = None
    retentionEnabled : bool 
    isSystemConfig : bool 
    externalRefId : str

class FormulaVariable(BaseResolverModel):
    id : int
    name : str
    description : str | None = None
    formulaId : int
    type : int
    subtype : int
    fieldId : int | None = None
    stateId : int | None = None
    defaultNull : bool
    objectTypeId : int | None = None
    relationshipTypes : list | int | None = None
    created : str
    modified : str | None = None
    org : int
    targetFormulaId : int | None = None
    propertyId : int | None = None
    targetObjectTypeId : int | None = None
    objectLifeCycleId : int | None = None




