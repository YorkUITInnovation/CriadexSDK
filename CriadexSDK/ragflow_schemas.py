from typing import Optional, Dict, Any
from pydantic import BaseModel

class AuthCreateConfig(BaseModel):
    master: bool = False

class AuthCreateResponse(BaseModel):
    api_key: str
    master: Optional[bool] = False

class GroupCreateConfig(BaseModel):
    type: str
    llm_model_id: int
    embedding_model_id: int
    rerank_model_id: int

class GroupCreateResponse(BaseModel):
    name: str
    type: str
    llm_model_id: int
    embedding_model_id: int
    rerank_model_id: int
    id: Optional[int]
    created: Optional[str]

# Add more as needed for other endpoints
