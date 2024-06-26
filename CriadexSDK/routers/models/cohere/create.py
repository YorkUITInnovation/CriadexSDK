from typing import Optional

from pydantic import BaseModel

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class CohereModelPartialBaseConfig(BaseModel):
    api_key: str = "your-api-key"


class CohereModelBaseConfig(CohereModelPartialBaseConfig):
    api_model: str = "rerank-multilingual-v2.0"


class CohereModelConfig(CohereModelBaseConfig):
    id: int


class ModelCreateRoute(Route):
    class Response(BaseResponse):
        model: Optional[CohereModelConfig]

    @outputs(Response)
    async def execute(self, model_id: int, model_config: CohereModelBaseConfig) -> Optional[dict]:
        return await self._post(
            path=f"/models/cohere/create",
            json=model_config
        )
