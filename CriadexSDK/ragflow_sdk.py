"""
RAGFlowSDK: Drop-in replacement for CriadexSDK, targeting RAGFlow API endpoints.
Scaffolded for migration. Implement methods to match CriadexSDK interface.
"""

from typing import Optional
from httpx import Client, AsyncClient


# --- Router Stubs ---
class ContentRouter:
    def __init__(self, api_base, httpx_client):
        self._api_base = api_base
        self._httpx = httpx_client
    
    async def upload(self, group_name, file):
        # POST /groups/{group_name}/content/upload
        url = f"{self._api_base}/groups/{group_name}/content/upload"
        resp = await self._httpx.post(url, json=file)
        resp.raise_for_status()
        return resp.json()
    
    async def search(self, group_name, search_config):
        # POST /groups/{group_name}/query
        url = f"{self._api_base}/groups/{group_name}/query"
        resp = await self._httpx.post(url, json=search_config)
        resp.raise_for_status()
        return resp.json()
    
    async def update(self, group_name, file):
        # PATCH /groups/{group_name}/content/update
        url = f"{self._api_base}/groups/{group_name}/content/update"
        resp = await self._httpx.patch(url, json=file)
        resp.raise_for_status()
        return resp.json()
    
    async def delete(self, group_name, document_name):
        # DELETE /groups/{group_name}/content/delete?document_name={document_name}
        url = f"{self._api_base}/groups/{group_name}/content/delete?document_name={document_name}"
        resp = await self._httpx.delete(url)
        resp.raise_for_status()
        return resp.json()
    
    async def list(self, group_name):
        # GET /groups/{group_name}/content/list
        url = f"{self._api_base}/groups/{group_name}/content/list"
        resp = await self._httpx.get(url)
        resp.raise_for_status()
        return resp.json()

class GroupsRouter:
    def __init__(self, api_base, httpx_client):
        self._api_base = api_base
        self._httpx = httpx_client
    
    async def create(self, group_name, group_config):
        # POST /groups/{group_name}/create
        url = f"{self._api_base}/groups/{group_name}/create"
        dump = group_config.model_dump() if hasattr(group_config, 'model_dump') else group_config
        resp = await self._httpx.post(url, json=dump)
        resp.raise_for_status()
        return resp.json()
    
    async def delete(self, group_name):
        # DELETE /groups/{group_name}/delete
        url = f"{self._api_base}/groups/{group_name}/delete"
        resp = await self._httpx.delete(url)
        resp.raise_for_status()
        return resp.json()
    
    async def about(self, group_name):
        # GET /groups/{group_name}/about
        url = f"{self._api_base}/groups/{group_name}/about"
        resp = await self._httpx.get(url)
        resp.raise_for_status()
        return resp.json()

class AuthRouter:
    def __init__(self, api_base, httpx_client):
        self._api_base = api_base
        self._httpx = httpx_client

    async def create(self, api_key, create_config):
        # POST /auth/{api_key}/create
        url = f"{self._api_base}/auth/{api_key}/create"
        dump = create_config.model_dump() if hasattr(create_config, 'model_dump') else create_config
        resp = await self._httpx.post(url, json=dump)
        resp.raise_for_status()
        return resp.json()

    async def delete(self, api_key):
        # DELETE /auth/keys/{api_key}
        url = f"{self._api_base}/auth/keys/{api_key}"
        resp = await self._httpx.delete(url)
        resp.raise_for_status()
        return resp.json()

    async def check(self, api_key):
        # GET /auth/keys/{api_key}
        url = f"{self._api_base}/auth/keys/{api_key}"
        resp = await self._httpx.get(url)
        resp.raise_for_status()
        return resp.json()

    async def reset(self, api_key, new_key):
        # PATCH /auth/keys/{api_key} (example, adjust as needed)
        url = f"{self._api_base}/auth/keys/{api_key}"
        data = {"new_key": new_key}
        resp = await self._httpx.patch(url, json=data)
        resp.raise_for_status()
        return resp.json()

class GroupAuthRouter:
    def __init__(self, api_base, httpx_client):
        self._api_base = api_base
        self._httpx = httpx_client
    
    async def create(self, group_name, api_key):
        # POST /group_auth/{group_name}/create
        url = f"{self._api_base}/group_auth/{group_name}/create"
        params = {"api_key": api_key}
        resp = await self._httpx.post(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    async def check(self, group_name, api_key):
        # GET /group_auth/{group_name}/check?api_key={api_key}
        url = f"{self._api_base}/group_auth/{group_name}/check"
        resp = await self._httpx.get(url, params={"api_key": api_key})
        resp.raise_for_status()
        return resp.json()
    
    async def delete(self, group_name, api_key):
        # DELETE /group_auth/{group_name}/delete?api_key={api_key}
        url = f"{self._api_base}/group_auth/{group_name}/delete"
        resp = await self._httpx.delete(url, params={"api_key": api_key})
        resp.raise_for_status()
        return resp.json()
    
    async def list(self, api_key):
        # GET /auth/keys/{api_key}/groups
        url = f"{self._api_base}/auth/keys/{api_key}/groups"
        resp = await self._httpx.get(url)
        resp.raise_for_status()
        return resp.json()

class ModelsRouter:
    def __init__(self, api_base, httpx_client):
        self._api_base = api_base
        self._httpx = httpx_client

    async def create(self, model_id, model_config):
        # POST /models
        url = f"{self._api_base}/models"
        data = {"model_id": model_id, **model_config}
        resp = await self._httpx.post(url, json=data)
        resp.raise_for_status()
        return resp.json()

    async def delete(self, model_id):
        # DELETE /models/{model_id}
        url = f"{self._api_base}/models/{model_id}"
        resp = await self._httpx.delete(url)
        resp.raise_for_status()
        return resp.json()

    async def about(self, model_id):
        # GET /models/{model_id}
        url = f"{self._api_base}/models/{model_id}"
        resp = await self._httpx.get(url)
        resp.raise_for_status()
        return resp.json()

    async def update(self, model_id, model_config):
        # PATCH /models/{model_id}
        url = f"{self._api_base}/models/{model_id}"
        resp = await self._httpx.patch(url, json=model_config)
        resp.raise_for_status()
        return resp.json()

class AgentsRouter:
    class Azure:
        def __init__(self, api_base, httpx_client):
            self._api_base = api_base
            self._httpx = httpx_client

        async def chat(self, model_id, agent_config):
            # POST /models/{model_id}/chat
            url = f"{self._api_base}/models/ragflow/{model_id}/agents/chat"
            resp = await self._httpx.post(url, json=agent_config)
            resp.raise_for_status()
            return resp.json()

        async def related_prompts(self, model_id, agent_config):
            # POST /models/{model_id}/related_prompts
            url = f"{self._api_base}/models/{model_id}/related_prompts"
            resp = await self._httpx.post(url, json=agent_config)
            resp.raise_for_status()
            return resp.json()

        async def transform(self, model_id, agent_config):
            # POST /models/{model_id}/transform
            url = f"{self._api_base}/models/{model_id}/transform"
            resp = await self._httpx.post(url, json=agent_config)
            resp.raise_for_status()
            return resp.json()

        async def intents(self, model_id, agent_config):
            # POST /models/{model_id}/intents
            url = f"{self._api_base}/models/{model_id}/intents"
            resp = await self._httpx.post(url, json=agent_config)
            resp.raise_for_status()
            return resp.json()

        async def language(self, model_id, agent_config):
            # POST /models/{model_id}/language
            url = f"{self._api_base}/models/{model_id}/language"
            resp = await self._httpx.post(url, json=agent_config)
            resp.raise_for_status()
            return resp.json()

    class Cohere:
        def __init__(self, api_base, httpx_client):
            self._api_base = api_base
            self._httpx = httpx_client

        async def rerank(self, model_id, agent_config):
            # POST /models/{model_id}/rerank
            url = f"{self._api_base}/models/{model_id}/rerank"
            cfg = agent_config.model_dump(mode='json') if hasattr(agent_config, 'model_dump') else dict(agent_config)
            # Map legacy fields to RAGFlow expected schema
            payload = {}
            # query
            payload["query"] = cfg.get("query") or cfg.get("prompt")
            # documents
            if "documents" in cfg:
                payload["documents"] = cfg["documents"]
            else:
                payload["documents"] = cfg.get("nodes", [])
            # pass-through optional params if present
            for key in ("top_n", "min_n"):
                if key in cfg:
                    payload[key] = cfg[key]

            resp = await self._httpx.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()

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

    def authenticate(self, api_key: str) -> None:
        # Set the API key header for all requests
        self._httpx.headers["x-api-key"] = api_key