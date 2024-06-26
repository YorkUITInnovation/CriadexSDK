from typing import Optional

from pydantic import BaseModel

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class AuthCreateConfig(BaseModel):
    master: bool


class AuthCreateRoute(Route):
    class Response(BaseResponse):
        api_key: Optional[str]
        master: Optional[bool]

    @outputs(Response)
    async def execute(self, api_key: str, create_config: AuthCreateConfig) -> Optional[dict]:
        return await self._post(
            path=f"/auth/{api_key}/create",
            json=create_config
        )
