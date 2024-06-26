import json
from typing import Optional, Callable

from pydantic import BaseModel

from CriadexSDK.core.api.route import Route, BaseResponse, outputs


class ContentUploadConfig(BaseModel):
    file_name: str
    file_contents: dict
    file_metadata: dict


class GroupContentUploadRoute(Route):
    ENDPOINT: str = "upload"
    METHOD: str = "_post"

    class Response(BaseResponse):
        token_usage: Optional[int]

    @outputs(Response)
    async def execute(
            self,
            group_name: str,
            file: ContentUploadConfig,
    ) -> Optional[dict]:
        http_method: Callable = getattr(self, getattr(self, 'METHOD'))  # Do it this way for inheritance
        endpoint: str = getattr(self, 'ENDPOINT')

        return await http_method(
            path=f"/groups/{group_name}/content/{endpoint}",
            json=file
        )
