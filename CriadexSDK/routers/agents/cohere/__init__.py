from httpx import AsyncClient

from CriadexSDK.core.api.router import Router
from .rerank import AgentRerankRoute


class CohereAgentsRouter(Router):

    def __init__(self, api_base: str, http: AsyncClient):
        super().__init__(api_base, http)

        self.rerank: AgentRerankRoute = self._create_route(AgentRerankRoute)


__all__ = ["CohereAgentsRouter"]
