
import pytest
from unittest.mock import AsyncMock

# Auth Router Tests
from CriadexSDK.routers.auth.check import AuthCheckRoute
from CriadexSDK.routers.auth.create import AuthCreateRoute, AuthCreateConfig
from CriadexSDK.routers.auth.delete import AuthDeleteRoute
from CriadexSDK.routers.auth.reset import AuthResetRoute

# Content Router Tests
from CriadexSDK.routers.content.delete import GroupContentDeleteRoute
from CriadexSDK.routers.content.list import GroupContentListRoute
from CriadexSDK.routers.content.search import GroupContentSearchRoute, SearchGroupConfig
from CriadexSDK.routers.content.upload import GroupContentUploadRoute, ContentUploadConfig
from CriadexSDK.routers.content.update import GroupContentUpdateRoute

# Group Auth Router Tests
from CriadexSDK.routers.group_auth.check import GroupAuthCheckRoute
from CriadexSDK.routers.group_auth.create import GroupAuthCreateRoute
from CriadexSDK.routers.group_auth.delete import GroupAuthDeleteRoute
from CriadexSDK.routers.group_auth.list import GroupAuthListRoute

# Groups Router Tests
from CriadexSDK.routers.groups.about import GroupAboutRoute
from CriadexSDK.routers.groups.create import GroupCreateRoute, PartialGroupConfig
from CriadexSDK.routers.groups.delete import GroupDeleteRoute

# Agents Router Tests
from CriadexSDK.routers.agents.azure.chat import AgentChatRoute, ChatAgentConfig
from CriadexSDK.routers.agents.azure.intents import AgentIntentsRoute, IntentsAgentConfig
from CriadexSDK.routers.agents.azure.lang import AgentLanguageRoute, LanguageAgentConfig
from CriadexSDK.routers.agents.cohere.rerank import AgentRerankRoute, RerankAgentConfig

# Models Router Tests
from CriadexSDK.routers.models.azure.about import ModelAboutRoute
from CriadexSDK.routers.models.azure.create import ModelCreateRoute as AzureModelCreateRoute, AzureModelBaseConfig
from CriadexSDK.routers.models.azure.delete import ModelDeleteRoute as AzureModelDeleteRoute
from CriadexSDK.routers.models.azure.update import ModelUpdateRoute as AzureModelUpdateRoute, AzureModelPartialBaseConfig

# Auth Router Tests
@pytest.mark.asyncio
async def test_auth_check(mocker):
    route = AuthCheckRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_get = mocker.patch.object(route, '_get', new_callable=AsyncMock, return_value={"authorized": True, "api_key": "test_key", "master": True, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(api_key="test_key")
    mock_get.assert_called_once_with(path="/auth/test_key/check")
    assert isinstance(response, AuthCheckRoute.Response)
    assert response.authorized is True

@pytest.mark.asyncio
async def test_auth_create(mocker):
    route = AuthCreateRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = AuthCreateConfig(master=True)
    mock_post = mocker.patch.object(route, '_post', new_callable=AsyncMock, return_value={"api_key": "new_key", "master": True, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(api_key="test_key", create_config=config)
    mock_post.assert_called_once_with(path="/auth/test_key/create", json=config)
    assert isinstance(response, AuthCreateRoute.Response)
    assert response.api_key == "new_key"

@pytest.mark.asyncio
async def test_auth_delete(mocker):
    route = AuthDeleteRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_delete = mocker.patch.object(route, '_delete', new_callable=AsyncMock, return_value={"api_key": "test_key", "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(api_key="test_key")
    mock_delete.assert_called_once_with(path="/auth/test_key/delete")
    assert isinstance(response, AuthDeleteRoute.Response)

@pytest.mark.asyncio
async def test_auth_reset(mocker):
    route = AuthResetRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_patch = mocker.patch.object(route, '_patch', new_callable=AsyncMock, return_value={"new_key": "new_api_key", "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(api_key="test_key", new_key="new_key")
    mock_patch.assert_called_once_with(path="/auth/test_key/reset", params={'new_key': 'new_key'})
    assert isinstance(response, AuthResetRoute.Response)
    assert response.new_key == "new_api_key"

# Content Router Tests
@pytest.mark.asyncio
async def test_group_content_delete(mocker):
    route = GroupContentDeleteRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_delete = mocker.patch.object(route, '_delete', new_callable=AsyncMock, return_value={"status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group", document_name="test_doc")
    mock_delete.assert_called_once_with(path="/groups/test_group/content/delete", params={"document_name": "test_doc"})
    assert isinstance(response, GroupContentDeleteRoute.Response)

@pytest.mark.asyncio
async def test_group_content_list(mocker):
    route = GroupContentListRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_get = mocker.patch.object(route, '_get', new_callable=AsyncMock, return_value={"files": ["file1.txt"], "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group")
    mock_get.assert_called_once_with(path="/groups/test_group/content/list")
    assert isinstance(response, GroupContentListRoute.Response)
    assert response.files == ["file1.txt"]

@pytest.mark.asyncio
async def test_group_content_search(mocker):
    route = GroupContentSearchRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = SearchGroupConfig(prompt="test_prompt")
    mock_post = mocker.patch.object(route, '_post', new_callable=AsyncMock, return_value={"response": {"nodes": [], "assets": []}, "group_name": "test_group", "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group", search_config=config)
    mock_post.assert_called_once_with(path="/groups/test_group/content/search", json=config)
    assert isinstance(response, GroupContentSearchRoute.Response)
    assert response.response.nodes == []

@pytest.mark.asyncio
async def test_group_content_upload(mocker):
    route = GroupContentUploadRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = ContentUploadConfig(file_name="test.txt", file_contents={}, file_metadata={})
    mock_post = mocker.patch.object(route, '_post', new_callable=AsyncMock, return_value={"token_usage": 10, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group", file=config)
    mock_post.assert_called_once_with(path="/groups/test_group/content/upload", json=config)
    assert isinstance(response, GroupContentUploadRoute.Response)
    assert response.token_usage == 10

@pytest.mark.asyncio
async def test_group_content_update(mocker):
    route = GroupContentUpdateRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = ContentUploadConfig(file_name="test.txt", file_contents={}, file_metadata={})
    mock_patch = mocker.patch.object(route, '_patch', new_callable=AsyncMock, return_value={"token_usage": 10, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group", file=config)
    mock_patch.assert_called_once_with(path="/groups/test_group/content/update", json=config)
    assert isinstance(response, GroupContentUpdateRoute.Response)
    assert response.token_usage == 10

# Group Auth Router Tests
@pytest.mark.asyncio
async def test_group_auth_check(mocker):
    route = GroupAuthCheckRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_get = mocker.patch.object(route, '_get', new_callable=AsyncMock, return_value={"authorized": True, "master": True, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group", api_key="test_key")
    mock_get.assert_called_once_with(path="/group_auth/test_group/check", params={"group_name": "test_group", "api_key": "test_key"})
    assert isinstance(response, GroupAuthCheckRoute.Response)
    assert response.authorized is True

@pytest.mark.asyncio
async def test_group_auth_create(mocker):
    route = GroupAuthCreateRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_post = mocker.patch.object(route, '_post', new_callable=AsyncMock, return_value={"status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group", api_key="test_key")
    mock_post.assert_called_once_with(path="/group_auth/test_group/create", params={"group_name": "test_group", "api_key": "test_key"})
    assert isinstance(response, GroupAuthCreateRoute.Response)

@pytest.mark.asyncio
async def test_group_auth_delete(mocker):
    route = GroupAuthDeleteRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_delete = mocker.patch.object(route, '_delete', new_callable=AsyncMock, return_value={"status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group", api_key="test_key")
    mock_delete.assert_called_once_with(path="/group_auth/test_group/delete", params={"group_name": "test_group", "api_key": "test_key"})
    assert isinstance(response, GroupAuthDeleteRoute.Response)

@pytest.mark.asyncio
async def test_group_auth_list(mocker):
    route = GroupAuthListRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_get = mocker.patch.object(route, '_get', new_callable=AsyncMock, return_value={"indexes": [], "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(api_key="test_key")
    mock_get.assert_called_once_with(path="/group_auth/list", params={"api_key": "test_key"})
    assert isinstance(response, GroupAuthListRoute.Response)
    assert response.indexes == []

# Groups Router Tests
@pytest.mark.asyncio
async def test_group_about(mocker):
    route = GroupAboutRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_get = mocker.patch.object(route, '_get', new_callable=AsyncMock, return_value={"info": {"id": 1, "created": "2023-01-01T00:00:00", "name": "test_group", "type": "DOCUMENT", "llm_model_id": 1, "embedding_model_id": 1, "rerank_model_id": 1}, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group")
    mock_get.assert_called_once_with(path="/groups/test_group/about")
    assert isinstance(response, GroupAboutRoute.Response)
    assert response.info.name == "test_group"

@pytest.mark.asyncio
async def test_group_create(mocker):
    route = GroupCreateRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = PartialGroupConfig(type="DOCUMENT", llm_model_id=1, embedding_model_id=1, rerank_model_id=1)
    mock_post = mocker.patch.object(route, '_post', new_callable=AsyncMock, return_value={"config": {"name": "test_group", "type": "DOCUMENT", "llm_model_id": 1, "embedding_model_id": 1, "rerank_model_id": 1, "id": 1, "created": "2023-01-01T00:00:00"}, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group", group_config=config)
    mock_post.assert_called_once_with(path="/groups/test_group/create", json=config)
    assert isinstance(response, GroupCreateRoute.Response)
    assert response.config.name == "test_group"

@pytest.mark.asyncio
async def test_group_delete(mocker):
    route = GroupDeleteRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_delete = mocker.patch.object(route, '_delete', new_callable=AsyncMock, return_value={"status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(group_name="test_group")
    mock_delete.assert_called_once_with(path="/groups/test_group/delete")
    assert isinstance(response, GroupDeleteRoute.Response)

# Agents Router Tests
@pytest.mark.asyncio
async def test_agent_chat(mocker):
    route = AgentChatRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = ChatAgentConfig(history=[])
    mock_post = mocker.patch.object(route, '_post', new_callable=AsyncMock, return_value={"agent_response": {"chat_response": {"message": {"role": "assistant", "blocks": []}, "raw": {"id": "", "choices": [], "created": 0, "model": "", "object": "", "system_fingerprint": "", "usage": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}}, "usage": []}, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(model_id=1, agent_config=config)
    mock_post.assert_called_once_with(path="/models/azure/1/agents/chat", json=config)
    assert isinstance(response, AgentChatRoute.Response)
    assert response.agent_response.chat_response.message.role == "assistant"

@pytest.mark.asyncio
async def test_agent_intents(mocker):
    route = AgentIntentsRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = IntentsAgentConfig(intents=[], prompt="test")
    mock_post = mocker.patch.object(route, '_post', new_callable=AsyncMock, return_value={"agent_response": {"ranked_intents": [], "usage": []}, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(model_id=1, agent_config=config)
    mock_post.assert_called_once_with(path="/models/azure/1/agents/intents", json=config)
    assert isinstance(response, AgentIntentsRoute.Response)
    assert response.agent_response.ranked_intents == []

@pytest.mark.asyncio
async def test_agent_language(mocker):
    route = AgentLanguageRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = LanguageAgentConfig(prompt="test")
    mock_post = mocker.patch.object(route, '_post', new_callable=AsyncMock, return_value={"agent_response": {"language": "en"}, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(model_id=1, agent_config=config)
    mock_post.assert_called_once_with(path="/models/azure/1/agents/language", json=config)
    assert isinstance(response, AgentLanguageRoute.Response)
    assert response.agent_response.language == "en"

@pytest.mark.asyncio
async def test_agent_rerank(mocker):
    route = AgentRerankRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = RerankAgentConfig(prompt="test", nodes=[])
    mock_post = mocker.patch.object(route, '_post', new_callable=AsyncMock, return_value={"agent_response": {"ranked_nodes": [], "search_units": 0}, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(model_id=1, agent_config=config)
    mock_post.assert_called_once_with(path="/models/cohere/1/agents/rerank", json=config)
    assert isinstance(response, AgentRerankRoute.Response)
    assert response.agent_response.ranked_nodes == []

# Models Router Tests
@pytest.mark.asyncio
async def test_model_about_azure(mocker):
    route = ModelAboutRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_get = mocker.patch.object(route, '_get', new_callable=AsyncMock, return_value={"model": {"id": 1, "api_model": "test", "api_key": "test", "api_resource": "test", "api_version": "test", "api_deployment": "test"}, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(model_id=1)
    mock_get.assert_called_once_with(path="/models/azure/1/about")
    assert isinstance(response, ModelAboutRoute.Response)
    assert response.model.api_model == "test"

@pytest.mark.asyncio
async def test_model_create_azure(mocker):
    route = AzureModelCreateRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = AzureModelBaseConfig(api_model="test", api_key="test", api_resource="test", api_version="test", api_deployment="test")
    mock_post = mocker.patch.object(route, '_post', new_callable=AsyncMock, return_value={"model": {"id": 1, "api_model": "test", "api_key": "test", "api_resource": "test", "api_version": "test", "api_deployment": "test"}, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(model_id=1, model_config=config)
    mock_post.assert_called_once_with(path="/models/azure/create", json=config)
    assert isinstance(response, AzureModelCreateRoute.Response)
    assert response.model.api_model == "test"

@pytest.mark.asyncio
async def test_model_delete_azure(mocker):
    route = AzureModelDeleteRoute(api_base="http://localhost:8000", http=AsyncMock())
    mock_delete = mocker.patch.object(route, '_delete', new_callable=AsyncMock, return_value={"status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(model_id=1)
    mock_delete.assert_called_once_with(path="/models/azure/1/delete")
    assert isinstance(response, AzureModelDeleteRoute.Response)

@pytest.mark.asyncio
async def test_model_update_azure(mocker):
    route = AzureModelUpdateRoute(api_base="http://localhost:8000", http=AsyncMock())
    config = AzureModelPartialBaseConfig()
    mock_patch = mocker.patch.object(route, '_patch', new_callable=AsyncMock, return_value={"model": {"id": 1, "api_model": "test", "api_key": "test", "api_resource": "test", "api_version": "test", "api_deployment": "test"}, "status": 200, "message": "", "code": "SUCCESS", "timestamp": 0})
    response = await route.execute(model_id=1, model_config=config)
    mock_patch.assert_called_once_with(path="/models/azure/1/update", json=config)
    assert isinstance(response, AzureModelCreateRoute.Response)
    assert response.model.api_model == "test"
