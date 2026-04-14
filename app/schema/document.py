from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime
from typing import Optional

class ChunkBase(BaseModel):
    content: str 
    chunk_index: int

class ChunkCreate(ChunkBase):
    document_id: str
    embedding: Optional[list[float]] = None


class ChunkResponse(ChunkBase): 
    id: int
    document_id: int
    create_at: datetime
    model_config = ConfigDict(from_attributes=True)

    


class DocumentBase(BaseModel):
    title: str = Field(...,)
    content: str = Field(...,)


class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    chunks: list[ChunkResponse] = []
    create_at: datetime
    update_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
    






