from httpx import AsyncClient

from CriadexSDK.core.api.router import Router
from CriadexSDK.routers.group_auth.check import GroupAuthCheckRoute
from CriadexSDK.routers.group_auth.create import GroupAuthCreateRoute
from CriadexSDK.routers.group_auth.delete import GroupAuthDeleteRoute
from CriadexSDK.routers.group_auth.list import GroupAuthListRoute


class GroupAuthRouter(Router):

    def __init__(self, api_base: str, http: AsyncClient):
        super().__init__(api_base, http)

        self.check: GroupAuthCheckRoute = self._create_route(GroupAuthCheckRoute)
        self.create: GroupAuthCreateRoute = self._create_route(GroupAuthCreateRoute)
        self.delete: GroupAuthDeleteRoute = self._create_route(GroupAuthDeleteRoute)
        self.list: GroupAuthListRoute = self._create_route(GroupAuthListRoute)


__all__ = ["GroupAuthRouter"]
