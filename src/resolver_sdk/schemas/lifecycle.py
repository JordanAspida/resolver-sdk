"""
Pydantic models for Lifecycle API responses.
"""

from typing import Optional
from pydantic import Field

from .base import BaseResolverModel

class ActionInfo(BaseResolverModel):
    id : int
    name : str 
    objectTypeId : int | None = None
    transitionId : int | None = None
    type : int
    subType : int | None = None
    fieldId : int | None = None
    setFieldValue : int | list | None = None
    created : str
    modified : str | None = None
    objectLifeCycleId : int
    externalRefId : str
    options : dict | None = Field(default_factory=dict)

class ActionDetails(BaseResolverModel):
    stateId : int
    stateExternalRefId : str | None = None
    stateName : str | None = None
    actionId : int
    actionName : str | None = None
    actionExternalRefId : str | None = None
    actionType : int
    triggerId : int | None = None
    triggerName : str | None = None
    objectLifeCycleId : int
    objectTypeId : int
    org : int

class TransitionDetails(BaseResolverModel):
    id : int
    name : str
    triggerId : int
    destinationStateId : int | None = None
    formulaId : int | None = None
    created : str
    modified : str | None = None
    org : int
    byPass : bool
    transitionCompleteAction : str | None = None
    objectLifeCycleId : int
    autoDelete : bool
    isSystemConfig : bool
    externalRefId : str

class TriggerDetails(BaseResolverModel):
    id : int
    orchestrationEventId : int | None = None
    type : int
    name : str
    description : str | None = None
    color : str | None = None
    objectLifeCycleId : int
    layoutProperties : dict | None = None
    created : str
    modified : str | None = None
    org : int
    externalRefId : str
    frequency : str | int | None = None
    icon : str | None = None
    isWorkflow : bool
    scheduleFieldId : int | None = None
    scheduleFormulaId : int | None = None
    scheduleType : int | None = None
    isSystemConfig : bool
    transitions : list[int] | None = None

class StateDetails(BaseResolverModel):
    id : int
    name : str
    ordinal : int
    stateCategoryId : int | None = None
    color : str | None = None
    created : str
    modified : str | None = None
    org : int
    objectLifeCycleId : int
    creation : Optional[bool] | None = None
    triggers : Optional[list[int]] | None = None

class LifecyclesListResponse(BaseResolverModel):
    id : int
    name : str
    type : int
    description : str | None = None
    created : str
    modified : str | None = None
    org : int
    nextStateOrdinal : int | None = None
    objectTypeId : int
    isSystemConfig : bool
    states : Optional[list[StateDetails]] | None = None
    externalRefId : str


class StatesAndTransitionsResponse(BaseResolverModel):
    states : list[StateDetails]
    triggers : Optional[list[TriggerDetails]] | None = None
    transitions : Optional[list[TransitionDetails]] | None = None

