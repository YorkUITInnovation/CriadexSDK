from httpx import AsyncClient

from CriadexSDK.core.api.router import Router
from CriadexSDK.routers.agents.azure import AzureAgentsRouter
from CriadexSDK.routers.agents.azure.chat import AgentChatRoute
from CriadexSDK.routers.agents.azure.intents import AgentIntentsRoute
from CriadexSDK.routers.agents.azure.lang import AgentLanguageRoute
from CriadexSDK.routers.agents.cohere import CohereAgentsRouter
from CriadexSDK.routers.agents.cohere.rerank import AgentRerankRoute


class AgentsRouter(Router):

    def __init__(self, api_base: str, http: AsyncClient):
        super().__init__(api_base, http)

        self.azure: AzureAgentsRouter = AzureAgentsRouter(api_base, http)
        self.cohere: CohereAgentsRouter = CohereAgentsRouter(api_base, http)


__all__ = ["AgentsRouter"]
