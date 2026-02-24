from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    include_context: Optional[bool] = False

class Source(BaseModel):
    label: str
    title: str
    url: Optional[str]
    type: str
    similarity: Optional[float] = None

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]
    search_results_count: int
    is_general: Optional[bool] = False
    session_id: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    embeddings_count: int
    version: str
