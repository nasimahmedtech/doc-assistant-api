from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schema.query import QueryResponse,ChunkResultStructured
from app.schema.chat import ChatRequest,ChatResponse
from app.api.deps import get_db
from app.utils.embedding import embed_text
from app.llm import generate_answer
router = APIRouter()

@router.post("/",response_model= ChatResponse)
def user_query(*,db: Session = Depends(get_db),payload: ChatRequest):
    query_embeddings = embed_text(payload.question)
    db.execute(text("SET ivfflat.probes = 3"))

    chunks = db.execute(text("""SELECT
                              c.id,
                              c.chunk_index,
                              c.content,
                              c.document_id,
                              d.title AS document_title,
                              c.embedding <-> CAST(:qvec AS Vector) AS distance

                              FROM chunks c
                              JOIN documents d ON d.id = c.document_id
                              ORDER by c.embedding <-> CAST(:qvec AS Vector)
                              LIMIT :top_k 
                              """),{
                                  "qvec": str(query_embeddings),
                                  "top_k": payload.top_k
                                  
                              }).fetchall()
    
    chunk_content = [chunk.content for chunk in chunks]
    answer=generate_answer(payload.question,chunk_content)

    return ChatResponse(
        question=payload.question,
        answer=answer,
        source=[
            ChunkResultStructured(
                chunk_index = chunk.chunk_index,
                content = chunk.content,
                distance = round(chunk.distance, 4),
                document_id = chunk.document_id,
                document_title = chunk.document_title

            )
            for chunk in chunks
        ]

    )

    
    
    