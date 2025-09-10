import asyncio
from CriadexSDK.ragflow_sdk import RAGFlowSDK

async def main():
    sdk = RAGFlowSDK(api_base="http://localhost:8000")
    await sdk.authenticate("test-key")
    print("API key header set:", sdk._httpx.headers.get("x-api-key"))

if __name__ == "__main__":
    asyncio.run(main())
