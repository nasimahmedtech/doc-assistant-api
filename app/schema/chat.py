from pydantic import BaseModel,Field
from app.schema.query import ChunkResultStructured
from typing import Optional

class ChatRequest(BaseModel):
    question: str = Field(...,min_length=1)
    top_k: int = Field(default=5,ge=1,le=20)
    threshlod: Optional[float] = None



class ChatResponse(BaseModel):
    question: str
    answer: str
    source: list[ChunkResultStructured]
    filtered_count: int
    

    