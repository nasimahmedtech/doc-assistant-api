from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schema.document import DocumentCreate,DocumentResponse
from app.model.document import Document,Chunk
from app.utils.chunking import chunk_text
from app.utils.embedding import embed_batch
from fastapi import Request
from app.core.limiter import limiter
import asyncio

router = APIRouter()

@router.post("/",response_model= DocumentResponse,status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_document(*,request: Request,db: Session = Depends(get_db),payload: DocumentCreate):
    doc = Document(
        title = payload.title,
        content = payload.content
    )
    db.add(doc)
    db.flush()

    chunks = await asyncio.to_thread(chunk_text,payload.content)
    if not chunks:
        raise ValueError("Content cann't be empty")
    
    chunks_embeddings = await asyncio.to_thread(embed_batch,chunks)


    db.add_all([ Chunk(
        document_id = doc.id,
        content = chunk,
        embedding = chunks_embedding,
        chunk_index = i,


    )
    for i,(chunk,chunks_embedding) in enumerate(zip(chunks,chunks_embeddings))
    ])
    db.commit()
    db.refresh(doc)
    return doc
