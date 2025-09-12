
from typing import Optional, List, Dict, Any, Union, Literal
from pydantic import BaseModel, Field, AnyUrl, FilePath

# --- Auth Schemas ---
class AuthCreateConfig(BaseModel):
    master: bool = False

class AuthCreateResponse(BaseModel):
    api_key: str
    master: Optional[bool] = False

class AuthCheckResponse(BaseModel):
    api_key: Optional[str]
    master: Optional[bool]
    authorized: Optional[bool]

class AuthDeleteResponse(BaseModel):
    api_key: Optional[str]

class AuthResetResponse(BaseModel):
    new_key: Optional[str]

# --- Group Schemas ---
class GroupCreateConfig(BaseModel):
    type: str
    llm_model_id: int
    embedding_model_id: int
    rerank_model_id: int

class GroupCreateResponse(BaseModel):
    name: str
    type: str
    llm_model_id: int
    embedding_model_id: int
    rerank_model_id: int
    id: Optional[int]
    created: Optional[str]

class GroupInfo(GroupCreateConfig):
    id: int
    created: str

class GroupAboutResponse(BaseModel):
    info: Optional[GroupInfo]

class GroupDeleteResponse(BaseModel):
    pass

# --- Content Schemas ---
class ContentUploadConfig(BaseModel):
    file_name: str
    file_contents: dict
    file_metadata: dict

class ContentUploadResponse(BaseModel):
    token_usage: Optional[int]

class Filter(BaseModel):
    should: Optional[List[dict]] = None
    must: Optional[List[dict]] = None
    must_not: Optional[List[dict]] = None

class SearchGroupConfig(BaseModel):
    prompt: str
    top_k: Optional[int] = Field(default=None, ge=1, le=1000)
    min_k: float = Field(default=0.0, ge=0.0, le=1.0)
    top_n: Optional[int] = Field(default=None, ge=1)
    min_n: float = Field(default=0.0, ge=0.0, le=1.0)
    rerank_enabled: bool = True
    search_filter: Optional[Filter] = None
    extra_groups: Optional[List[str]] = None

class CompletionUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    usage_label: Optional[str] = None

class BaseNode(BaseModel):
    metadata: dict
    excluded_embed_metadata_keys: List[str] = []
    excluded_llm_metadata_keys: List[str] = []
    class_name: str

class TextNode(BaseNode):
    text: str
    text_template: str
    metadata_template: str

class NodeWithScore(BaseModel):
    node: BaseNode
    score: float

class TextNodeWithScore(NodeWithScore):
    node: TextNode

class Asset(BaseModel):
    id: int
    uuid: str
    document_id: int
    group_id: int
    mimetype: str
    data: str
    created: str
    description: str

class GroupSearchResponse(BaseModel):
    nodes: List[TextNodeWithScore]
    assets: List[Asset]
    search_units: Optional[int] = None
    metadata: dict = {}

class ContentListResponse(BaseModel):
    files: List[str]

class ContentDeleteResponse(BaseModel):
    pass

class ContentUpdateResponse(ContentUploadResponse):
    pass

# --- Group Auth Schemas ---
class GroupAuthCheckResponse(BaseModel):
    authorized: Optional[bool]
    master: Optional[bool]

class GroupAuthListResponse(BaseModel):
    indexes: List[GroupInfo]

# --- Agent/Model Schemas ---
class AzureModelPartialBaseConfig(BaseModel):
    api_resource: str = "your-resource"
    api_version: str = "2023-05-15"
    api_key: str = "your-controllers-key"
    api_deployment: str = "your-deployment-name"

class AzureModelBaseConfig(AzureModelPartialBaseConfig):
    api_model: str = "text-embedding-ada-002"

class AzureModelConfig(AzureModelBaseConfig):
    id: int

class CohereModelPartialBaseConfig(BaseModel):
    api_key: str = "your-api-key"

class CohereModelBaseConfig(CohereModelPartialBaseConfig):
    api_model: str = "rerank-multilingual-v2.0"

class CohereModelConfig(CohereModelBaseConfig):
    id: int

class ModelCreateResponse(BaseModel):
    model: Optional[Union[AzureModelConfig, CohereModelConfig]]

class ModelAboutResponse(ModelCreateResponse):
    pass

class ModelDeleteResponse(BaseModel):
    pass

# --- Agent Chat/Related/Transform/Rerank Schemas ---
class TextBlock(BaseModel):
    block_type: Literal["text"] = "text"
    text: str

class ImageBlock(BaseModel):
    block_type: Literal["image"] = "image"
    image: Optional[str] = None
    path: Optional[FilePath] = None
    url: Union[AnyUrl, str, None] = None
    image_mimetype: Optional[str] = None
    detail: Optional[str] = None

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    blocks: List[Union[TextBlock, ImageBlock]]
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

class AgentChatResponse(BaseModel):
    agent_response: Optional[ChatAgentResponse]

class RelatedPrompt(BaseModel):
    label: str
    prompt: str
    llm_generated: bool = False

class RelatedPromptsAgentResponse(LLMAgentResponse):
    related_prompts: List[RelatedPrompt]

class RelatedPromptsAgentConfig(QueryModelParameters):
    llm_prompt: str
    llm_reply: str

class AgentRelatedPromptsResponse(BaseModel):
    agent_response: Optional[RelatedPromptsAgentResponse]

class TransformAgentResponse(LLMAgentResponse):
    new_prompt: Optional[str] = None

class TransformAgentConfig(QueryModelParameters):
    prompt: str
    history: List[ChatMessage]

class AgentTransformResponse(BaseModel):
    agent_response: Optional[TransformAgentResponse]

class RerankAgentResponse(BaseAgentResponse):
    ranked_nodes: List[TextNodeWithScore] = []
    search_units: int

class RerankAgentConfig(QueryModelParameters):
    prompt: str
    top_n: Optional[int] = Field(default=None, ge=1)
    min_n: float = Field(default=0.0, ge=0.0, le=1.0)
    nodes: List[TextNodeWithScore]

class AgentRerankResponse(BaseModel):
    agent_response: Optional[RerankAgentResponse]
