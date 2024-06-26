from httpx import AsyncClient

from .azure import AzureModelsRouter
from .cohere import CohereModelsRouter
from ...core.api.router import Router


class ModelsRouter(Router):

    def __init__(self, api_base: str, http: AsyncClient):
        super().__init__(api_base, http)

        self.azure: AzureModelsRouter = AzureModelsRouter(api_base, http)
        self.cohere: CohereModelsRouter = CohereModelsRouter(api_base, http)


__all__ = ["ModelsRouter"]
