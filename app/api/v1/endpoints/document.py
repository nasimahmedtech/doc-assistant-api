from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.schema.document import DocumentCreate,DocumentResponse
from app.model.document import Document,Chunk
from app.utils.chunking import chunk_text
from app.utils.embedding import embed_batch

router = APIRouter()

@router.post("/",response_model= DocumentResponse,status_code=status.HTTP_201_CREATED)
def create_document(*,db: Session = Depends(get_db),payload: DocumentCreate):
    doc = Document(
        title = payload.title,
        content = payload.content
    )
    db.add(doc)
    db.flush()

    chunks = chunk_text(payload.content)
    if not chunks:
        raise ValueError("Content cann't be empty")
    
    chunks_embeddings = embed_batch(chunks)


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
