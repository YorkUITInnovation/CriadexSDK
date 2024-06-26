from typing import Optional, List

from CriadexSDK.core.api.route import Route, BaseResponse, outputs
from CriadexSDK.routers.groups.about import GroupInfo


class GroupAuthListRoute(Route):
    class Response(BaseResponse):
        indexes: List[GroupInfo]

    @outputs(Response)
    async def execute(self, api_key: str) -> Optional[dict]:
        return await self._get(
            path=f"/group_auth/list",
            params={"api_key": api_key}
        )
