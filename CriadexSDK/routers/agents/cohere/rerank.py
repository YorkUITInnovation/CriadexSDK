from typing import Optional, List

from pydantic import Field

from CriadexSDK.core.api.route import Route, BaseResponse, outputs
from CriadexSDK.routers.agents.azure.chat import QueryModelParameters, BaseAgentResponse
from CriadexSDK.routers.content.search import TextNodeWithScore


class RerankAgentResponse(BaseAgentResponse):
    ranked_nodes: List[TextNodeWithScore] = []
    search_units: int


class RerankAgentConfig(QueryModelParameters):
    prompt: str

    top_n: Optional[int] = Field(default=None, ge=1)
    min_n: float = Field(default=0.0, ge=0.0, le=1.0)

    nodes: List[TextNodeWithScore]


class AgentRerankRoute(Route):
    class Response(BaseResponse):
        agent_response: Optional[RerankAgentResponse]

    @outputs(Response)
    async def execute(
            self,
            model_id: int,
            agent_config: RerankAgentConfig
    ) -> Optional[dict]:
        return await self._post(
            path=f"/models/cohere/{model_id}/agents/rerank",
            json=agent_config
        )

