from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs
from CriadexSDK.routers.groups.create import GroupConfig


class GroupInfo(GroupConfig):
    id: int
    created: str


class GroupAboutRoute(Route):
    class Response(BaseResponse):
        info: Optional[GroupInfo]

    @outputs(Response)
    async def execute(self, group_name: str) -> Optional[dict]:
        return await self._get(
            path=f"/groups/{group_name}/about"
        )
