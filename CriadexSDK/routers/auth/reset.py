from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class AuthResetRoute(Route):
    class Response(BaseResponse):
        new_key: Optional[str]

    @outputs(Response)
    async def execute(self, api_key: str, new_key: str) -> Optional[dict]:
        return await self._patch(
            path=f"/auth/{api_key}/reset",
            params={'new_key': new_key}
        )
