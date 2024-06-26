from typing import Type, TypeVar

from httpx import AsyncClient

from CriadexSDK.core.api.route import Route

T = TypeVar('T', bound=Route)


class Router:

    def __init__(
            self,
            api_base: str,
            http: AsyncClient
    ):
        self._api_base: str = api_base
        self._http: AsyncClient = http

    def _create_route(self, route: Type[T]) -> T:
        return route(api_base=self._api_base, http=self._http)
