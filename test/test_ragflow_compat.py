import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from CriadexSDK.ragflow_sdk import RAGFlowSDK

@pytest.fixture
def sdk():
    return RAGFlowSDK(api_base="http://localhost:8000")

@pytest.mark.asyncio
async def test_content_upload_response_compatibility(sdk):
    # Mock the httpx post method to return a known response
    mock_response_obj = AsyncMock()
    # httpx.Response.json() is synchronous; use MagicMock
    mock_response_obj.json = MagicMock(return_value={"token_usage": 42, "status": "success"})
    mock_response_obj.raise_for_status = MagicMock()
    with patch.object(sdk._httpx, "post", new=AsyncMock(return_value=mock_response_obj)):
        result = await sdk.content.upload("test_group", {"file_name": "foo.txt", "file_contents": {}, "file_metadata": {}})
        assert result == mock_response_obj.json.return_value
        assert "token_usage" in result
        assert result["token_usage"] == 42
        assert result["status"] == "success"

@pytest.mark.asyncio
async def test_content_search_response_compatibility(sdk):
    # Mock the httpx post method to return a known search response
    mock_response_obj = AsyncMock()
    mock_response_obj.json = MagicMock(return_value={
        "nodes": [],
        "assets": [],
        "search_units": 1,
        "metadata": {"foo": "bar"}
    })
    mock_response_obj.raise_for_status = MagicMock()
    with patch.object(sdk._httpx, "post", new=AsyncMock(return_value=mock_response_obj)):
        result = await sdk.content.search("test_group", {"prompt": "test"})
        assert result == mock_response_obj.json.return_value
        assert "nodes" in result
        assert "assets" in result
        assert result["search_units"] == 1
        assert result["metadata"]["foo"] == "bar"

@pytest.mark.asyncio
async def test_auth_check_response_compatibility(sdk):
    # Mock the httpx get method to return a known auth check response
    mock_response_obj = AsyncMock()
    mock_response_obj.json = MagicMock(return_value={
        "api_key": "abc123",
        "master": True,
        "authorized": True
    })
    mock_response_obj.raise_for_status = MagicMock()

    # Patch sdk._httpx.get to return our mock_response_obj
    with patch.object(sdk._httpx, "get", new=AsyncMock(return_value=mock_response_obj)):
        result = await sdk.auth.check("abc123")
        expected = mock_response_obj.json.return_value
        assert result == expected
        assert result["api_key"] == "abc123"
        assert result["master"] is True
        assert result["authorized"] is True