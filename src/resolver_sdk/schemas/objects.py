"""
Pydantic models for Objects API responses & requests.
"""
from .base import *
from pydantic import Field
from typing import Optional

"""
Request Models
"""
# used as request model for update object endpoint, contains only the subset of fields that can be included in the request body for object updates (whereas ObjectCreateRequest is used as a more extended request model for add object endpoint where all fields that can be included in the request body when creating an object are included)
class ObjectRequest(BaseResolverModel):
    name : str
    description : str | None = None
    externalRefId : str | None = None

# used as request model for add object endpoint, contains all fields that can be included in the request body when creating an object (whereas ObjectRequest is used as a more generic request model for object update endpoints where only a subset of fields can be included in the request body)
class ObjectCreateRequest(ObjectRequest):
    anchor : int | str | None = None
    dimensions : int | str | None = None
    evaluations : list[Evaluation] | None = None
    relationships : list[Relationship] | None = None
    references : list[Relationship] | None = None
    roles : list[RoleEvaluationRequest] | None = None
    files : list[FileRequest] | None = None
    objectTypeId : int | str
    triggerId : int | str
    assessment : bool = False

"""
Response Models
"""
# used as response model for get all objects endpoint, contains subset of fields compared to ObjectDetailResponse
class ObjectsListResponse(BaseResolverModel):
    objects : list[ObjectSummary] = Field(alias="data")

# most limited response model used for when an endpoint returns a reference to a specific object
class ObjectReference(BaseResolverModel):
    objectId : int = Field(alias="id")
    name : str
    stateId : int | None = Field(alias="objectLifeCycleStateId")

# used as a response model for when an endpoint returns a few extra fields when referencing a specific object compared to ObjectReference but not the full set of fields returned in ObjectDetailResponse
class ObjectBasic(ObjectReference):
    uniqueId : int | float
    objectTypeId : int
    created : str
    lastSyncDate : str | None

# used as a minimised response model for get all objects endpoint when a more limited field/ property set are returned compared to ObjectDetailResponse  (where it is returning all properties / fields for a single specified object)
class ObjectSummary(ObjectBasic):
    description : str | None
    externalRefId : str
    evaluations : dict[int, EvaluationResponse] = Field(default_factory=dict) # fieldId > value (can be integer if multi-select/ numeric/ date, str if text, dict if RTF field)
    formulas : dict[int, Formula] = Field(default_factory=dict) # formulaId > formula details
    createdBy : int
    dateStateChanged : str | None = Field(alias="dateStateChanged")
    assessment : bool
    anchor : int | None = None

# used as response model for get object by id endpoint, contains all fields returned in the response
class ObjectDetailResponse(ObjectSummary):
    modified : str | None = None
    modifiedBy : int | None = None
    allowedTriggers : list[Optional[int]] | None = None
    uniqueIdArray : list[int] = Field(default_factory=list) # if assessment object splits unique id by '.' i.e. 1.2.3 becomes [1,2,3] to make it easier to work with in the case of clones where the unique id can be different to the library object unique id
    assessmentObjectId : int | None = None
    assessmentObjectTypeId : int | None = None
    assessmentLaunched : bool | None = None
    isArchive : bool = Field(False, alias="is_archive")
    roles : Roles | None = None

# used as a response model when an endpoint returns a reference to an objects assessment dimensions
class DimensionReference(BaseResolverModel):
    type : int # refers to which dimension this object relates to, typically just one as most assessments only have one dimension
    optionId : int # typically refers to the dimensions object id
    dimensionId : int # Typically refers to the dimensions object type id

# used in the get assessment data endpoint and maps the fields returned within the "clones" array
class ObjectCloneInfo(ObjectReference):
    objectTypeId : int
    externalRefId : str | None = None
    assessmentObjectId : int | None = None
    assessmentObjectTypeId : int | None = None
    isArchive : bool = Field(False, alias="is_archive")
    modified : str | None = None
    lastSyncDate : str | None = None
    formulas : dict[int, Formula] = Field(default_factory=dict)
    dimensions : list[DimensionReference] = Field(default_factory=list)
    uniqueIdArray : list[int] = Field(default_factory=list) # if assessment object splits unique id by '.' i.e. 1.2.3 becomes [1,2,3] to make it easier to work with in the case of clones where the unique id can be different to the library object unique id

# used in the get assessment data endpoint and maps the fields returned within the "clonesWithSharedAssessments" array which contains basic info on the clone and which assessment it is linked to
class ObjectCloneAssessmentInfo(ObjectReference):
    uniqueId : int | float
    objectTypeId : int
    assessmentObjectId : int
    assessmentObjectTypeId : int
    assessmentName : str = Field(alias="assessmentObjectName")
    dimensions : list[DimensionReference] = Field(default_factory=list)
    modified : str | None = None
    lastSyncDate : str | None = None
    uniqueIdArray : list[int] = Field(default_factory=list) # if assessment object splits unique id by '.' i.e. 1.2.3 becomes [1,2,3] to make it easier to work with in the case of clones where the unique id can be different to the library object unique id

# used as response model for check object exists endpoint, returns exists: true if the specified object already exists in Resolver
class ObjectExistsResponse(BaseResolverModel):
    exists: bool

# used as a response model for the add object endpoint, contains the fields returned in the response after creating an object via the endpoint
class ObjectCreateResponse(BaseResolverModel):
    objectId : int = Field(alias="id")
    uniqueId : int | float
    name : str
    externalRefId : str
    stateId : int = Field(alias="objectLifeCycleStateId")
    uniqueIdArray : list[int] = Field(default_factory=list) # if assessment object splits unique id by '.' i.e. 1.2.3 becomes [1,2,3] to make it easier to work with in the case of clones where the unique id can be different to the library object unique id

# Model which maps the assessment update resulks i.e. for each assessment provides a list of the clones which were create / updated & the relationships which were made
class AssessmentUpdateResult(BaseResolverModel):
    createdClones : list[int] = Field(alias="createdCloneIds")
    updatedClones : list[int] = Field(alias="updatedCloneIds")
    relationships : list[int] = Field(alias="relationshipIds")

# Model for the update assessments response returns a list of all the results for the assessments, as well as any errors and the message requests
class AssessmentsUpdateResponse(BaseResolverModel):
    results : list[AssessmentUpdateResult]
    errors : list[Error]
    messageRequests : MessageRequest

# used as a response model for the get assessment data endpoint, contains the fields returned in the "clonesGroupByLibraryObjects" array which returns the clones grouped by the original library object they were cloned from with all their fields for each clone
class ClonesByObject(BaseResolverModel):
    objectId : int = Field(alias="libraryObject")
    clones : list[ObjectCloneInfo] 

# used as a response model for the get assessment data endpoint, maps all the returned arrays in the response to corresponding fields in the model for easier access to the data returned in the response (& validation of the response data structure)
class AssessmentDataResponse(BaseResolverModel):
    assessmentObjects : list[ObjectBasic]
    dimensions : list[ObjectReference] = Field(alias="objectTypeDimensionObjects")
    clonesByObj : list[ClonesByObject] = Field(alias="clonesGroupByLibraryObjects") # list of objects with all their fields for each clone grouped by the original object id they were cloned from
    cloneAssessments : list[ObjectCloneAssessmentInfo] = Field(alias="clonesWithSharedAssessments") # list of all clones with all their fields without grouping by the original object id they were cloned from

class RelatedObjectsListResponse(BaseResolverModel):
    pass


class ObjectRelationshipResponse(BaseResolverModel):
    pass
