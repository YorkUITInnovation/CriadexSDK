from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class AuthCheckRoute(Route):
    class Response(BaseResponse):
        api_key: Optional[str]
        master: Optional[bool]
        authorized: Optional[bool]

    @outputs(Response)
    async def execute(self, api_key: str) -> Optional[dict]:
        return await self._get(
            path=f"/auth/{api_key}/check",
        )
