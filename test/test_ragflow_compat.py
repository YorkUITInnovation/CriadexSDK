import pytest
from unittest.mock import MagicMock, patch
from CriadexSDK.ragflow_sdk import RAGFlowSDK

@pytest.fixture
def sdk():
    return RAGFlowSDK(api_base="http://localhost:8000")

def test_content_upload_response_compatibility(sdk):
    # Mock the httpx post method to return a known response
    mock_response = {"token_usage": 42, "status": "success"}
    with patch.object(sdk._httpx, "post", new=MagicMock(return_value=MagicMock(json=MagicMock(return_value=mock_response), raise_for_status=MagicMock()))):
        result = sdk.content.upload("test_group", {"file_name": "foo.txt", "file_contents": {}, "file_metadata": {}})
        assert result == mock_response
        assert "token_usage" in result
        assert result["token_usage"] == 42
        assert result["status"] == "success"

def test_content_search_response_compatibility(sdk):
    # Mock the httpx post method to return a known search response
    mock_response = {
        "nodes": [],
        "assets": [],
        "search_units": 1,
        "metadata": {"foo": "bar"}
    }
    with patch.object(sdk._httpx, "post", new=MagicMock(return_value=MagicMock(json=MagicMock(return_value=mock_response), raise_for_status=MagicMock()))):
        result = sdk.content.search("test_group", {"prompt": "test"})
        assert result == mock_response
        assert "nodes" in result
        assert "assets" in result
        assert result["search_units"] == 1
        assert result["metadata"]["foo"] == "bar"

def test_auth_check_response_compatibility(sdk):
    # Mock the httpx get method to return a known auth check response
    mock_response = {"api_key": "abc123", "master": True, "authorized": True}
    with patch.object(sdk._httpx, "get", new=MagicMock(return_value=MagicMock(json=MagicMock(return_value=mock_response), raise_for_status=MagicMock()))):
        result = sdk.auth.check("abc123")
        assert result == mock_response
        assert result["api_key"] == "abc123"
        assert result["master"] is True
        assert result["authorized"] is True