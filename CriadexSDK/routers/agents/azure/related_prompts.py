from typing import List, Optional

from pydantic import BaseModel

from CriadexSDK.core.api.route import Route, BaseResponse, outputs
from .chat import QueryModelParameters, LLMAgentResponse


class RelatedPrompt(BaseModel):
    label: str
    prompt: str
    llm_generated: bool = False


class RelatedPromptsAgentResponse(LLMAgentResponse):
    related_prompts: List[RelatedPrompt]


class RelatedPromptsAgentConfig(QueryModelParameters):
    llm_prompt: str
    llm_reply: str


class AgentRelatedPromptsRoute(Route):
    class Response(BaseResponse):
        agent_response: Optional[RelatedPromptsAgentResponse]

    @outputs(Response)
    async def execute(
            self,
            model_id: int,
            agent_config: RelatedPromptsAgentConfig
    ) -> Optional[dict]:
        return await self._post(
            path=f"/models/azure/{model_id}/agents/intents",
            json=agent_config
        )
