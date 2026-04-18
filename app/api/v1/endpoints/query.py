from fastapi import APIRouter, Depends
import asyncio
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schema.query import QueryResponse,QueryQuestion,ChunkResultStructured
from app.api.deps import get_db
from app.utils.embedding import embed_text
from app.core.config import settings
from app.utils.retrieval import retrieve_relevant_chunks
from app.core.limiter import limiter
from fastapi import Request
router = APIRouter()

@router.post("/",response_model= QueryResponse)
@limiter.limit("10/minute")
async def user_query(*,request: Request,db: Session = Depends(get_db),payload: QueryQuestion):

    relevent,filtered_count = await retrieve_relevant_chunks(
        question=payload.question,
        top_k= payload.top_k,
        threshold=payload.threshold,
        db=db

    )
    

    
    return QueryResponse(
        question= payload.question,
        filtered_count=filtered_count,
                  results= [
                      ChunkResultStructured(
                            chunk_index=row.chunk_index,
                            content=row.content,
                            document_id = row.document_id,
                            document_title = row.document_title,
                            distance = round(row.distance,4))                                                
                            for row in relevent
                            ])





 





