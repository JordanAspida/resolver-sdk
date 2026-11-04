from ..schemas.object_type_groups import ObjectTypeGroupDetails
from ..schemas.object_types import ExpandedObjectTypeDetails

class ObjectTypeGroupsAPI:
    endpoint_get_obj_type_grps = "/object/objectTypeGroup"
    endpoint_get_obj_types_for_group = "/object/objectTypeGroup/{id}/objectType"

    def __init__(self, client) -> None:
        self.client = client

    # Get all object type groups
    def get_all_obj_type_grps(self, search_string=None, ids=[], limit=None) -> list[ObjectTypeGroupDetails]:
        params = {
            "search" : search_string,
            "ids" : ids,
            "limit" : limit
        }
        response = self.client.safe_get(self.endpoint_get_obj_type_grps, params=params).get("data", [])
        return [ObjectTypeGroupDetails(**obj_type_grp) for obj_type_grp in response]

    # Get all object types for object type group
    def get_obj_types_for_grp(self, obj_type_grp_id) -> list[ExpandedObjectTypeDetails]:
        response = self.client.safe_get(self.endpoint_get_obj_types_for_group.format(id=obj_type_grp_id))

        return [ExpandedObjectTypeDetails(**obj_type) for obj_type in response]

    