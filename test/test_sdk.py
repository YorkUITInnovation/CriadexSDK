import pytest
from CriadexSDK.ragflow_sdk import RAGFlowSDK

@pytest.mark.asyncio
async def test_authentication():
    """
    Tests the authentication method of the RAGFlowSDK.
    """
    sdk = RAGFlowSDK(api_base="http://localhost:8000")
    await sdk.authenticate("test-key")
    assert sdk._httpx.headers.get("x-api-key") == "test-key"
