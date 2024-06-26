from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class GroupAuthCheckRoute(Route):
    class Response(BaseResponse):
        authorized: Optional[bool]
        master: Optional[bool]

    @outputs(Response)
    async def execute(self, group_name: str, api_key: str) -> Optional[dict]:
        return await self._get(
            path=f"/group_auth/{group_name}/check",
            params={"group_name": group_name, "api_key": api_key}
        )
