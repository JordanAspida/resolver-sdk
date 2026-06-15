"""
Base Resolver SDK Pydantic model with configuration.
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Any


class BaseResolverModel(BaseModel):
    """Base model for all Resolver SDK Pydantic models with extra fields allowed."""
    model_config = ConfigDict(extra="allow")

# common models used across multiple endpoints/ resources

class Error(BaseResolverModel):
    errorMessage : str

# Evaluation model used in objects endpoint responses to represent field evaluations for objects
class Evaluation(BaseResolverModel):
    value: str | int | dict[str, Any] | list[dict[str, Any]] | bool | None = None
    fieldId : int | str | None = None

# Evaluation model used in objects endpoint responses to represent field evaluations for objects where the response contains a more extended set of fields/ properties for the evaluation compared to Evaluation
class EvaluationResponse(Evaluation):
    modified : str | None = None
    modifiedBy : int | None = None
    externalRefId : str | None = None
    uniqueName : str | None = None

# Formula model used in objects endpoint responses to represent formula evaluations for objects
class Formula(BaseResolverModel):
    color : str | None = None
    label : int | str | None = None
    range : str | None = None
    value : int | float
    rangeId : int | None = None
    formulaName : str | None = None
    lastCalculated : str | None = None
    externalRefId : str | None = None

# Relationship model used in objects endpoint responses to represent relationships and references for objects where the relationship/ reference can contain either a list of object ids or a list of strings depending on whether the endpoint is byRef or not
class Relationship(BaseResolverModel):
    relationshipId : int | str | None = None
    value : list[int] | list[str] | None = None

# Role Evaluation model used in objects endpoint responses to represent role assignments for objects returning all assigned role ids and their corresponding users and groups
class RoleEvaluation(BaseResolverModel):
    roleId : int
    users : list[int] = Field(default_factory=list)
    groups : list[int] = Field(default_factory=list)

# Role Evaluation model used in request bodies to represent role assignments for objects 
class RoleEvaluationRequest(BaseResolverModel):
    roleId : int
    users : list[int] = Field(default_factory=list)
    userGroups : list[int] = Field(default_factory=list)

# File model used in objects endpoint request bodies to represent file attachments for objects
class FileRequest(BaseResolverModel):
    fileId : int
    fieldId : int

#  User model used in objects endpoint responses to represent user information
class User(BaseResolverModel):
    userId : int = Field(alias="id")
    fname : str | None = Field(None, alias="first")
    lname : str | None = Field(None, alias="last")
    email : str | None = None
    modified : str | None = None
    created : str | None = None
    externalRefId : str | None = None
    lastLogin : str | None = None

# User Group model used in objects endpoint responses to represent user group information
class UserGroup(BaseResolverModel):
    groupId : int = Field(alias="id")
    name : str | None = None
    description : str | None = None
    created : str | None = None
    modified : str | None = None
    createdBy : int | None = None
    modifiedBy : int | None = None
    org : int | None = None
    externalRefId : str | None = None

# Roles model used in objects endpoint responses to represent all role assignments for an object, containing a list of RoleEvaluation (representing assigned roles and their corresponding users and groups), a list of all users with assigned roles, and a list of all groups with assigned roles
class Roles(BaseResolverModel):
    roleEvaluations : list[RoleEvaluation] | None = None
    users : list[User] | None = None
    groups : list[UserGroup] | None = None

# Model which maps the fields from the $metadata list in the search index requests for the update assessments endpoint
class MetaData(BaseResolverModel):
    statusCode : int = Field(alias="httpStatusCode")
    requestId : str
    attempts : int
    totalRetryDelay : int

# Model to map the search index requests from the update assessments endpoint
class SearchIndexRequest(BaseResolverModel):
    metadata : MetaData = Field(alias="$metadata")
    messageHash : str = Field(alias="MD5OfMessageBody")
    messageId : str = Field(alias="MessageId")
    sequenceNumber : str = Field(alias="SequenceNumber")

# Model to map the message requests from the updates assesssments endpoint
class MessageRequest(BaseResolverModel):
    searchIndexRequests : list[SearchIndexRequest]
    evaluationFormulaUpdateRequests : list[bool]
    relationshipFormulaUpdateRequests : list[bool]