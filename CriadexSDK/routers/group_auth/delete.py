from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class GroupAuthDeleteRoute(Route):
    class Response(BaseResponse):
        pass

    @outputs(Response)
    async def execute(self, group_name: str, api_key: str) -> Optional[dict]:
        return await self._delete(
            path=f"/group_auth/{group_name}/delete",
            params={"group_name": group_name, "api_key": api_key}
        )
