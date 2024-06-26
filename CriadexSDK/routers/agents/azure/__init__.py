from httpx import AsyncClient

from CriadexSDK.core.api.router import Router
from .chat import AgentChatRoute
from .intents import AgentIntentsRoute
from .lang import AgentLanguageRoute
from .transform import AgentTransformRoute


class AzureAgentsRouter(Router):

    def __init__(self, api_base: str, http: AsyncClient):
        super().__init__(api_base, http)

        self.chat: AgentChatRoute = self._create_route(AgentChatRoute)
        self.intents: AgentIntentsRoute = self._create_route(AgentIntentsRoute)
        self.language: AgentLanguageRoute = self._create_route(AgentLanguageRoute)
        self.transform: AgentTransformRoute = self._create_route(AgentTransformRoute)


__all__ = ["AzureAgentsRouter"]
