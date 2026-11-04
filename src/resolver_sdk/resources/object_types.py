from ..schemas.object_types import ExpandedObjectTypeDetails

class ObjectTypesAPI:
    endpoint_get_all_obj_types = "/object/objectType"

    def __init__(self, client):
        self.client = client

    def get_all_obj_types(self) -> list[ExpandedObjectTypeDetails]:
        response = self.client.safe_get(self.endpoint_get_all_obj_types).get("data", [])

        return [ExpandedObjectTypeDetails(**obj_type) for obj_type in response]
