from ..schemas.user_groups import *

class UserGroupsAPI:
    endpoint_get_users_in_group = "/user/group/{id}/users"

    def __init__(self, client):
        self.client = client

    # Get all users in a specified group
    def get_users_in_group(self, group_id) -> list[UserInfo]:

        users = self.client.safe_get(self.endpoint_get_users_in_group.format(id=group_id))["data"]
        print(users)
        return [UserInfo(**user) for user in users]