from typing import Optional, List

from CriadexSDK.core.api.route import Route, BaseResponse, outputs
from CriadexSDK.routers.agents.azure.chat import LLMAgentResponse, QueryModelParameters, ChatMessage


class TransformAgentResponse(LLMAgentResponse):
    new_prompt: Optional[str] = None


class TransformAgentConfig(QueryModelParameters):
    prompt: str
    history: List[ChatMessage]


class AgentTransformRoute(Route):
    class Response(BaseResponse):
        agent_response: Optional[TransformAgentResponse]

    @outputs(Response)
    async def execute(
            self,
            model_id: int,
            agent_config: TransformAgentConfig
    ) -> Optional[dict]:
        return await self._post(
            path=f"/models/azure/{model_id}/agents/transform",
            json=agent_config
        )
