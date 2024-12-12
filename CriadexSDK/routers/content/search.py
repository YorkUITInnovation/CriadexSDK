from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


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


class Asset(BaseModel):
    id: int
    uuid: str
    document_id: int
    group_id: int
    mimetype: str
    data: str
    created: datetime


class TextNode(BaseNode):
    text: str
    text_template: str
    metadata_template: str


class NodeWithScore(BaseModel):
    node: BaseNode
    score: float


class TextNodeWithScore(NodeWithScore):
    node: TextNode


class GroupSearchResponse(BaseModel):
    nodes: List[TextNodeWithScore]
    assets: List[Asset]
    search_units: Optional[int] = None
    metadata: dict = {}


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


class GroupContentSearchRoute(Route):
    class Response(BaseResponse):
        response: Optional[GroupSearchResponse]
        group_name: str

    @outputs(Response)
    async def execute(self, group_name: str, search_config: SearchGroupConfig) -> Optional[dict]:
        response: dict = await self._post(
            path=f"/groups/{group_name}/content/search",
            json=search_config
        )

        return {"group_name": group_name, **response}
