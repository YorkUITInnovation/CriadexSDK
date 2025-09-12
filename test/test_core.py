import pytest
from unittest.mock import AsyncMock, MagicMock
import httpx

from CriadexSDK.core.criadex import CriadexSDK
from CriadexSDK.core.schemas import CriadexUnauthorizedError
from CriadexSDK.core.network import create_httpx_client
from CriadexSDK.core.api.route import CriadexError, BaseResponse
from CriadexSDK.routers.auth.check import AuthCheckRoute


# Tests for schemas.py

def test_criadex_unauthorized_error():
    with pytest.raises(CriadexUnauthorizedError):
        raise CriadexUnauthorizedError("Test")

def test_criadex_error():
    with pytest.raises(CriadexError):
        raise CriadexError(bad_response=BaseResponse(status=400, message="", code="ERROR"))

def test_base_response_verify():
    response = BaseResponse(status=200, message="", code="SUCCESS")
    response.verify()

    response = BaseResponse(status=400, message="", code="ERROR")
    with pytest.raises(CriadexError):
        response.verify()

# Tests for network.py

def test_create_httpx_client():
    client = create_httpx_client(error_stacktrace=True)
    assert isinstance(client, httpx.AsyncClient)
    assert client.headers["x-api-stacktrace"] == "true"

    client = create_httpx_client(error_stacktrace=False)
    assert client.headers["x-api-stacktrace"] == "false"

# Tests for criadex.py

@pytest.fixture
def sdk():
    return CriadexSDK(api_base="http://localhost:8000")

@pytest.mark.asyncio
async def test_authenticate_invalid_key(sdk, mocker):
    mocker.patch.object(sdk, 'is_master', return_value=False)
    with pytest.raises(CriadexUnauthorizedError):
        await sdk.authenticate(api_key="invalid_key")

@pytest.mark.asyncio
async def test_authenticate_valid_key(sdk, mocker):
    mocker.patch.object(sdk, 'is_master', return_value=True)
    mocker.patch.object(sdk, '_include_routers')
    await sdk.authenticate(api_key="valid_key")
    assert sdk._httpx.headers["x-api-key"] == "valid_key"
    sdk._include_routers.assert_called_once()

@pytest.mark.asyncio
async def test_is_master(sdk, mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    
    mock_get = AsyncMock(return_value=mock_response)
    mocker.patch.object(sdk._httpx, 'get', mock_get)
    
    result = await sdk.is_master(api_key="some_key")
    
    assert result is True
    mock_get.assert_called_once_with(
        "http://localhost:8000/auth/some_key/check",
        headers={"x-api-key": "some_key"}
    )

@pytest.mark.asyncio
async def test_is_master_unauthorized(sdk, mocker):
    mock_response = MagicMock()
    mock_response.status_code = 401
    
    mock_get = AsyncMock(return_value=mock_response)
    mocker.patch.object(sdk._httpx, 'get', mock_get)
    
    result = await sdk.is_master(api_key="some_key")
    
    assert result is False

@pytest.mark.asyncio
async def test_base_request_exception(mocker):
    mock_http_client = AsyncMock()
    mock_http_client.get.side_effect = Exception("Test Exception")
    route = AuthCheckRoute(api_base="http://localhost:8000", http=mock_http_client)
    result = await route.execute(api_key="test_key")
    assert isinstance(result, BaseResponse)
    assert result.code == "SERIALIZE_ERROR"