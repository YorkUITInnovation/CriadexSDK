from httpx import AsyncClient

from CriadexSDK.core.api.router import Router
from .about import GroupAboutRoute
from .create import GroupCreateRoute
from .delete import GroupDeleteRoute


class GroupsRouter(Router):

    def __init__(self, api_base: str, http: AsyncClient):
        super().__init__(api_base, http)

        self.about: GroupAboutRoute = self._create_route(GroupAboutRoute)
        self.delete: GroupDeleteRoute = self._create_route(GroupDeleteRoute)
        self.create: GroupCreateRoute = self._create_route(GroupCreateRoute)


__all__ = ["GroupsRouter"]
