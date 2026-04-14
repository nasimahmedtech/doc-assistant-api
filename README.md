# Documentation Assistant API

A RAG system that lets you query documents in plain English.
Uploaded any documents,ask questions,get answers grounded 
in your content with source references.

## Live Demo

Coming soon --- deploying to Railway

## Architecture

Document -> token-aware chunking -> sentence-transformers
embeddings(384-dim) -> pgvector storage -> ivfflat index
-> cosine similarity search Groq LLaMA 3.3 70B generation

## Key Technical Decisions

*Token-aware-chunking over sentence splitting*
sentence splitting breaks on poorly formatted documents.
Token-aware chunking with overlap guarantees consistent
chunk sizes matching the embedding model's input limits.

*ivfflat index with probes = 3*
Full cosine scan is O(n) - unusable at scale.ivfflat 
clusters vectors into lists,reducing search to nearby
clusters only.probes = 3 searches 3 nearest clusters,
balancing recall(~95%)vs speed.

*flush() before embed_batch()*
Ensures Document ID is avilable for chunk foreign keys
While keeping the entire operation in one transaction.
If embedding fails,document and chunks both roll back.

*Groq over openAI*
200-400 tokens/second vs 20-40.RAG already has latency 
from embeddings+vector search.Groq keeps total
response time under 2 seconds

## Stack
. FastAPI
. PostgreSQL + pgvector
. sentence-transformers(all-MiniLM-L6-v2)
. SQLAlchemy + Alembic
. Groq LLaMA 3.3 70B
. Docker

## Run locally
### Prerequisites
. Docker and Docker compose
.Groq API key

## Setup
bash
git clone https://github.com/yourusername/doc-assistant-api
cd doc-assistant-api
cp .env.example .env
# add your GROQ_API_KEY to .env
docker compose up
## Run migrations
bash
docker compose exec app alembic upgrade head

### API Endpoints
- POST /api/v1/documents/ — ingest a document
- POST /api/v1/query/     — semantic search
- POST /api/v1/chat/      — RAG question answering
- GET  /docs              — Swagger UI

## API Usage

*Ingest a document:*
json
POST /api/v1/documents/
{
  "title": "Your Document Title",
  "content": "Your document content here..."
}

*Ask a question:*
```json
POST /api/v1/chat/
{
  "question": "What is X?",
  "top_k": 5
}



