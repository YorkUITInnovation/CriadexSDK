from typing import List, Optional, Literal, Any, Union

from pydantic import BaseModel, FilePath, AnyUrl

from CriadexSDK.core.api.route import Route, BaseResponse, outputs
from CriadexSDK.routers.content.search import CompletionUsage


class ImageBlock(BaseModel):
    block_type: Literal["image"] = "image"
    image: Optional[block_type] = None
    path: Optional[FilePath] = None
    url: Union[AnyUrl, str, None] = None
    image_mimetype: Optional[str] = None
    detail: Optional[str] = None


class TextBlock(BaseModel):
    block_type: Literal["text"] = "text"
    text: str


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    blocks: List[Union[TextBlock, ImageBlock]]
    additional_kwargs: dict = dict()
    metadata: dict = dict()

    @property
    def content(self) -> str:
        return " ".join([block.text for block in self.blocks if isinstance(block, TextBlock)])

    @classmethod
    def from_content(
            cls,
            content: str,
            **kwargs
    ) -> "ChatMessage":
        return cls(
            blocks=[TextBlock(text=content)],
            **kwargs
        )


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
