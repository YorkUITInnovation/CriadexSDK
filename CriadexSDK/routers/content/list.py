from typing import Optional, List

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class GroupContentListRoute(Route):
    class Response(BaseResponse):
        files: List[str]

    @outputs(Response)
    async def execute(self, group_name: str) -> Optional[dict]:
        return await self._get(
            path=f"/groups/{group_name}/content/list"
        )
