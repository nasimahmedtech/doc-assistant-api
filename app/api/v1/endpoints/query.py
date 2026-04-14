from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schema.query import QueryResponse,QueryQuestion,ChunkResultStructured
from app.api.deps import get_db
from app.utils.embedding import embed_text
router = APIRouter()

@router.post("/",response_model= QueryResponse)
def user_query(*,db: Session = Depends(get_db),payload: QueryQuestion):
    query_embeddings = embed_text(payload.question)
    db.execute(text("SET ivfflat.probes = 3"))

    results = db.execute(text("""SELECT
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
    
    return QueryResponse(
        question= payload.question,
                  results= [
                      ChunkResultStructured(
                            chunk_index=row.chunk_index,
                            content=row.content,
                            document_id = row.document_id,
                            document_title = row.document_title,
                            distance = round(row.distance,4))                                                
                            for row in results
                            ])





 





