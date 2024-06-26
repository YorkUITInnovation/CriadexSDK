from typing import Optional

from pydantic import BaseModel

from CriadexSDK.core.api.route import Route, BaseResponse, outputs
from CriadexSDK.routers.agents.azure.chat import BaseAgentResponse


class LanguageAgentResponse(BaseAgentResponse):
    language: Optional[str]


class LanguageAgentConfig(BaseModel):
    prompt: str


class AgentLanguageRoute(Route):
    class Response(BaseResponse):
        agent_response: Optional[LanguageAgentResponse]

    @outputs(Response)
    async def execute(
            self,
            model_id: int,
            agent_config: LanguageAgentConfig
    ) -> Optional[dict]:
        return await self._post(
            path=f"/models/azure/{model_id}/agents/language",
            json=agent_config
        )
