from typing import List, Optional, Literal, Any

from pydantic import BaseModel

from CriadexSDK.core.api.route import Route, BaseResponse, outputs
from CriadexSDK.routers.content.search import CompletionUsage


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    additional_kwargs: dict = dict()
    metadata: dict = dict()


class ChatMessageRaw(BaseModel):
    id: str
    choices: List[dict]
    created: int
    model: str
    object: str
    system_fingerprint: Any
    usage: CompletionUsage


class ChatResponse(BaseModel):
    message: ChatMessage
    raw: ChatMessageRaw


class QueryModelParameters(BaseModel):
    max_reply_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None


class ChatAgentConfig(QueryModelParameters):
    history: List[ChatMessage]


class BaseAgentResponse(BaseModel):
    message: Optional[str] = None


class LLMAgentResponse(BaseAgentResponse):
    usage: List[CompletionUsage]


class ChatAgentResponse(LLMAgentResponse):
    chat_response: ChatResponse


class AgentChatRoute(Route):
    class Response(BaseResponse):
        agent_response: Optional[ChatAgentResponse]

    @outputs(Response)
    async def execute(
            self,
            model_id: int,
            agent_config: ChatAgentConfig
    ) -> Optional[dict]:
        return await self._post(
            path=f"/models/azure/{model_id}/agents/chat",
            json=agent_config
        )
