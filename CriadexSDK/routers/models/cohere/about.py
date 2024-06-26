from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs
from CriadexSDK.routers.models.cohere.create import CohereModelConfig


class ModelAboutRoute(Route):
    class Response(BaseResponse):
        model: Optional[CohereModelConfig]

    @outputs(Response)
    async def execute(self, model_id: int) -> Optional[dict]:
        return await self._get(
            path=f"/models/cohere/{model_id}/about"
        )
