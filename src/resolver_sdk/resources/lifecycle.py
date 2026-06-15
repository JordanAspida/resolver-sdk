class LifecycleAPI:
    endpoint_get_lifecycles = "/object/objectLifeCycle"
    endpoint_get_state_actions = "/object/objectLifeCycleState/actions"
    endpoint_get_states = "/object/objectType/{objectTypeId}/objectLifeCycle/{objectLifeCycleId}/state"
    endpoint_get_transitions = "/object/objectType/{objectTypeId}/objectLifeCycle/{objectLifeCycleId}/trigger/{triggerId}/transition"
    endpoint_get_transition_actions = "/object/objectType/{objectTypeId}/objectLifeCycle/{objectLifeCycleId}/transition/{transitionId}/action"

    # Initializes the LifecycleAPI with a client reference
    def __init__(self, client):
        self.client = client

    # Retrieves all object lifecycles with optional states and caching capability
    def get_all_lifecycles(self, states=True, refresh=False):
        if self.client.cache["all_lifecycles"] is not None and not refresh:
            return self.client.cache["all_lifecycles"]
        response = self.client.safe_get(self.endpoint_get_lifecycles, {"includeStates": states})
        self.client.cache["all_lifecycles"] = response.get("data", [])
        return self.client.cache["all_lifecycles"]

    # Retrieves states and transitions for a specific lifecycle of an object type
    def get_states_and_transitions(self, obj_type_id, lifecycle_id, deep=True):
        response = self.client.safe_get(self.endpoint_get_states.format(objectTypeId=obj_type_id, objectLifeCycleId=lifecycle_id), {"deep": deep})
        return response.get("states", []), response.get("triggers", []), response.get("transitions", [])

    # Retrieves actions for specified lifecycle states
    def post_state_actions(self, state_ids, action_type=None):
        return self.client.safe_post(self.endpoint_get_state_actions, body={"stateIds": state_ids, "actionTypes": action_type})

    # Retrieves transitions triggered by a specific trigger in a lifecycle
    def get_trigger_transitions(self, obj_type_id, lifecycle_id, trigger_id):
        return self.client.safe_get(self.endpoint_get_transitions.format(objectTypeId=obj_type_id, objectLifeCycleId=lifecycle_id, triggerId=trigger_id)).get("data", [])

    # Retrieves actions associated with a specific transition
    def get_transition_actions(self, obj_type_id, lifecycle_id, transition_id):
        return self.client.safe_get(self.endpoint_get_transition_actions.format(objectTypeId=obj_type_id, objectLifeCycleId=lifecycle_id, transitionId=transition_id))
