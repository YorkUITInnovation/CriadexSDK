"""
RAGFlowSDK: Drop-in replacement for CriadexSDK, targeting RAGFlow API endpoints.
Scaffolded for migration. Implement methods to match CriadexSDK interface.
"""

from typing import Optional, Any
import asyncio
import logging

from httpx import AsyncClient, Timeout, HTTPStatusError, RequestError


logger = logging.getLogger(__name__)


class CriadexSDKError(Exception):
    """Base exception for SDK errors."""


class CriadexNetworkError(CriadexSDKError):
    """Network/connection errors."""


class CriadexAPIError(CriadexSDKError):
    """API errors (4xx, 5xx)."""

    def __init__(self, status_code: int, message: str, response: Optional[dict] = None) -> None:
        self.status_code = status_code
        self.message = message
        self.response = response
        super().__init__(f"[{status_code}] {message}")


async def _request_with_retry(
    httpx_client: AsyncClient,
    method: str,
    url: str,
    *,
    max_retries: int,
    **kwargs: Any,
) -> dict:
    """
    Perform an HTTP request with basic retry logic and consistent error handling.
    """
    last_exception: Optional[BaseException] = None

    for attempt in range(max_retries):
        try:
            logger.debug("RAGFlowSDK request %s %s (attempt %d)", method, url, attempt + 1)
            resp = await httpx_client.request(method, url, **kwargs)
            resp.raise_for_status()
            logger.debug("RAGFlowSDK response %s %s -> %s", method, url, resp.status_code)
            return resp.json()
        except HTTPStatusError as exc:
            status = exc.response.status_code
            last_exception = exc

            # Do not retry 4xx client errors; surface them as API errors
            if 400 <= status < 500:
                raise CriadexAPIError(status_code=status, message=exc.response.text) from exc

            # Retry 5xx server errors with exponential backoff
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue

            raise CriadexAPIError(
                status_code=status,
                message=f"Server error after {max_retries} attempts",
            ) from exc
        except RequestError as exc:
            last_exception = exc
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            raise CriadexNetworkError(f"Network error after {max_retries} attempts: {exc}") from exc

    raise CriadexNetworkError(f"Request failed after {max_retries} attempts: {last_exception}")


# --- Routers ---
class ContentRouter:
    def __init__(self, api_base: str, httpx_client: AsyncClient, max_retries: int) -> None:
        self._api_base = api_base
        self._httpx = httpx_client
        self._max_retries = max_retries
    
    async def upload(self, group_name, file):
        # POST /groups/{group_name}/content/upload
        url = f"{self._api_base}/groups/{group_name}/content/upload"
        return await _request_with_retry(
            self._httpx,
            "POST",
            url,
            max_retries=self._max_retries,
            json=file,
        )
    
    async def search(self, group_name, search_config):
        # POST /groups/{group_name}/query
        url = f"{self._api_base}/groups/{group_name}/query"
        return await _request_with_retry(
            self._httpx,
            "POST",
            url,
            max_retries=self._max_retries,
            json=search_config,
        )
    
    async def update(self, group_name, file):
        # PATCH /groups/{group_name}/content/update
        url = f"{self._api_base}/groups/{group_name}/content/update"
        return await _request_with_retry(
            self._httpx,
            "PATCH",
            url,
            max_retries=self._max_retries,
            json=file,
        )
    
    async def delete(self, group_name, document_name):
        # DELETE /groups/{group_name}/content/delete?document_name={document_name}
        url = f"{self._api_base}/groups/{group_name}/content/delete"
        return await _request_with_retry(
            self._httpx,
            "DELETE",
            url,
            max_retries=self._max_retries,
            params={"document_name": document_name},
        )
    
    async def list(self, group_name):
        # GET /groups/{group_name}/content/list
        url = f"{self._api_base}/groups/{group_name}/content/list"
        return await _request_with_retry(
            self._httpx,
            "GET",
            url,
            max_retries=self._max_retries,
        )

class GroupsRouter:
    def __init__(self, api_base: str, httpx_client: AsyncClient, max_retries: int) -> None:
        self._api_base = api_base
        self._httpx = httpx_client
        self._max_retries = max_retries
    
    async def create(self, group_name, group_config):
        # POST /groups/{group_name}/create
        url = f"{self._api_base}/groups/{group_name}/create"
        dump = group_config.model_dump() if hasattr(group_config, 'model_dump') else group_config
        return await _request_with_retry(
            self._httpx,
            "POST",
            url,
            max_retries=self._max_retries,
            json=dump,
        )
    
    async def delete(self, group_name):
        # DELETE /groups/{group_name}/delete
        url = f"{self._api_base}/groups/{group_name}/delete"
        return await _request_with_retry(
            self._httpx,
            "DELETE",
            url,
            max_retries=self._max_retries,
        )
    
    async def about(self, group_name):
        # GET /groups/{group_name}/about
        url = f"{self._api_base}/groups/{group_name}/about"
        return await _request_with_retry(
            self._httpx,
            "GET",
            url,
            max_retries=self._max_retries,
        )

class AuthRouter:
    def __init__(self, api_base: str, httpx_client: AsyncClient, max_retries: int) -> None:
        self._api_base = api_base
        self._httpx = httpx_client
        self._max_retries = max_retries

    async def create(self, api_key, create_config):
        # POST /auth/{api_key}/create
        url = f"{self._api_base}/auth/{api_key}/create"
        dump = create_config.model_dump() if hasattr(create_config, 'model_dump') else create_config
        return await _request_with_retry(
            self._httpx,
            "POST",
            url,
            max_retries=self._max_retries,
            json=dump,
        )

    async def delete(self, api_key):
        # DELETE /auth/{api_key}/delete
        url = f"{self._api_base}/auth/{api_key}/delete"
        return await _request_with_retry(
            self._httpx,
            "DELETE",
            url,
            max_retries=self._max_retries,
        )

    async def check(self, api_key):
        # GET /auth/{api_key}/check
        url = f"{self._api_base}/auth/{api_key}/check"
        return await _request_with_retry(
            self._httpx,
            "GET",
            url,
            max_retries=self._max_retries,
        )

    async def reset(self, api_key, new_key):
        # PATCH /auth/{api_key}/reset
        url = f"{self._api_base}/auth/{api_key}/reset"
        data = {"new_key": new_key}
        return await _request_with_retry(
            self._httpx,
            "PATCH",
            url,
            max_retries=self._max_retries,
            json=data,
        )

class GroupAuthRouter:
    def __init__(self, api_base: str, httpx_client: AsyncClient, max_retries: int) -> None:
        self._api_base = api_base
        self._httpx = httpx_client
        self._max_retries = max_retries
    
    async def create(self, group_name, api_key):
        # POST /group_auth/{group_name}/create
        url = f"{self._api_base}/group_auth/{group_name}/create"
        params = {"api_key": api_key}
        return await _request_with_retry(
            self._httpx,
            "POST",
            url,
            max_retries=self._max_retries,
            params=params,
        )
    
    async def check(self, group_name, api_key):
        # GET /group_auth/{group_name}/check?api_key={api_key}
        url = f"{self._api_base}/group_auth/{group_name}/check"
        return await _request_with_retry(
            self._httpx,
            "GET",
            url,
            max_retries=self._max_retries,
            params={"api_key": api_key},
        )
    
    async def delete(self, group_name, api_key):
        # DELETE /group_auth/{group_name}/delete?api_key={api_key}
        url = f"{self._api_base}/group_auth/{group_name}/delete"
        return await _request_with_retry(
            self._httpx,
            "DELETE",
            url,
            max_retries=self._max_retries,
            params={"api_key": api_key},
        )
    
    async def list(self, api_key):
        # GET /auth/keys/{api_key}/groups
        url = f"{self._api_base}/auth/keys/{api_key}/groups"
        return await _request_with_retry(
            self._httpx,
            "GET",
            url,
            max_retries=self._max_retries,
        )

class ModelsRouter:
    def __init__(self, api_base: str, httpx_client: AsyncClient, max_retries: int) -> None:
        self._api_base = api_base
        self._httpx = httpx_client
        self._max_retries = max_retries

    async def create(self, model_id, model_config):
        # POST /models
        url = f"{self._api_base}/models"
        data = {"model_id": model_id, **model_config}
        return await _request_with_retry(
            self._httpx,
            "POST",
            url,
            max_retries=self._max_retries,
            json=data,
        )

    async def delete(self, model_id):
        # DELETE /models/{model_id}
        url = f"{self._api_base}/models/{model_id}"
        return await _request_with_retry(
            self._httpx,
            "DELETE",
            url,
            max_retries=self._max_retries,
        )

    async def about(self, model_id):
        # GET /models/{model_id}
        url = f"{self._api_base}/models/{model_id}"
        return await _request_with_retry(
            self._httpx,
            "GET",
            url,
            max_retries=self._max_retries,
        )

    async def update(self, model_id, model_config):
        # PATCH /models/{model_id}
        url = f"{self._api_base}/models/{model_id}"
        return await _request_with_retry(
            self._httpx,
            "PATCH",
            url,
            max_retries=self._max_retries,
            json=model_config,
        )

class AgentsRouter:
    class Azure:
        def __init__(self, api_base: str, httpx_client: AsyncClient, max_retries: int) -> None:
            self._api_base = api_base
            self._httpx = httpx_client
            self._max_retries = max_retries

        async def chat(self, model_id, agent_config):
            # POST /models/{model_id}/chat
            url = f"{self._api_base}/models/ragflow/{model_id}/agents/chat"
            return await _request_with_retry(
                self._httpx,
                "POST",
                url,
                max_retries=self._max_retries,
                json=agent_config,
            )

        async def related_prompts(self, model_id, agent_config):
            # POST /models/{model_id}/related_prompts
            url = f"{self._api_base}/models/{model_id}/related_prompts"
            return await _request_with_retry(
                self._httpx,
                "POST",
                url,
                max_retries=self._max_retries,
                json=agent_config,
            )

        async def transform(self, model_id, agent_config):
            # POST /models/{model_id}/transform
            url = f"{self._api_base}/models/{model_id}/transform"
            return await _request_with_retry(
                self._httpx,
                "POST",
                url,
                max_retries=self._max_retries,
                json=agent_config,
            )

        async def intents(self, model_id, agent_config):
            # POST /models/{model_id}/intents
            url = f"{self._api_base}/models/{model_id}/intents"
            return await _request_with_retry(
                self._httpx,
                "POST",
                url,
                max_retries=self._max_retries,
                json=agent_config,
            )

        async def language(self, model_id, agent_config):
            # POST /models/{model_id}/language
            url = f"{self._api_base}/models/{model_id}/language"
            return await _request_with_retry(
                self._httpx,
                "POST",
                url,
                max_retries=self._max_retries,
                json=agent_config,
            )

    class Cohere:
        def __init__(self, api_base: str, httpx_client: AsyncClient, max_retries: int) -> None:
            self._api_base = api_base
            self._httpx = httpx_client
            self._max_retries = max_retries

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

            headers = {"x-api-key": self._httpx.headers.get("x-api-key")}
            return await _request_with_retry(
                self._httpx,
                "POST",
                url,
                max_retries=self._max_retries,
                json=payload,
                headers=headers,
            )

    def __init__(self, api_base, httpx_client):
        # max_retries is owned by RAGFlowSDK; router is wired up there
        raise RuntimeError("AgentsRouter must be constructed by RAGFlowSDK with max_retries.")


class RAGFlowSDK:
    def __init__(self, api_base: str, error_stacktrace: bool = True, timeout: float = 30.0, max_retries: int = 3):
        self._api_base = api_base[:-1] if api_base.endswith("/") else api_base
        self._error_stacktrace = error_stacktrace
        self._timeout = Timeout(timeout)
        self._max_retries = max_retries
        # Use a bounded timeout to avoid hanging requests
        self._httpx = AsyncClient(timeout=self._timeout)
        # Explicitly remove Authorization header from default headers
        if "Authorization" in self._httpx.headers:
            del self._httpx.headers["Authorization"]
        self.content = ContentRouter(self._api_base, self._httpx, self._max_retries)
        self.manage = GroupsRouter(self._api_base, self._httpx, self._max_retries)
        self.auth = AuthRouter(self._api_base, self._httpx, self._max_retries)
        self.group_auth = GroupAuthRouter(self._api_base, self._httpx, self._max_retries)
        self.models = ModelsRouter(self._api_base, self._httpx, self._max_retries)
        self.agents = type("Agents", (), {})()
        self.agents.azure = AgentsRouter.Azure(self._api_base, self._httpx, self._max_retries)
        self.agents.cohere = AgentsRouter.Cohere(self._api_base, self._httpx, self._max_retries)

    def authenticate(self, api_key: str) -> None:
        # Set the API key header for all requests
        self._httpx.headers["x-api-key"] = api_key
        # Remove the Authorization header, as Criadex expects x-api-key
        if "Authorization" in self._httpx.headers:
            del self._httpx.headers["Authorization"]
        # Also remove the Authorization header from the default headers of the httpx client
        if "Authorization" in self._httpx.headers:
            del self._httpx.headers["Authorization"]