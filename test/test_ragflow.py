import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from CriadexSDK.ragflow_sdk import RAGFlowSDK
import httpx

@pytest.fixture
def sdk():
    """Fixture to provide a RAGFlowSDK instance."""
    return RAGFlowSDK(api_base="http://localhost:8000")

def test_authenticate(sdk):
    """Test that authenticate sets the API key correctly."""
    sdk.authenticate(api_key="test_key")
    assert sdk._httpx.headers["x-api-key"] == "test_key"

class TestContent:
    """Tests for the Content resource."""
    
    @pytest.mark.parametrize(
        "method, sdk_method, payload, expected_endpoint",
        [
            ("post", "upload", {"file_name": "test.txt"}, "content/upload"),
            ("post", "search", {"prompt": "hello"}, "query"),
            ("patch", "update", {"file_name": "test.txt"}, "content/update"),
        ],
    )
    @pytest.mark.asyncio
    async def test_content_write_methods(self, sdk, method, sdk_method, payload, expected_endpoint):
        """Test content methods that write data (POST, PATCH)."""
        with patch.object(sdk._httpx, method, new_callable=AsyncMock) as mock_method:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            # httpx.Response.json() is synchronous; use MagicMock
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_method.return_value = mock_response
            
            sdk_call = getattr(sdk.content, sdk_method)
            result = await sdk_call("test_group", payload)
            
            mock_method.assert_called_once_with(
                f"http://localhost:8000/groups/test_group/{expected_endpoint}",
                json=payload,
            )
            assert result == mock_response.json.return_value
    
    @pytest.mark.parametrize(
        "method, sdk_method, args, expected_endpoint",
        [
            ("delete", "delete", ["doc_id"], "content/delete?document_name=doc_id"),
            ("get", "list", [], "content/list"),
        ],
    )
    @pytest.mark.asyncio
    async def test_content_read_delete_methods(self, sdk, method, sdk_method, args, expected_endpoint):
        """Test content methods that read or delete data (GET, DELETE)."""
        with patch.object(sdk._httpx, method, new_callable=AsyncMock) as mock_method:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_method.return_value = mock_response
            
            sdk_call = getattr(sdk.content, sdk_method)
            result = await sdk_call("test_group", *args)
            
            mock_method.assert_called_once_with(
                f"http://localhost:8000/groups/test_group/{expected_endpoint}"
            )
            assert result == mock_response.json.return_value


class TestManage:
    """Tests for the Manage (knowledge bases) resource."""

    @pytest.mark.asyncio
    async def test_create(self, sdk):
        """Test creating a knowledge base."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"id": "123"}
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response
            result = await sdk.manage.create("test_group", {"type": "test"})
            mock_post.assert_called_once_with("http://localhost:8000/groups/test_group/create", json={"type": "test"})
            assert await result == await mock_response.json()

    @pytest.mark.parametrize(
        "method, sdk_method",
        [
            ("delete", "delete"),
            ("get", "about"),
        ],
    )
    @pytest.mark.asyncio
    async def test_manage_methods(self, sdk, method, sdk_method):
        """Test manage methods (GET, DELETE)."""
        with patch.object(sdk._httpx, method, new_callable=AsyncMock) as mock_method:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"status": "ok"}
            mock_response.raise_for_status = MagicMock()
            mock_method.return_value = mock_response
            sdk_call = getattr(sdk.manage, sdk_method)
            result = await sdk_call("test_group")
            if sdk_method == 'delete':
                mock_method.assert_called_once_with("http://localhost:8000/groups/test_group/delete")
            else:
                mock_method.assert_called_once_with("http://localhost:8000/groups/test_group/about")
            assert await result == await mock_response.json()


class TestAuth:
    """Tests for the Auth resource."""

    @pytest.mark.asyncio
    async def test_create(self, sdk):
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"status": "ok"}
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response
            result = await sdk.auth.create("test_key", {"master": True})
            mock_post.assert_called_once_with("http://localhost:8000/auth/test_key/create", json={"master": True})
            assert await result == await mock_response.json()

    @pytest.mark.asyncio
    async def test_reset(self, sdk):
        with patch.object(sdk._httpx, 'patch', new_callable=AsyncMock) as mock_patch:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"status": "ok"}
            mock_response.raise_for_status = MagicMock()
            mock_patch.return_value = mock_response
            result = await sdk.auth.reset("test_key", "new_key")
            mock_patch.assert_called_once_with("http://localhost:8000/auth/keys/test_key", json={"new_key": "new_key"})
            assert await result == await mock_response.json()

    @pytest.mark.parametrize("sdk_method, http_method", [("delete", "delete"), ("check", "get")])
    @pytest.mark.asyncio
    async def test_delete_check(self, sdk, sdk_method, http_method):
        with patch.object(sdk._httpx, http_method, new_callable=AsyncMock) as mock_http_method:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"status": "ok"}
            mock_response.raise_for_status = MagicMock()
            mock_http_method.return_value = mock_response
            sdk_call = getattr(sdk.auth, sdk_method)
            result = await sdk_call("test_key")
            mock_http_method.assert_called_once_with("http://localhost:8000/auth/keys/test_key")
            assert await result == await mock_response.json()


class TestGroupAuth:
    """Tests for the GroupAuth resource."""

    @pytest.mark.asyncio
    async def test_create(self, sdk):
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response

            result = await sdk.group_auth.create("test_group", "test_key")

            mock_post.assert_called_once_with(
                "http://localhost:8000/group_auth/test_group/create",
                params={"api_key": "test_key"}
            )
            assert result == mock_response.json.return_value

    @pytest.mark.parametrize("sdk_method, http_method", [("check", "get"), ("delete", "delete")])
    @pytest.mark.asyncio
    async def test_check_delete(self, sdk, sdk_method, http_method):
        with patch.object(sdk._httpx, http_method, new_callable=AsyncMock) as mock_http_method:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_http_method.return_value = mock_response

            sdk_call = getattr(sdk.group_auth, sdk_method)
            result = await sdk_call("test_group", "test_key")

            if sdk_method == "check":
                mock_http_method.assert_called_once_with(
                    "http://localhost:8000/group_auth/test_group/check", params={"api_key": "test_key"}
                )
            else:
                mock_http_method.assert_called_once_with(
                    "http://localhost:8000/group_auth/test_group/delete", params={"api_key": "test_key"}
                )
            assert result == mock_response.json.return_value

    @pytest.mark.asyncio
    async def test_list(self, sdk):
        """Test listing groups for an API key."""
        with patch.object(sdk._httpx, 'get', new_callable=AsyncMock) as mock_get:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value=["group1", "group2"])
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response

            result = await sdk.group_auth.list("test_key")

            mock_get.assert_called_once_with(
                "http://localhost:8000/auth/keys/test_key/groups"
            )
            assert result == mock_response.json.return_value

class TestGroups:
    """Tests for the Groups resource."""
    
    @pytest.mark.asyncio
    async def test_create(self, sdk):
        """Test creating a group."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {"status": "ok", "group_name": "test_group"}
            mock_post.return_value = mock_response
            
            group_config = {"description": "Test group", "settings": {}}
            result = await sdk.manage.create("test_group", group_config)
            
            mock_post.assert_called_once_with(
                "http://localhost:8000/groups/test_group/create",
                json=group_config
            )
            assert await result == await mock_response.json()
    
    @pytest.mark.asyncio
    async def test_create_with_pydantic_model(self, sdk):
        """Test creating a group with a Pydantic model."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"status": "ok"}
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response
            
            # Mock Pydantic model
            mock_config = MagicMock()
            mock_config.model_dump.return_value = {"description": "Test", "settings": {}}
            
            result = await sdk.manage.create("test_group", mock_config)
            
            mock_post.assert_called_once_with(
                "http://localhost:8000/groups/test_group/create",
                json={"description": "Test", "settings": {}}
            )
            assert await result == await mock_response.json()
    
    @pytest.mark.asyncio
    async def test_delete(self, sdk):
        """Test deleting a group."""
        with patch.object(sdk._httpx, 'delete', new_callable=AsyncMock) as mock_delete:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {"status": "deleted"}
            mock_delete.return_value = mock_response
            
            result = await sdk.manage.delete("test_group")
            
            mock_delete.assert_called_once_with(
                "http://localhost:8000/groups/test_group/delete"
            )
            assert await result == await mock_response.json()
    
    @pytest.mark.asyncio
    async def test_about(self, sdk):
        """Test getting group information."""
        with patch.object(sdk._httpx, 'get', new_callable=AsyncMock) as mock_get:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {
                "group_name": "test_group",
                "description": "Test group",
                "created_at": "2024-01-01"
            }
            mock_get.return_value = mock_response
            
            result = await sdk.manage.about("test_group")
            
            mock_get.assert_called_once_with(
                "http://localhost:8000/groups/test_group/about"
            )
            json_result = await mock_response.json()
            assert json_result["group_name"] == "test_group"
            assert json_result["description"] == "Test group"

class TestModels:
    """Tests for the Models resource."""

    @pytest.mark.asyncio
    async def test_create_model(self, sdk):
        """Test creating a model."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"id": "123"}
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response
            result = await sdk.models.create("test_model", {"type": "test"})
            mock_post.assert_called_once_with("http://localhost:8000/models", json={"model_id": "test_model", "type": "test"})
            assert await result == await mock_response.json()

    @pytest.mark.parametrize(
        "method, sdk_method",
        [
            ("delete", "delete"),
            ("get", "about"),
        ],
    )
    @pytest.mark.asyncio
    async def test_model_methods(self, sdk, method, sdk_method):
        """Test model methods (GET, DELETE)."""
        with patch.object(sdk._httpx, method, new_callable=AsyncMock) as mock_method:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"status": "ok"}
            mock_response.raise_for_status = MagicMock()
            mock_method.return_value = mock_response
            sdk_call = getattr(sdk.models, sdk_method)
            result = await sdk_call("test_model")
            mock_method.assert_called_once_with("http://localhost:8000/models/test_model")
            assert await result == await mock_response.json()


class TestAgents:
    """Tests for the Agents resource."""

    @pytest.mark.parametrize(
        "agent, sdk_method, endpoint, expected_url_path",
        [
            ("azure", "chat", "chat", "models/ragflow/test_model/agents/chat"),
            ("azure", "related_prompts", "related_prompts", "models/test_model/related_prompts"),
            ("azure", "transform", "transform", "models/test_model/transform"),
            ("cohere", "rerank", "rerank", "models/test_model/rerank"),
        ],
    )
    @pytest.mark.asyncio
    async def test_agent_methods(self, sdk, agent, sdk_method, endpoint, expected_url_path):
        """Test various agent methods."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"response": "ok"}
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response
            agent_sdk = getattr(sdk.agents, agent)
            sdk_call = getattr(agent_sdk, sdk_method)
            result = await sdk_call("test_model", {"prompt": "hello"})
            expected_json = {"prompt": "hello"}
            if agent == "cohere" and endpoint == "rerank":
                expected_json = {"query": "hello", "documents": []}
            mock_post.assert_called_once_with(
                f"http://localhost:8000/{expected_url_path}",
                json=expected_json,
            )
            assert await result == await mock_response.json()


class TestErrorHandling:
    """Tests for error handling."""

    @pytest.mark.parametrize(
        "status_code, error_message",
        [
            (400, "Bad Request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not Found"),
            (500, "Internal Server Error"),
        ],
    )
    @pytest.mark.asyncio
    async def test_http_status_errors(self, sdk, status_code, error_message):
        """Test that HTTP status errors are raised correctly."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    message=error_message,
                    request=MagicMock(),
                    response=httpx.Response(status_code),
                )
            )
            mock_post.return_value = mock_response
            with pytest.raises(httpx.HTTPStatusError) as excinfo:
                await sdk.content.upload("test_group", {"file_name": "test.txt"})
            assert excinfo.value.response.status_code == status_code

    @pytest.mark.asyncio
    async def test_network_error(self, sdk):
        """Test that network errors are handled."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = httpx.ConnectError("Connection failed")
            with pytest.raises(httpx.ConnectError):
                await sdk.content.upload("test_group", {"file_name": "test.txt"})

    @pytest.mark.asyncio
    async def test_timeout_error(self, sdk):
        """Test that timeout errors are handled."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = httpx.TimeoutException("Timeout")
            with pytest.raises(httpx.TimeoutException):
                await sdk.content.upload("test_group", {"file_name": "test.txt"})