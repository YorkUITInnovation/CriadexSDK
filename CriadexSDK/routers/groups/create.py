from typing import Optional, Literal, Type

from pydantic import BaseModel

from CriadexSDK.core.api.route import Route, BaseResponse, outputs

IndexTypes: Type = Literal["DOCUMENT", "QUESTION", "CACHE"]


class PartialGroupConfig(BaseModel):
    type: IndexTypes
    llm_model_id: int
    embedding_model_id: int
    rerank_model_id: int


class GroupConfig(PartialGroupConfig):
    name: str


class GroupCreateRoute(Route):
    class Response(BaseResponse):
        config: Optional[GroupConfig]

    @outputs(Response)
    async def execute(self, group_name: str, group_config: PartialGroupConfig) -> Optional[dict]:
        return await self._post(
            path=f"/groups/{group_name}/create",
            json=group_config
        )
