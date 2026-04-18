import hashlib
import logging
import redis
from app.core.config import settings
import logging
import json
from app.core.redis_client import redis_client
logger = logging.getLogger(__name__)

def make_key(prefix: str,value: str)-> str:
    hashed = hashlib.md5(value.encode()).hexdigest()
    return f"{prefix}:{hashed}"

def get_cache_embedding(text: str) ->list[float]:
    key = make_key("embedding",text)
    try:
        cached = redis_client.get(key)
        if cached:
            logger.info(f"Embedding cache Hit | key = {key}")
            return json.loads(cached)
    except Exception as e:
        logger.info(f"Redis get failed: {e}")
    return None

def set_cache_embedding(text: str,embedding: list[float],ttl: int = 86400):
    key = make_key("embedding",text)
    try:
        redis_client.setex(key,ttl,json.dumps(embedding))
        logger.info(f"Embedding cache SET | key = {key} ttl = {ttl}") 
    except Exception as e:
        logger.info(f"Redis set failed: {e}")    


def get_cache_response(question: str) -> dict:
    key = make_key("response",question)
    try:
        cached = redis_client.get(key)
        if cached:
            logger.info(f"Response cache Hit | key = {key}")
            return json.loads(cached)
    except Exception as e:
        logger.info(f"Redis get failed: {e}")
    return None

def set_cache_response(question: str,response: dict,ttl: int = 3600):
    key = make_key("response",question)
    try:
        redis_client.setex(key,ttl,json.dumps(response)) 
        logger.info(f"Response cache Set | key = {key} ttl = {ttl}")
    except Exception as e:
        logger.info(f"Redis set failed: {e}")    