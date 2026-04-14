from pydantic import BaseModel,Field
from app.schema.query import ChunkResultStructured

class ChatRequest(BaseModel):
    question: str = Field(...,min_length=1)
    top_k: int = Field(default=5,ge=1,le=20)



class ChatResponse(BaseModel):
    question: str
    answer: str
    source: list[ChunkResultStructured]
    

    