from httpx import AsyncClient

from CriadexSDK.core.api.router import Router
from CriadexSDK.routers.auth.check import AuthCheckRoute
from CriadexSDK.routers.auth.create import AuthCreateRoute
from CriadexSDK.routers.auth.delete import AuthDeleteRoute
from CriadexSDK.routers.auth.reset import AuthResetRoute


class AuthRouter(Router):

    def __init__(self, api_base: str, http: AsyncClient):
        super().__init__(api_base, http)

        self.check: AuthCheckRoute = self._create_route(AuthCheckRoute)
        self.create: AuthCreateRoute = self._create_route(AuthCreateRoute)
        self.reset: AuthResetRoute = self._create_route(AuthResetRoute)
        self.delete: AuthDeleteRoute = self._create_route(AuthDeleteRoute)


__all__ = ["AuthRouter"]
