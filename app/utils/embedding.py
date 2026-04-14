import logging
from sentence_transformers import SentenceTransformer


logger = logging.getLogger()
_model = None


def get_model()-> SentenceTransformer:
    global _model
    if _model is  None:
        logger.info("Loading embedding is: all-MiniLM-l6-v2")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Embedding model loaded successfully")
    return _model


def embed_text(text: str)-> list[float]:
    if not text or not text.strip:
        raise ValueError("cannot Embed empty text")
    model = get_model()
    embedding = model.encode(text,normalize_embeddings=True)
    return embedding.tolist()



def embed_batch(texts: list[str])-> list[list[float]]:
    if not texts:
        raise ValueError("Cannot Embed empty list")
    model = get_model()
    embedding = model.encode(texts,normalize_embeddings = True,batch_size = 32)
    return embedding


    
    
    
    

        
  
    

