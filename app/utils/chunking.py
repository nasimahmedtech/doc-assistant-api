import logging
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

TOKENIZER_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
_tokenizer = None

def chunk_model()-> SentenceTransformer:
    global _tokenizer
    if not _tokenizer:
        logger.info(f"Tokenizer loading")
        _tokenizer =  AutoTokenizer.from_pretrained(TOKENIZER_MODEL)
        logger.info(f"Tokenizer loaded successfully")
    return _tokenizer


def chunk_text(text: str,chunk_size:int = 200,overlap: int = 50)-> list[str]:
    if not text or not text.strip:
        raise ValueError("Text cannot be empty")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk size")
    
    tokenizer = chunk_model()
    token_ids = tokenizer.encode(text,add_special_tokens = False)
    if not token_ids:
        raise ValueError("text produced no tokens after encoding")
    
    chunks= []
    start = 0
    step = chunk_size - overlap
    while start < len(token_ids):
        end = start + chunk_size
        chunk_token_ids = token_ids[start: end]

        chunk_text_decoded = tokenizer.decode(chunk_token_ids,skip_special_tokens = True,clean_up_tokenization_spaces = True,)

        if chunk_text_decoded.strip():
            chunks.append(chunk_text_decoded.strip())
        start += step

        logger.info(
            f"Chunk text into {len(chunks)} Chunks"
            f"Chunk_size = {chunk_size},overlap = {overlap}"
            f"total_tokens = {len(token_ids)}"
        )    
    return chunks


def chunk_documents(documents: list[str],chunk_size = 500,overlap = 50)-> list[list[str]]:
    return [chunk_text(doc,chunk_size,overlap)for doc in documents]


    

        

        
    

