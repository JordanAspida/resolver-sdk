from ..schemas.objects import *

class ObjectsAPI:
    endpoint_get_all_objects = "/data/object"
    endpoint_get_object = "/data/object/{id}"
    endpoint_check_object_exists = "/data/object/{id}/exists"
    endpoint_object_count = "/data/object/count"
    endpoint_add_object = "/creation/creation"
    endpoint_update_object = "/data/object/{id}"
    endpoint_delete_object = "/data/object/{id}"
    endpoint_update_assessments = "/creation/assessments/{libraryObjectId}"
    endpoint_get_assessment_data = "/data/object/assessment/allRelatedAssessmentData"
    endpoint_get_related_objects_by_type = "/data/object/{objectId}/relationships/{relationshipTypeId}"
    endpoint_relate_objects = "/creation/creation/{objectId}/relationship/{relationshipTypeId}/relatedObject/{relatedObjectId}"

    # Initializes the ObjectsAPI with a client reference
    def __init__(self, client):
        self.client = client

    # Retrieves all objects optionally limited by objectType or an array of object ids
    def get_all_objects(self, obj_type_id=None, ids=None, page_size=100, page_number=None,exclude_clones=False) -> ObjectsListResponse:
        params = {
            "objectTypeId": obj_type_id,
            "pageSize": page_size,
            "pageNumber": page_number,
            "excludeClones": str(exclude_clones).lower(),
            "ids": ids
        }

        response = ObjectsListResponse(**self.client.safe_get(self.endpoint_get_all_objects, params=params))
        
        return response

    # Retrieves an objct info via id
    def get_object(self, obj_id, by_ref=False, include_field_metadata=False, include_formula_metadata=False) -> ObjectDetailResponse:
        params = {
            "byRef": str(by_ref).lower(), # Transforms into str and lower case since Resolver API expects "true" for boolean True
            "includeFieldMetaData": str(include_field_metadata).lower(),
            "includeFormulaMetaData": str(include_formula_metadata).lower()
            }
        
        return ObjectDetailResponse(**self.client.safe_get(self.endpoint_get_object.format(id=obj_id), params=params))

    # Returns exists: true if a specific object already exists
    def check_object_exists(self, obj_id, by_ref=False) -> ObjectExistsResponse:
        params = {
            "byRef": str(by_ref).lower()
        }

        response = ObjectExistsResponse(**self.client.safe_get(self.endpoint_check_object_exists.format(id=obj_id), params=params))

        return response
    
    # Returns the number of objects of a specific type (optionally restricted by objects which have a specific relationship)
    def object_count(self, obj_type_id=None, rel_type_id=None) -> int:
        params = {
            "objectTypeId":obj_type_id,
            "relationshipTypeId": rel_type_id
        }

        return int(self.client.safe_get(self.endpoint_object_count, params=params))

    # Adds an object to Resolver after specifying a JSON body
    def add_object(self, body, by_ref=False, email_id=None) -> ObjectCreateResponse:
        params = {
            "byRef": str(by_ref).lower(),
            "emailAddressId": email_id
        }

        return ObjectCreateResponse(**self.client.safe_post(self.endpoint_add_object, params=params, body=body))

    # Updates a specific object (limited to properties only for this endpoint)
    def update_object(self, obj_id, body, by_ref=False) -> None:
        params = {
            "byRef": str(by_ref).lower()
        }

        self.client.safe_put(self.endpoint_update_object.format(id=obj_id), params=params, body=body)

    # Deletes the specified object
    def delete_object(self, obj_id, by_ref=False, use_job=False, retention_enabled=False) -> None:
        params = {
            "byRef": str(by_ref).lower(),
            "useJob":str(use_job).lower(), 
            "retentionEnabled":str(retention_enabled).lower()
        }

        self.client.safe_delete(self.endpoint_delete_object.format(id=obj_id), params=params)

    # Updates the specified assessments in two ways
    # IF there is an existing assessment object of the specified library object:
    #   - All the fields selected in the "fields to sync" (in assessment config for the specified object type) option will be updated from the library object > assessment object
    # IF there is NOT an existing assessment object of the specified library object:
    #   - It will create a new assessment object in all assessments (meeting the above condition) which is an exact copy of the library object
    #   - One caveat is that the object can only be created if its parent object is already apart of the specified object
    #   - If you attempt to update an assessment with an object who's parent does not exist in that assessment the action will error
    def update_assessments(self, obj_id, assessment_ids, use_job=True) -> AssessmentsUpdateResponse:
        params = { "useJob":str(use_job).lower() }

        body = { "assessmentIds":assessment_ids }
        
        # If a job is used this section triggers and will constantly poll the job status until it has been executed and then returns the response
        if use_job == True:
            job_id = self.client.safe_post(self.endpoint_update_assessments.format(libraryObjectId=obj_id), params=params, body=body).get("jobId")

            return AssessmentsUpdateResponse(**self.client.utility.wait_for_job(job_id=job_id).payload)
        
        # Only triggers if a job is not used and instantly returns the response.
        return AssessmentsUpdateResponse(**self.client.safe_post(self.endpoint_update_assessments.format(libraryObjectId=obj_id), params=params, body=body))

    # Retrieves all the assessment clones for a set of object ids
    def get_assessment_data(self, object_ids : list[int]) -> AssessmentDataResponse:
        # Bug in API where a single value in an array is treated as an int or str rather than an array
        # So to fix I have forced the duplication of any single value arrays
        if len(object_ids) == 1: 
            object_ids = [object_ids[0], object_ids[0]]

        params = { "libraryObjectIds" : object_ids }

        return AssessmentDataResponse(**self.client.safe_get(self.endpoint_get_assessment_data, params=params))

    # Retrieve all related objects for a given object & relationship type
    def get_related_objects(self, obj_id, rel_type_id, by_ref=False):
        params = { "byRef" : by_ref }

        return self.client.safe_get(self.endpoint_get_related_objects_by_type.format(objectId=obj_id, relationshipTypeId=rel_type_id), params=params)

    # Relate one object with another, should_clone clones assessment objects when relating assessment objects so 1.1 becomes 1.1.1
    def relate_objects(self, obj_id, rel_type_id, rel_obj_id, by_ref=False, should_clone=False):
        params = {
            "byRef": by_ref,
            "shouldClone": should_clone
        }

        return self.client.safe_post(self.endpoint_relate_objects.format(objectId=obj_id, relationshipTypeId=rel_type_id, relatedObjectId=rel_obj_id), params=params)
