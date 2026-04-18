from pydantic import BaseModel, Field,ConfigDict
from typing import Optional

class QueryQuestion(BaseModel):
    question: str = Field(...,min_length= 1)
    top_k : int = Field(default=5,ge=1,le=20)
    threshold: Optional[float] = None

class ChunkResultStructured(BaseModel):
    chunk_index: int
    document_id: int
    document_title: str
    content: str
    distance: float

    model_config = ConfigDict(from_attributes=True)


class QueryResponse(QueryQuestion):
    question: str
    results: list[ChunkResultStructured]
    filtered_count: int

