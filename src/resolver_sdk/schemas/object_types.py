"""
Pydantic models for Object Types API responses.
"""

from pydantic import Field

from .base import ObjectTypeDetails

class ExpandedObjectTypeDetails(ObjectTypeDetails):
    colour : str | None = Field(default=None, alias="Color")
    nextElement : int | None = None
    org : int
    anchor : int | None = None 
    anchorRelationship : int | None = None
    dataDefinitionId : int | None = None
    retentionEnabled : bool
    isSystemConfig : bool

