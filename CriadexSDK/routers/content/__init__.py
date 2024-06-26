from httpx import AsyncClient

from CriadexSDK.core.api.router import Router
from CriadexSDK.routers.content.delete import GroupContentDeleteRoute
from CriadexSDK.routers.content.list import GroupContentListRoute
from CriadexSDK.routers.content.search import GroupContentSearchRoute
from CriadexSDK.routers.content.update import GroupContentUpdateRoute
from CriadexSDK.routers.content.upload import GroupContentUploadRoute


class ContentRouter(Router):

    def __init__(self, api_base: str, http: AsyncClient):
        super().__init__(api_base, http)

        self.upload: GroupContentUploadRoute = self._create_route(GroupContentUploadRoute)
        self.update: GroupContentUpdateRoute = self._create_route(GroupContentUpdateRoute)
        self.delete: GroupContentDeleteRoute = self._create_route(GroupContentDeleteRoute)
        self.list: GroupContentListRoute = self._create_route(GroupContentListRoute)
        self.search: GroupContentSearchRoute = self._create_route(GroupContentSearchRoute)


__all__ = ["ContentRouter"]
