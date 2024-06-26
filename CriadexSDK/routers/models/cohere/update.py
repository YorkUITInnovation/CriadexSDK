from typing import Optional

from CriadexSDK.core.api.route import Route, outputs
from CriadexSDK.routers.models.azure.create import ModelCreateRoute
from CriadexSDK.routers.models.cohere.create import CohereModelPartialBaseConfig


class ModelUpdateRoute(Route):

    @outputs(ModelCreateRoute.Response)
    async def execute(self, model_id: int, model_config: CohereModelPartialBaseConfig) -> Optional[dict]:
        return await self._patch(
            path=f"/models/cohere/{model_id}/update",
            json=model_config
        )
