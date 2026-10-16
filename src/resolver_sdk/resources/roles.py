from ..schemas.roles import RoleDetails, RoleMembers, UserDetails, UserGroup, LifecycleId, RolePermissions

class RolesAPI:
    endpoint_get_all_roles = "/user/role"
    endpoint_get_role = "/user/role/{id}"
    endpoint_delete_role = "/user/role/{id}"
    endpoint_get_users_in_role = "/user/role/{id}/searchMembers"
    endpoint_get_lifecycles_for_role = "/data/rolePermissions/objectLifeCycles/role/{roleId}"
    endpoint_get_perms_for_object_in_role = "/data/rolePermissions/role/{roleId}/objectType/{objectTypeId}"

    # Initializes the RolesAPI with a client reference
    def __init__(self, client):
        self.client = client

    # Retrieves all roles with optional caching and refresh capability
    def get_all_roles(self, refresh=False) -> list[RoleDetails]:
        if self.client.cache["all_roles"] is not None and not refresh:
            return self.client.cache["all_roles"]
        response = self.client.safe_get(self.endpoint_get_all_roles)
        self.client.cache["all_roles"] = [RoleDetails(**role) for role in response.get("data", [])]
        return self.client.cache["all_roles"]

    # Retrieves users and groups that are members of a specific role
    def get_users_and_groups_in_role(self, role_id, query="id > 0") -> RoleMembers:
        response = self.client.safe_get(self.endpoint_get_users_in_role.format(id=role_id), params={"query": query})

        return RoleMembers(
            users=[UserDetails(**user) for user in response.get("users", [])],
            groups=[UserGroup(**group) for group in response.get("groups", [])]
        )

    # Retrieves details for a specific role by its ID
    def get_role(self, role_id) -> RoleDetails:
        return RoleDetails(**self.client.safe_get(self.endpoint_get_role.format(id=role_id)))

    # Deletes a specific role by its ID
    def delete_role(self, role_id):
        return self.client.safe_delete(self.endpoint_delete_role.format(id=role_id))

    # ROLE PERMISSIONS ENDPOINTS

    # Get lifecycle ids which have permissions to the given role
    def get_lifecycles_for_role(self, role_id) -> list[LifecycleId]:
        response = self.client.safe_get(self.endpoint_get_lifecycles_for_role.format(roleId=role_id))

        return [LifecycleId(**lifecycle) for lifecycle in response.get("data", [])]

    # Get role permissions for a specific object type for a specific role
    def get_obj_permissions_for_role(self, object_type_id, role_id) -> list[RolePermissions]:
        response = self.client.safe_get(self.endpoint_get_perms_for_object_in_role.format(roleId=role_id, objectTypeId=object_type_id))

        return [RolePermissions(**permission) for permission in response.get("data", [])]