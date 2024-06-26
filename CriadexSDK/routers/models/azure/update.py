from typing import Optional

from CriadexSDK.core.api.route import Route, outputs
from CriadexSDK.routers.models.azure.create import AzureModelPartialBaseConfig, ModelCreateRoute


class ModelUpdateRoute(Route):

    @outputs(ModelCreateRoute.Response)
    async def execute(self, model_id: int, model_config: AzureModelPartialBaseConfig) -> Optional[dict]:
        return await self._patch(
            path=f"/models/azure/{model_id}/update",
            json=model_config
        )
