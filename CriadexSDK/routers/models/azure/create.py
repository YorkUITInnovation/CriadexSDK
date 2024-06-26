from typing import Optional

from pydantic import BaseModel

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class AzureModelPartialBaseConfig(BaseModel):
    api_resource: str = "your-resource"
    api_version: str = "2023-05-15"
    api_key: str = "your-controllers-key"
    api_deployment: str = "your-deployment-name"


class AzureModelBaseConfig(AzureModelPartialBaseConfig):
    api_model: str = "text-embedding-ada-002"


class AzureModelConfig(AzureModelBaseConfig):
    id: int


class ModelCreateRoute(Route):
    class Response(BaseResponse):
        model: Optional[AzureModelConfig]

    @outputs(Response)
    async def execute(self, model_id: int, model_config: AzureModelBaseConfig) -> Optional[dict]:
        return await self._post(
            path=f"/models/azure/create",
            json=model_config
        )
