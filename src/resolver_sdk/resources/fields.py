from ..schemas.base import ObjectTypeDetails, FieldDetails

class FieldsAPI:
    # Endpoints here
    endpoint_get_all_fields = "/object/field"
    endpoint_get_field_obj_types = "/object/field/{id}/objectType"

    # Initialises FieldsAPI with a ResolverClient instance
    def __init__(self, client):
        self.client = client

    # Retrieves all fields with optional search text, specific IDs, and field options
    def get_all_fields(self, search_text=None, ids : list[str] | None = None, field_options=False) -> list[FieldDetails]:
        params = {
            "searchText": search_text,
            "ids": ids,
            "includeFieldOptions": str(field_options).lower()
        }

        response = self.client.safe_get(self.endpoint_get_all_fields, params=params)
        return [FieldDetails(**field) for field in response.get("data", [])]

    # Endpoint to retrieve all of the object types which use a given field
    def get_all_obj_types_for_field(self, field_id) -> list[ObjectTypeDetails]:

        response = self.client.safe_get(self.endpoint_get_field_obj_types.format(id=field_id))
        return [ObjectTypeDetails(**obj_type) for obj_type in response]