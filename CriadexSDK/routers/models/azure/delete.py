from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class ModelDeleteRoute(Route):
    class Response(BaseResponse):
        pass

    @outputs(Response)
    async def execute(self, model_id: int) -> Optional[dict]:
        return await self._delete(
            path=f"/models/azure/{model_id}/delete"
        )
