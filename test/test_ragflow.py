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
    assert "Authorization" not in sdk._httpx.headers

class TestContent:
    """Tests for the Content resource."""
    
    @pytest.mark.parametrize(
        "method, sdk_method, payload, expected_endpoint",
        [
            ("POST", "upload", {"file_name": "test.txt"}, "content/upload"),
            ("POST", "search", {"prompt": "hello"}, "query"),
            ("PATCH", "update", {"file_name": "test.txt"}, "content/update"),
        ],
    )
    @pytest.mark.asyncio
    async def test_content_write_methods(self, sdk, method, sdk_method, payload, expected_endpoint):
        """Test content methods that write data (POST, PATCH)."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            # httpx.Response.json() is synchronous; use MagicMock
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_request.return_value = mock_response
            
            sdk_call = getattr(sdk.content, sdk_method)
            result = await sdk_call("test_group", payload)
            
            mock_request.assert_called_once_with(
                method,
                f"http://localhost:8000/groups/test_group/{expected_endpoint}",
                json=payload,
            )
            assert result == mock_response.json.return_value
    
    @pytest.mark.parametrize(
        "method, sdk_method, args, expected_endpoint, expected_params",
        [
            ("DELETE", "delete", ["doc_id"], "content/delete", {"document_name": "doc_id"}),
            ("GET", "list", [], "content/list", None),
        ],
    )
    @pytest.mark.asyncio
    async def test_content_read_delete_methods(self, sdk, method, sdk_method, args, expected_endpoint, expected_params):
        """Test content methods that read or delete data (GET, DELETE)."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_request.return_value = mock_response
            
            sdk_call = getattr(sdk.content, sdk_method)
            result = await sdk_call("test_group", *args)
            
            if expected_params:
                mock_request.assert_called_once_with(
                    method,
                    f"http://localhost:8000/groups/test_group/{expected_endpoint}",
                    params=expected_params,
                )
            else:
                mock_request.assert_called_once_with(
                    method,
                    f"http://localhost:8000/groups/test_group/{expected_endpoint}",
                )
            assert result == mock_response.json.return_value


class TestManage:
    """Tests for the Manage (knowledge bases) resource."""

    @pytest.mark.asyncio
    async def test_create(self, sdk):
        """Test creating a knowledge base."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"id": "123"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response
            result = await sdk.manage.create("test_group", {"type": "test"})
            mock_request.assert_called_once_with("POST", "http://localhost:8000/groups/test_group/create", json={"type": "test"})
            assert result == mock_response.json.return_value

    @pytest.mark.parametrize(
        "method, sdk_method, expected_url",
        [
            ("DELETE", "delete", "http://localhost:8000/groups/test_group/delete"),
            ("GET", "about", "http://localhost:8000/groups/test_group/about"),
        ],
    )
    @pytest.mark.asyncio
    async def test_manage_methods(self, sdk, method, sdk_method, expected_url):
        """Test manage methods (GET, DELETE)."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response
            sdk_call = getattr(sdk.manage, sdk_method)
            result = await sdk_call("test_group")
            mock_request.assert_called_once_with(method, expected_url)
            assert result == mock_response.json.return_value


class TestAuth:
    """Tests for the Auth resource."""

    @pytest.mark.asyncio
    async def test_create(self, sdk):
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response
            result = await sdk.auth.create("test_key", {"master": True})
            mock_request.assert_called_once_with("POST", "http://localhost:8000/auth/test_key/create", json={"master": True})
            assert result == mock_response.json.return_value

    @pytest.mark.asyncio
    async def test_reset(self, sdk):
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response
            result = await sdk.auth.reset("test_key", "new_key")
            mock_request.assert_called_once_with("PATCH", "http://localhost:8000/auth/test_key/reset", json={"new_key": "new_key"})
            assert result == mock_response.json.return_value

    @pytest.mark.parametrize("sdk_method, http_method", [("delete", "DELETE"), ("check", "GET")])
    @pytest.mark.asyncio
    async def test_delete_check(self, sdk, sdk_method, http_method):
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response
            sdk_call = getattr(sdk.auth, sdk_method)
            result = await sdk_call("test_key")
            mock_request.assert_called_once_with(http_method, f"http://localhost:8000/auth/test_key/{sdk_method}")
            assert result == mock_response.json.return_value


class TestGroupAuth:
    """Tests for the GroupAuth resource."""

    @pytest.mark.asyncio
    async def test_create(self, sdk):
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response

            result = await sdk.group_auth.create("test_group", "test_key")

            mock_request.assert_called_once_with(
                "POST",
                "http://localhost:8000/group_auth/test_group/create",
                params={"api_key": "test_key"}
            )
            assert result == mock_response.json.return_value

    @pytest.mark.parametrize("sdk_method, http_method", [("check", "GET"), ("delete", "DELETE")])
    @pytest.mark.asyncio
    async def test_check_delete(self, sdk, sdk_method, http_method):
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response

            sdk_call = getattr(sdk.group_auth, sdk_method)
            result = await sdk_call("test_group", "test_key")

            if sdk_method == "check":
                mock_request.assert_called_once_with(
                    http_method,
                    "http://localhost:8000/group_auth/test_group/check", params={"api_key": "test_key"}
                )
            else:
                mock_request.assert_called_once_with(
                    http_method,
                    "http://localhost:8000/group_auth/test_group/delete", params={"api_key": "test_key"}
                )
            assert result == mock_response.json.return_value

    @pytest.mark.asyncio
    async def test_list(self, sdk):
        """Test listing groups for an API key."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value=["group1", "group2"])
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response

            result = await sdk.group_auth.list("test_key")

            mock_request.assert_called_once_with(
                "GET",
                "http://localhost:8000/auth/keys/test_key/groups"
            )
            assert result == mock_response.json.return_value

class TestGroups:
    """Tests for the Groups resource."""
    
    @pytest.mark.asyncio
    async def test_create(self, sdk):
        """Test creating a group."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value={"status": "ok", "group_name": "test_group"})
            mock_request.return_value = mock_response
            
            group_config = {"description": "Test group", "settings": {}}
            result = await sdk.manage.create("test_group", group_config)
            
            mock_request.assert_called_once_with(
                "POST",
                "http://localhost:8000/groups/test_group/create",
                json=group_config
            )
            assert result == mock_response.json.return_value
    
    @pytest.mark.asyncio
    async def test_create_with_pydantic_model(self, sdk):
        """Test creating a group with a Pydantic model."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response
            
            # Mock Pydantic model
            mock_config = MagicMock()
            mock_config.model_dump.return_value = {"description": "Test", "settings": {}}
            
            result = await sdk.manage.create("test_group", mock_config)
            
            mock_request.assert_called_once_with(
                "POST",
                "http://localhost:8000/groups/test_group/create",
                json={"description": "Test", "settings": {}}
            )
            assert result == mock_response.json.return_value
    
    @pytest.mark.asyncio
    async def test_delete(self, sdk):
        """Test deleting a group."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value={"status": "deleted"})
            mock_request.return_value = mock_response
            
            result = await sdk.manage.delete("test_group")
            
            mock_request.assert_called_once_with(
                "DELETE",
                "http://localhost:8000/groups/test_group/delete"
            )
            assert result == mock_response.json.return_value
    
    @pytest.mark.asyncio
    async def test_about(self, sdk):
        """Test getting group information."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value={
                "group_name": "test_group",
                "description": "Test group",
                "created_at": "2024-01-01"
            })
            mock_request.return_value = mock_response
            
            result = await sdk.manage.about("test_group")
            
            mock_request.assert_called_once_with(
                "GET",
                "http://localhost:8000/groups/test_group/about"
            )
            json_result = mock_response.json.return_value
            assert json_result["group_name"] == "test_group"
            assert json_result["description"] == "Test group"

class TestModels:
    """Tests for the Models resource."""

    @pytest.mark.asyncio
    async def test_create_model(self, sdk):
        """Test creating a model."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"id": "123"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response
            result = await sdk.models.create("test_model", {"type": "test"})
            mock_request.assert_called_once_with("POST", "http://localhost:8000/models/azure/create", json={"model_id": "test_model", "type": "test"})
            assert result == mock_response.json.return_value

    @pytest.mark.asyncio
    async def test_about_model_with_provider_type(self, sdk):
        """Test provider-specific model about path."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response

            result = await sdk.models.about("test_model", provider_type="anthropic")
            mock_request.assert_called_once_with("GET", "http://localhost:8000/models/anthropic/test_model/about")
            assert result == mock_response.json.return_value

    @pytest.mark.parametrize(
        "method, sdk_method",
        [
            ("DELETE", "delete"),
            ("GET", "about"),
        ],
    )
    @pytest.mark.asyncio
    async def test_model_methods(self, sdk, method, sdk_method):
        """Test model methods (GET, DELETE)."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response
            sdk_call = getattr(sdk.models, sdk_method)
            result = await sdk_call("test_model")
            mock_request.assert_called_once_with(method, f"http://localhost:8000/models/azure/test_model/{sdk_method}")
            assert result == mock_response.json.return_value


class TestAgents:
    """Tests for the Agents resource."""

    @pytest.mark.parametrize(
        "agent, sdk_method, endpoint, expected_url_path",
        [
            ("azure", "chat", "chat", "models/ragflow/test_model/agents/chat"),
            ("azure", "related_prompts", "related_prompts", "models/test_model/related_prompts"),
            ("azure", "transform", "transform", "models/ragflow/test_model/agents/transform"),
            ("cohere", "rerank", "rerank", "models/test_model/rerank"),
        ],
    )
    @pytest.mark.asyncio
    async def test_agent_methods(self, sdk, agent, sdk_method, endpoint, expected_url_path):
        """Test various agent methods."""
        sdk.authenticate("test_key")
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.json = MagicMock(return_value={"response": "ok"})
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response
            agent_sdk = getattr(sdk.agents, agent)
            sdk_call = getattr(agent_sdk, sdk_method)
            result = await sdk_call("test_model", {"prompt": "hello"})
            expected_json = {"prompt": "hello"}
            if agent == "cohere" and endpoint == "rerank":
                expected_json = {"query": "hello", "documents": []}
            
            if agent == "cohere" and endpoint == "rerank":
                mock_request.assert_called_once_with(
                    "POST",
                    f"http://localhost:8000/{expected_url_path}",
                    json=expected_json,
                    headers={"x-api-key": "test_key"}
                )
            else:
                mock_request.assert_called_once_with(
                    "POST",
                    f"http://localhost:8000/{expected_url_path}",
                    json=expected_json
                )

            assert result == mock_response.json.return_value


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
        from CriadexSDK.ragflow_sdk import CriadexAPIError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    message=error_message,
                    request=MagicMock(),
                    response=httpx.Response(status_code),
                )
            )
            mock_request.return_value = mock_response
            with pytest.raises(CriadexAPIError) as excinfo:
                await sdk.content.upload("test_group", {"file_name": "test.txt"})
            assert excinfo.value.status_code == status_code

    @pytest.mark.asyncio
    async def test_network_error(self, sdk):
        """Test that network errors are handled."""
        from CriadexSDK.ragflow_sdk import CriadexNetworkError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.ConnectError("Connection failed")
            with pytest.raises(CriadexNetworkError):
                await sdk.content.upload("test_group", {"file_name": "test.txt"})

    @pytest.mark.asyncio
    async def test_timeout_error(self, sdk):
        """Test that timeout errors are handled."""
        from CriadexSDK.ragflow_sdk import CriadexNetworkError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.TimeoutException("Timeout")
            with pytest.raises(CriadexNetworkError):
                await sdk.content.upload("test_group", {"file_name": "test.txt"})

    @pytest.mark.asyncio
    async def test_5xx_retry_logic(self, sdk):
        """Test that 5xx errors trigger retry logic."""
        from CriadexSDK.ragflow_sdk import CriadexAPIError
        import asyncio
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    message="Internal Server Error",
                    request=MagicMock(),
                    response=httpx.Response(500),
                )
            )
            mock_request.return_value = mock_response
            with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                with pytest.raises(CriadexAPIError) as excinfo:
                    await sdk.content.upload("test_group", {"file_name": "test.txt"})
                # Should have retried max_retries times (default 3)
                assert mock_request.call_count == 3
                assert mock_sleep.call_count == 2  # Sleeps between retries
                assert excinfo.value.status_code == 500

    @pytest.mark.asyncio
    async def test_network_error_retry(self, sdk):
        """Test that network errors trigger retry logic."""
        from CriadexSDK.ragflow_sdk import CriadexNetworkError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.ConnectError("Connection failed")
            with patch('asyncio.sleep', new_callable=AsyncMock):
                with pytest.raises(CriadexNetworkError):
                    await sdk.content.upload("test_group", {"file_name": "test.txt"})
                # Should have retried max_retries times (default 3)
                assert mock_request.call_count == 3

    @pytest.mark.asyncio
    async def test_json_decode_error(self, sdk):
        """Test handling of invalid JSON responses."""
        from CriadexSDK.ragflow_sdk import CriadexNetworkError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(side_effect=ValueError("Invalid JSON"))
            mock_request.return_value = mock_response
            with pytest.raises(ValueError):
                await sdk.content.upload("test_group", {"file_name": "test.txt"})


class TestNegativeCases:
    """Negative test cases for edge cases and error scenarios."""

    @pytest.mark.asyncio
    async def test_authenticate_with_empty_key(self, sdk):
        """Test authentication with empty API key."""
        sdk.authenticate(api_key="")
        assert sdk._httpx.headers["x-api-key"] == ""

    @pytest.mark.asyncio
    async def test_authenticate_removes_authorization(self, sdk):
        """Test that authenticate removes Authorization header."""
        # Simulate Authorization header existing
        sdk._httpx.headers["Authorization"] = "Bearer token"
        sdk.authenticate(api_key="test_key")
        assert "Authorization" not in sdk._httpx.headers
        assert sdk._httpx.headers["x-api-key"] == "test_key"

    @pytest.mark.asyncio
    async def test_content_upload_empty_payload(self, sdk):
        """Test content upload with empty payload."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value={"status": "ok"})
            mock_request.return_value = mock_response
            result = await sdk.content.upload("test_group", {})
            assert result == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_content_search_empty_prompt(self, sdk):
        """Test content search with empty prompt."""
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value={"nodes": []})
            mock_request.return_value = mock_response
            result = await sdk.content.search("test_group", {"prompt": ""})
            assert result == {"nodes": []}

    @pytest.mark.asyncio
    async def test_auth_create_duplicate_key(self, sdk):
        """Test creating auth key that already exists (409 Conflict)."""
        from CriadexSDK.ragflow_sdk import CriadexAPIError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    message="Conflict",
                    request=MagicMock(),
                    response=httpx.Response(409),
                )
            )
            mock_request.return_value = mock_response
            with pytest.raises(CriadexAPIError) as excinfo:
                await sdk.auth.create("existing_key", {"master": False})
            assert excinfo.value.status_code == 409

    @pytest.mark.asyncio
    async def test_auth_check_nonexistent_key(self, sdk):
        """Test checking non-existent auth key (404 Not Found)."""
        from CriadexSDK.ragflow_sdk import CriadexAPIError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    message="Not Found",
                    request=MagicMock(),
                    response=httpx.Response(404),
                )
            )
            mock_request.return_value = mock_response
            with pytest.raises(CriadexAPIError) as excinfo:
                await sdk.auth.check("nonexistent_key")
            assert excinfo.value.status_code == 404

    @pytest.mark.asyncio
    async def test_group_auth_unauthorized(self, sdk):
        """Test group auth check with unauthorized key (403 Forbidden)."""
        from CriadexSDK.ragflow_sdk import CriadexAPIError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    message="Forbidden",
                    request=MagicMock(),
                    response=httpx.Response(403),
                )
            )
            mock_request.return_value = mock_response
            with pytest.raises(CriadexAPIError) as excinfo:
                await sdk.group_auth.check("test_group", "unauthorized_key")
            assert excinfo.value.status_code == 403

    @pytest.mark.asyncio
    async def test_model_delete_nonexistent(self, sdk):
        """Test deleting non-existent model (404 Not Found)."""
        from CriadexSDK.ragflow_sdk import CriadexAPIError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    message="Not Found",
                    request=MagicMock(),
                    response=httpx.Response(404),
                )
            )
            mock_request.return_value = mock_response
            with pytest.raises(CriadexAPIError) as excinfo:
                await sdk.models.delete("nonexistent_model")
            assert excinfo.value.status_code == 404

    @pytest.mark.asyncio
    async def test_agent_chat_invalid_model(self, sdk):
        """Test agent chat with invalid model ID (400 Bad Request)."""
        from CriadexSDK.ragflow_sdk import CriadexAPIError
        sdk.authenticate("test_key")
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    message="Bad Request",
                    request=MagicMock(),
                    response=httpx.Response(400),
                )
            )
            mock_request.return_value = mock_response
            with pytest.raises(CriadexAPIError) as excinfo:
                await sdk.agents.azure.chat("invalid_model", {"prompt": "test"})
            assert excinfo.value.status_code == 400

    @pytest.mark.asyncio
    async def test_content_delete_nonexistent_document(self, sdk):
        """Test deleting non-existent document (404 Not Found)."""
        from CriadexSDK.ragflow_sdk import CriadexAPIError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    message="Not Found",
                    request=MagicMock(),
                    response=httpx.Response(404),
                )
            )
            mock_request.return_value = mock_response
            with pytest.raises(CriadexAPIError) as excinfo:
                await sdk.content.delete("test_group", "nonexistent_doc")
            assert excinfo.value.status_code == 404

    @pytest.mark.asyncio
    async def test_manage_create_duplicate_group(self, sdk):
        """Test creating duplicate group (409 Conflict)."""
        from CriadexSDK.ragflow_sdk import CriadexAPIError
        with patch.object(sdk._httpx, 'request', new_callable=AsyncMock) as mock_request:
            mock_response = AsyncMock()
            mock_response.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    message="Conflict",
                    request=MagicMock(),
                    response=httpx.Response(409),
                )
            )
            mock_request.return_value = mock_response
            with pytest.raises(CriadexAPIError) as excinfo:
                await sdk.manage.create("existing_group", {"description": "test"})
            assert excinfo.value.status_code == 409

    @pytest.mark.asyncio
    async def test_sdk_initialization_with_trailing_slash(self):
        """Test SDK initialization handles trailing slash in API base."""
        sdk1 = RAGFlowSDK(api_base="http://localhost:8000/")
        sdk2 = RAGFlowSDK(api_base="http://localhost:8000")
        # Both should normalize to same base (without trailing slash)
        assert sdk1._api_base == "http://localhost:8000"
        assert sdk2._api_base == "http://localhost:8000"

    @pytest.mark.asyncio
    async def test_sdk_custom_timeout(self):
        """Test SDK initialization with custom timeout."""
        sdk = RAGFlowSDK(api_base="http://localhost:8000", timeout=60.0)
        assert sdk._timeout.read == 60.0

    @pytest.mark.asyncio
    async def test_sdk_custom_max_retries(self):
        """Test SDK initialization with custom max retries."""
        sdk = RAGFlowSDK(api_base="http://localhost:8000", max_retries=5)
        assert sdk._max_retries == 5
        assert sdk.content._max_retries == 5