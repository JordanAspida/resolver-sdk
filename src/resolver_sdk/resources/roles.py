class RolesAPI:
    endpoint_get_all_roles = "/user/role"
    endpoint_get_role = "/user/role/{id}"
    endpoint_delete_role = "/user/role/{id}"
    endpoint_get_users_in_role = "/user/role/{id}/searchMembers"

    # Initializes the RolesAPI with a client reference
    def __init__(self, client):
        self.client = client

    # Retrieves all roles with optional caching and refresh capability
    def get_all_roles(self, refresh=False):
        if self.client.cache["all_roles"] is not None and not refresh:
            return self.client.cache["all_roles"]
        response = self.client.safe_get(self.endpoint_get_all_roles)
        self.client.cache["all_roles"] = response.get("data", [])
        return self.client.cache["all_roles"]

    # Retrieves users and groups that are members of a specific role
    def get_users_and_groups_in_role(self, role_id, query="id > 0"):
        response = self.client.safe_get(self.endpoint_get_users_in_role.format(id=role_id), params={"query": query})
        return response.get("users", []), response.get("groups", [])

    # Retrieves details for a specific role by its ID
    def get_role(self, role_id):
        return self.client.safe_get(self.endpoint_get_role.format(id=role_id))

    # Deletes a specific role by its ID
    def delete_role(self, role_id):
        return self.client.safe_delete(self.endpoint_delete_role.format(id=role_id))
