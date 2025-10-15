"""
RAGFlowSDK: Drop-in replacement for CriadexSDK, targeting RAGFlow API endpoints.
Scaffolded for migration. Implement methods to match CriadexSDK interface.
"""

from typing import Optional
from httpx import AsyncClient


# --- Router Stubs ---
class ContentRouter:
    def __init__(self, api_base, httpx_client):
        self._api_base = api_base
        self._httpx = httpx_client

    async def upload(self, group_name, file):
        # POST /knowledge_bases/{group_name}/documents
        url = f"{self._api_base}/knowledge_bases/{group_name}/documents"
        resp = await self._httpx.post(url, json=file)
        await resp.raise_for_status()
        return await resp.json()

    async def search(self, group_name, search_config):
        # POST /knowledge_bases/{group_name}/query
        url = f"{self._api_base}/knowledge_bases/{group_name}/query"
        resp = await self._httpx.post(url, json=search_config)
        await resp.raise_for_status()
        return await resp.json()

    async def update(self, group_name, file):
        # PATCH /knowledge_bases/{group_name}/documents
        url = f"{self._api_base}/knowledge_bases/{group_name}/documents"
        resp = await self._httpx.patch(url, json=file)
        await resp.raise_for_status()
        return await resp.json()

    async def delete(self, group_name, document_name):
        # DELETE /knowledge_bases/{group_name}/documents/{document_name}
        url = f"{self._api_base}/knowledge_bases/{group_name}/documents/{document_name}"
        resp = await self._httpx.delete(url)
        await resp.raise_for_status()
        return await resp.json()

    async def list(self, group_name):
        # GET /knowledge_bases/{group_name}/documents
        url = f"{self._api_base}/knowledge_bases/{group_name}/documents"
        resp = await self._httpx.get(url)
        await resp.raise_for_status()
        return await resp.json()

class GroupsRouter:
    def __init__(self, api_base, httpx_client):
        self._api_base = api_base
        self._httpx = httpx_client

    async def create(self, group_name, group_config):
        # POST /groups/{group_name}/create
        url = f"{self._api_base}/groups/{group_name}/create"
        dump = group_config.model_dump() if hasattr(group_config, 'model_dump') else group_config
        resp = await self._httpx.post(url, json=dump)
        await resp.raise_for_status()
        return await resp.json()

    async def delete(self, group_name):
        # DELETE /groups/{group_name}/delete
        url = f"{self._api_base}/groups/{group_name}/delete"
        resp = await self._httpx.delete(url)
        await resp.raise_for_status()
        return await resp.json()

    async def about(self, group_name):
        # GET /knowledge_bases/{group_name}
        url = f"{self._api_base}/knowledge_bases/{group_name}"
        resp = await self._httpx.get(url)
        await resp.raise_for_status()
        return await resp.json()

class AuthRouter:
    def __init__(self, api_base, httpx_client):
        self._api_base = api_base
        self._httpx = httpx_client

    async def create(self, api_key, create_config):
        # POST /auth/{api_key}/create
        url = f"{self._api_base}/auth/{api_key}/create"
        dump = create_config.model_dump() if hasattr(create_config, 'model_dump') else create_config
        resp = await self._httpx.post(url, json=dump)
        await resp.raise_for_status()
        return await resp.json()

    async def delete(self, api_key):
        # DELETE /auth/keys/{api_key}
        url = f"{self._api_base}/auth/keys/{api_key}"
        resp = await self._httpx.delete(url)
        await resp.raise_for_status()
        return await resp.json()

    async def check(self, api_key):
        # GET /auth/keys/{api_key}
        url = f"{self._api_base}/auth/keys/{api_key}"
        resp = await self._httpx.get(url)
        await resp.raise_for_status()
        return await resp.json()

    async def reset(self, api_key, new_key):
        # PATCH /auth/keys/{api_key} (example, adjust as needed)
        url = f"{self._api_base}/auth/keys/{api_key}"
        data = {"new_key": new_key}
        resp = await self._httpx.patch(url, json=data)
        await resp.raise_for_status()
        return await resp.json()

class GroupAuthRouter:
    def __init__(self, api_base, httpx_client):
        self._api_base = api_base
        self._httpx = httpx_client

    async def create(self, group_name, api_key):
        # POST /group_auth/{group_name}/create
        url = f"{self._api_base}/group_auth/{group_name}/create"
        params = {"api_key": api_key}
        resp = await self._httpx.post(url, params=params)
        await resp.raise_for_status()
        return await resp.json()

    async def check(self, group_name, api_key):
        # GET /knowledge_bases/{group_name}/auth/{api_key}
        url = f"{self._api_base}/knowledge_bases/{group_name}/auth/{api_key}"
        resp = await self._httpx.get(url)
        await resp.raise_for_status()
        return await resp.json()

    async def delete(self, group_name, api_key):
        # DELETE /knowledge_bases/{group_name}/auth/{api_key}
        url = f"{self._api_base}/knowledge_bases/{group_name}/auth/{api_key}"
        resp = await self._httpx.delete(url)
        await resp.raise_for_status()
        return await resp.json()

    async def list(self, api_key):
        # GET /auth/keys/{api_key}/knowledge_bases
        url = f"{self._api_base}/auth/keys/{api_key}/knowledge_bases"
        resp = await self._httpx.get(url)
        await resp.raise_for_status()
        return await resp.json()

class ModelsRouter:
    def __init__(self, api_base, httpx_client):
        self._api_base = api_base
        self._httpx = httpx_client

    async def create(self, model_id, model_config):
        # POST /models
        url = f"{self._api_base}/models"
        data = {"model_id": model_id, **model_config}
        resp = await self._httpx.post(url, json=data)
        await resp.raise_for_status()
        return await resp.json()

    async def delete(self, model_id):
        # DELETE /models/{model_id}
        url = f"{self._api_base}/models/{model_id}"
        resp = await self._httpx.delete(url)
        await resp.raise_for_status()
        return await resp.json()

    async def about(self, model_id):
        # GET /models/{model_id}
        url = f"{self._api_base}/models/{model_id}"
        resp = await self._httpx.get(url)
        await resp.raise_for_status()
        return await resp.json()

    async def update(self, model_id, model_config):
        # PATCH /models/{model_id}
        url = f"{self._api_base}/models/{model_id}"
        resp = await self._httpx.patch(url, json=model_config)
        await resp.raise_for_status()
        return await resp.json()

class AgentsRouter:
    class Azure:
        def __init__(self, api_base, httpx_client):
            self._api_base = api_base
            self._httpx = httpx_client

        async def chat(self, model_id, agent_config):
            # POST /models/{model_id}/chat
            url = f"{self._api_base}/models/{model_id}/chat"
            resp = await self._httpx.post(url, json=agent_config)
            await resp.raise_for_status()
            return await resp.json()

        async def related_prompts(self, model_id, agent_config):
            # POST /models/{model_id}/related_prompts
            url = f"{self._api_base}/models/{model_id}/related_prompts"
            resp = await self._httpx.post(url, json=agent_config)
            await resp.raise_for_status()
            return await resp.json()

        async def transform(self, model_id, agent_config):
            # POST /models/{model_id}/transform
            url = f"{self._api_base}/models/{model_id}/transform"
            resp = await self._httpx.post(url, json=agent_config)
            await resp.raise_for_status()
            return await resp.json()

        async def intents(self, model_id, agent_config):
            # POST /models/{model_id}/intents
            url = f"{self._api_base}/models/{model_id}/intents"
            resp = await self._httpx.post(url, json=agent_config)
            await resp.raise_for_status()
            return await resp.json()

        async def language(self, model_id, agent_config):
            # POST /models/{model_id}/language
            url = f"{self._api_base}/models/{model_id}/language"
            resp = await self._httpx.post(url, json=agent_config)
            await resp.raise_for_status()
            return await resp.json()

    class Cohere:
        def __init__(self, api_base, httpx_client):
            self._api_base = api_base
            self._httpx = httpx_client

        async def rerank(self, model_id, agent_config):
            # POST /models/{model_id}/rerank
            url = f"{self._api_base}/models/{model_id}/rerank"
            resp = await self._httpx.post(url, json=agent_config)
            await resp.raise_for_status()
            return await resp.json()

    def __init__(self, api_base, httpx_client):
        self.azure = AgentsRouter.Azure(api_base, httpx_client)
        self.cohere = AgentsRouter.Cohere(api_base, httpx_client)


class RAGFlowSDK:
    def __init__(self, api_base: str, error_stacktrace: bool = True):
        self._api_base = api_base[:-1] if api_base.endswith("/") else api_base
        self._error_stacktrace = error_stacktrace
        self._httpx = AsyncClient()
        self.content = ContentRouter(self._api_base, self._httpx)
        self.manage = GroupsRouter(self._api_base, self._httpx)
        self.auth = AuthRouter(self._api_base, self._httpx)
        self.group_auth = GroupAuthRouter(self._api_base, self._httpx)
        self.models = ModelsRouter(self._api_base, self._httpx)
        self.agents = AgentsRouter(self._api_base, self._httpx)

    async def authenticate(self, api_key: str) -> None:
        # Set the API key header for all requests
        self._httpx.headers["x-api-key"] = api_key
