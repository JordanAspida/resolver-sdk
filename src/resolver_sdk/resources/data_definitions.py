from ..schemas.data_definitions import DataDefinitionDetails, DataDefinitionDependents

class DataDefinitionsAPI:
    # Endpoints here
    endpoint_get_all_data_definitions = "/object/dataDefinition"
    endpoint_get_data_definition_dependents = "/object/dataDefinition/{id}/dependents"

    def __init__(self, client):
        self.client = client

    # Retrieves all data definitions
    def get_all_data_definitions(self) -> list[DataDefinitionDetails]:
        response = self.client.safe_get(self.endpoint_get_all_data_definitions).get("data", [])
        return [DataDefinitionDetails(**item) for item in response]

    # Get all entities linked to this data definition
    def get_data_definition_dependents(self, data_definition_id: int) -> DataDefinitionDependents:

        response = self.client.safe_get(self.endpoint_get_data_definition_dependents.format(id=data_definition_id))
        return DataDefinitionDependents(**response)
        