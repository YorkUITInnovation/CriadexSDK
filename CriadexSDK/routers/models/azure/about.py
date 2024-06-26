from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs
from CriadexSDK.routers.models.azure.create import AzureModelConfig


class ModelAboutRoute(Route):
    class Response(BaseResponse):
        model: Optional[AzureModelConfig]

    @outputs(Response)
    async def execute(self, model_id: int) -> Optional[dict]:
        return await self._get(
            path=f"/models/azure/{model_id}/about"
        )
