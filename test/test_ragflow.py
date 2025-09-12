import pytest
from unittest.mock import AsyncMock, MagicMock
import httpx

from CriadexSDK.ragflow_sdk import RAGFlowSDK

# Tests for ragflow_sdk.py (interface compatibility and basic behavior)

@pytest.fixture
def sdk():
    return RAGFlowSDK(api_base="http://localhost:8000")

@pytest.mark.asyncio
async def test_authenticate_sets_api_key(sdk):
    await sdk.authenticate(api_key="test_key")
    assert sdk._httpx.headers["x-api-key"] == "test_key"

@pytest.mark.asyncio
async def test_content_router_methods_exist(sdk):
    # Just check methods exist and are callable (not full integration)
    assert hasattr(sdk.content, "upload")
    assert hasattr(sdk.content, "search")
    assert hasattr(sdk.content, "update")
    assert hasattr(sdk.content, "delete")
    assert hasattr(sdk.content, "list")

@pytest.mark.asyncio
async def test_groups_router_methods_exist(sdk):
    assert hasattr(sdk.manage, "create")
    assert hasattr(sdk.manage, "delete")
    assert hasattr(sdk.manage, "about")

@pytest.mark.asyncio
async def test_auth_router_methods_exist(sdk):
    assert hasattr(sdk.auth, "create")
    assert hasattr(sdk.auth, "delete")
    assert hasattr(sdk.auth, "check")
    assert hasattr(sdk.auth, "reset")

@pytest.mark.asyncio
async def test_group_auth_router_methods_exist(sdk):
    assert hasattr(sdk.group_auth, "create")
    assert hasattr(sdk.group_auth, "check")
    assert hasattr(sdk.group_auth, "delete")
    assert hasattr(sdk.group_auth, "list")

@pytest.mark.asyncio
async def test_models_router_methods_exist(sdk):
    assert hasattr(sdk.models, "create")
    assert hasattr(sdk.models, "delete")
    assert hasattr(sdk.models, "about")

@pytest.mark.asyncio
async def test_agents_router_methods_exist(sdk):
    assert hasattr(sdk.agents, "azure")
    assert hasattr(sdk.agents, "cohere")
    assert hasattr(sdk.agents.azure, "chat")
    assert hasattr(sdk.agents.azure, "related_prompts")
    assert hasattr(sdk.agents.azure, "transform")
    assert hasattr(sdk.agents.cohere, "rerank")
