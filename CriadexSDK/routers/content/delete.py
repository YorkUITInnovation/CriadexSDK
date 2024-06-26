from typing import Optional

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class GroupContentDeleteRoute(Route):
    class Response(BaseResponse):
        pass

    @outputs(Response)
    async def execute(self, group_name: str, document_name: str) -> Optional[dict]:
        return await self._delete(
            path=f"/groups/{group_name}/content/delete",
            params={"document_name": document_name}
        )
