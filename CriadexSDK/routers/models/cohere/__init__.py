from httpx import AsyncClient

from CriadexSDK.core.api.router import Router
from .about import ModelAboutRoute
from .create import ModelCreateRoute
from .delete import ModelDeleteRoute
from .update import ModelUpdateRoute


class CohereModelsRouter(Router):

    def __init__(self, api_base: str, http: AsyncClient):
        super().__init__(api_base, http)

        self.delete: ModelDeleteRoute = self._create_route(ModelDeleteRoute)
        self.create: ModelCreateRoute = self._create_route(ModelCreateRoute)
        self.about: ModelAboutRoute = self._create_route(ModelAboutRoute)
        self.update: ModelUpdateRoute = self._create_route(ModelUpdateRoute)
