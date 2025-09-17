import pytest
from unittest.mock import AsyncMock, patch
from CriadexSDK.ragflow_sdk import RAGFlowSDK
import httpx

@pytest.fixture
def sdk():
    """Fixture to provide a RAGFlowSDK instance."""
    return RAGFlowSDK(api_base="http://localhost:8000")

@pytest.mark.asyncio
async def test_authenticate(sdk):
    """Test that authenticate sets the API key correctly."""
    await sdk.authenticate(api_key="test_key")
    assert sdk._httpx.headers["x-api-key"] == "test_key"

class TestContent:
    """Tests for the Content resource."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method, sdk_method, payload, expected_endpoint",
        [
            ("post", "upload", {"file_name": "test.txt"}, "documents"),
            ("post", "search", {"prompt": "hello"}, "query"),
            ("patch", "update", {"file_name": "test.txt"}, "documents"),
        ],
    )
    async def test_content_write_methods(self, sdk, method, sdk_method, payload, expected_endpoint):
        """Test content methods that write data (POST, PATCH)."""
        with patch.object(sdk._httpx, method, new_callable=AsyncMock) as mock_method:
            mock_response = AsyncMock()
            mock_response.raise_for_status = AsyncMock()
            mock_response.json.return_value = {"status": "ok"}
            mock_method.return_value = mock_response

            sdk_call = getattr(sdk.content, sdk_method)
            result = await sdk_call("test_group", payload)

            mock_method.assert_called_once_with(
                f"http://localhost:8000/knowledge_bases/test_group/{expected_endpoint}",
                json=payload,
            )
            assert result == {"status": "ok"}

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method, sdk_method, args, expected_endpoint",
        [
            ("delete", "delete", ["doc_id"], "documents/doc_id"),
            ("get", "list", [], "documents"),
        ],
    )
    async def test_content_read_delete_methods(self, sdk, method, sdk_method, args, expected_endpoint):
        """Test content methods that read or delete data (GET, DELETE)."""
        with patch.object(sdk._httpx, method, new_callable=AsyncMock) as mock_method:
            mock_response = AsyncMock()
            mock_response.raise_for_status = AsyncMock()
            mock_response.json.return_value = {"status": "ok"}
            mock_method.return_value = mock_response

            sdk_call = getattr(sdk.content, sdk_method)
            result = await sdk_call("test_group", *args)

            mock_method.assert_called_once_with(
                f"http://localhost:8000/knowledge_bases/test_group/{expected_endpoint}"
            )
            assert result == {"status": "ok"}


class TestManage:
    """Tests for the Manage (knowledge bases) resource."""

    @pytest.mark.asyncio
    async def test_create(self, sdk):
        """Test creating a knowledge base."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = {"id": "123"}
            mock_post.return_value.raise_for_status = AsyncMock()
            result = await sdk.manage.create("test_group", {"type": "test"})
            mock_post.assert_called_once_with("http://localhost:8000/knowledge_bases", json={"name": "test_group", "type": "test"})
            assert result == {"id": "123"}

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method, sdk_method",
        [
            ("delete", "delete"),
            ("get", "about"),
        ],
    )
    async def test_manage_methods(self, sdk, method, sdk_method):
        """Test manage methods (GET, DELETE)."""
        with patch.object(sdk._httpx, method, new_callable=AsyncMock) as mock_method:
            mock_method.return_value.json.return_value = {"status": "ok"}
            mock_method.return_value.raise_for_status = AsyncMock()
            sdk_call = getattr(sdk.manage, sdk_method)
            result = await sdk_call("test_group")
            mock_method.assert_called_once_with("http://localhost:8000/knowledge_bases/test_group")
            assert result == {"status": "ok"}


class TestAuth:
    """Tests for the Auth resource."""

    @pytest.mark.asyncio
    async def test_create(self, sdk):
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = {"status": "ok"}
            mock_post.return_value.raise_for_status = AsyncMock()
            result = await sdk.auth.create("test_key", {"master": True})
            mock_post.assert_called_once_with("http://localhost:8000/auth/keys", json={"api_key": "test_key", "master": True})
            assert result == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_reset(self, sdk):
        with patch.object(sdk._httpx, 'patch', new_callable=AsyncMock) as mock_patch:
            mock_patch.return_value.json.return_value = {"status": "ok"}
            mock_patch.return_value.raise_for_status = AsyncMock()
            result = await sdk.auth.reset("test_key", "new_key")
            mock_patch.assert_called_once_with("http://localhost:8000/auth/keys/test_key", json={"new_key": "new_key"})
            assert result == {"status": "ok"}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("sdk_method, http_method", [("delete", "delete"), ("check", "get")])
    async def test_delete_check(self, sdk, sdk_method, http_method):
        with patch.object(sdk._httpx, http_method, new_callable=AsyncMock) as mock_http_method:
            mock_http_method.return_value.json.return_value = {"status": "ok"}
            mock_http_method.return_value.raise_for_status = AsyncMock()
            sdk_call = getattr(sdk.auth, sdk_method)
            result = await sdk_call("test_key")
            mock_http_method.assert_called_once_with("http://localhost:8000/auth/keys/test_key")
            assert result == {"status": "ok"}


class TestGroupAuth:
    """Tests for the GroupAuth resource."""

    @pytest.mark.asyncio
    async def test_create(self, sdk):
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = {"status": "ok"}
            mock_post.return_value.raise_for_status = AsyncMock()
            result = await sdk.group_auth.create("test_group", "test_key")
            mock_post.assert_called_once_with("http://localhost:8000/knowledge_bases/test_group/auth", json={"api_key": "test_key"})
            assert result == {"status": "ok"}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("sdk_method, http_method", [("check", "get"), ("delete", "delete")])
    async def test_check_delete(self, sdk, sdk_method, http_method):
        with patch.object(sdk._httpx, http_method, new_callable=AsyncMock) as mock_http_method:
            mock_http_method.return_value.json.return_value = {"status": "ok"}
            mock_http_method.return_value.raise_for_status = AsyncMock()
            sdk_call = getattr(sdk.group_auth, sdk_method)
            result = await sdk_call("test_group", "test_key")
            mock_http_method.assert_called_once_with("http://localhost:8000/knowledge_bases/test_group/auth/test_key")
            assert result == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_list(self, sdk):
        """Test listing groups for an API key."""
        with patch.object(sdk._httpx, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.json.return_value = ["group1", "group2"]
            mock_get.return_value.raise_for_status = AsyncMock()
            result = await sdk.group_auth.list("test_key")
            mock_get.assert_called_once_with("http://localhost:8000/auth/keys/test_key/knowledge_bases")
            assert result == ["group1", "group2"]


class TestModels:
    """Tests for the Models resource."""

    @pytest.mark.asyncio
    async def test_create_model(self, sdk):
        """Test creating a model."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = {"id": "123"}
            mock_post.return_value.raise_for_status = AsyncMock()
            result = await sdk.models.create("test_model", {"type": "test"})
            mock_post.assert_called_once_with("http://localhost:8000/models", json={"model_id": "test_model", "type": "test"})
            assert result == {"id": "123"}

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method, sdk_method",
        [
            ("delete", "delete"),
            ("get", "about"),
        ],
    )
    async def test_model_methods(self, sdk, method, sdk_method):
        """Test model methods (GET, DELETE)."""
        with patch.object(sdk._httpx, method, new_callable=AsyncMock) as mock_method:
            mock_method.return_value.json.return_value = {"status": "ok"}
            mock_method.return_value.raise_for_status = AsyncMock()
            sdk_call = getattr(sdk.models, sdk_method)
            result = await sdk_call("test_model")
            mock_method.assert_called_once_with("http://localhost:8000/models/test_model")
            assert result == {"status": "ok"}


class TestAgents:
    """Tests for the Agents resource."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "agent, sdk_method, endpoint",
        [
            ("azure", "chat", "chat"),
            ("azure", "related_prompts", "related_prompts"),
            ("azure", "transform", "transform"),
            ("cohere", "rerank", "rerank"),
        ],
    )
    async def test_agent_methods(self, sdk, agent, sdk_method, endpoint):
        """Test various agent methods."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = {"response": "ok"}
            mock_post.return_value.raise_for_status = AsyncMock()
            agent_sdk = getattr(sdk.agents, agent)
            sdk_call = getattr(agent_sdk, sdk_method)
            result = await sdk_call("test_model", {"prompt": "hello"})
            mock_post.assert_called_once_with(
                f"http://localhost:8000/models/test_model/{endpoint}",
                json={"prompt": "hello"},
            )
            assert result == {"response": "ok"}


class TestErrorHandling:
    """Tests for error handling."""

    @pytest.mark.asyncio
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
    async def test_http_status_errors(self, sdk, status_code, error_message):
        """Test that HTTP status errors are raised correctly."""
        with patch.object(sdk._httpx, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.raise_for_status = AsyncMock(
                side_effect=httpx.HTTPStatusError(
                    message=error_message,
                    request=AsyncMock(),
                    response=httpx.Response(status_code),
                )
            )
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
