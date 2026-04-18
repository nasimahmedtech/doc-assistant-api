from fastapi import APIRouter, Depends
import asyncio
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schema.query import QueryResponse,ChunkResultStructured
from app.schema.chat import ChatRequest,ChatResponse
from app.api.deps import get_db
from app.utils.embedding import embed_text
from app.llm import generate_answer
from app.core.config import settings
from app.utils.retrieval import retrieve_relevant_chunks
from app.core.limiter import limiter
from fastapi import Request
from app.cache import get_cache_response,set_cache_response
router = APIRouter()

@router.post("/",response_model= ChatResponse)
@limiter.limit("10/minute")
async def user_query(*,request: Request,db: Session = Depends(get_db),payload: ChatRequest):
    cache = get_cache_response(payload.question)
    if cache:
        return ChatResponse(**cache)


    relevent,filtered_count =await retrieve_relevant_chunks(
        question=payload.question,
        top_k=payload.top_k,
        threshold=payload.threshlod,
        db=db
    )



    if not relevent:
        return ChatRequest(
            question=payload.question,
            answer = "I cound not find relevent information in the document",
            source = [],
            filtered_count = filtered_count 
        )
    
    chunk_content = [chunk.content for chunk in relevent]
    answer= await asyncio.to_thread(generate_answer,payload.question,chunk_content)

    response = ChatResponse(
        question=payload.question,
        answer=answer,
        filtered_count= filtered_count,
        source=[
            ChunkResultStructured(
                chunk_index = chunk.chunk_index,
                content = chunk.content,
                distance = round(chunk.distance, 4),
                document_id = chunk.document_id,
                document_title = chunk.document_title

            )
            for chunk in relevent
        ]

    )
    set_cache_response(payload.question,response.model_dump())
    return response
    

    
    
    