from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class GroupDeleteRoute(Route):
    class Response(BaseResponse):
        pass

    @outputs(Response)
    async def execute(self, group_name: str) -> Optional[dict]:
        return await self._delete(
            path=f"/groups/{group_name}/delete"
        )
