from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class AuthDeleteRoute(Route):
    class Response(BaseResponse):
        api_key: Optional[str]

    @outputs(Response)
    async def execute(self, api_key: str) -> Optional[dict]:
        return await self._delete(
            path=f"/auth/{api_key}/delete",
        )
