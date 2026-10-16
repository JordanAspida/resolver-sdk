from ..schemas.applications import ApplicationsListResponse, ActivitiesListResponse, ActionsListResponse, ViewsListResponse

class ApplicationsAPI:
    endpoint_get_apps = "/object/application"
    endpoint_get_activities = "/object/application/{applicationId}/activity"
    endpoint_get_actions = "/object/application/{applicationId}/activity/{activityId}/action"
    endpoint_get_views = "/object/application/{applicationId}/activity/{activityId}/view"

    # Initializes the ApplicationsAPI with a client reference
    def __init__(self, client):
        self.client = client

    # Retrieves all applications with optional caching and refresh capability
    def get_all_applications(self, refresh=False) -> list[ApplicationsListResponse]:
        if self.client.cache["all_applications"] is not None and not refresh:
            return self.client.cache["all_applications"]
        
        response = self.client.safe_get(self.endpoint_get_apps)
        self.client.cache["all_applications"] = [ApplicationsListResponse(**app) for app in response.get("data", [])]
        return self.client.cache["all_applications"]

    # Retrieves activities for a specific application by application ID
    def get_activities(self, app_id) -> list[ActivitiesListResponse]:
        return [ActivitiesListResponse(**activity) for activity in self.client.safe_get(self.endpoint_get_activities.format(applicationId=app_id)).get("data", [])]

    # Retrieves actions for a specific activity, optionally including form references
    def get_actions(self, app_id, activity_id, include_form_ref=True) -> list[ActionsListResponse]:
        params = {"includeFormRef": include_form_ref}
        return [ActionsListResponse(**action) for action in self.client.safe_get(self.endpoint_get_actions.format(applicationId=app_id, activityId=activity_id), params=params).get("data", [])]

    # Retrieves views for a specific activity within an application
    def get_views(self, app_id, activity_id) -> list[ViewsListResponse]:
        return [ViewsListResponse(**view) for view in self.client.safe_get(self.endpoint_get_views.format(applicationId=app_id, activityId=activity_id)).get("data", [])]
