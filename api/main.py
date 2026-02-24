from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.models import QueryRequest, QueryResponse, HealthResponse, Source
from rag.query_pipeline import QueryPipeline
from rag.embedding_storage import EmbeddingStorage
import uuid

app = FastAPI(
    title="Najah Graduate Studies Chatbot API",
    description="API for querying information about Najah National University Graduate Studies",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

query_pipeline = QueryPipeline(top_k=10)
sessions = {}

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Najah Graduate Studies Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    try:
        embeddings_count = EmbeddingStorage.get_embeddings_count()
        return HealthResponse(
            status="healthy",
            embeddings_count=embeddings_count,
            version="1.0.0"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def query(request: QueryRequest):
    try:
        if not request.question or request.question.strip() == "":
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        session_id = request.session_id or str(uuid.uuid4())
        
        response = query_pipeline.query(
            request.question,
            include_context=request.include_context
        )
        
        sources = [
            Source(
                label=source.get('label', ''),
                title=source.get('title', ''),
                url=source.get('url'),
                type=source.get('type', ''),
                similarity=source.get('similarity')
            )
            for source in response.get('sources', [])
        ]
        
        return QueryResponse(
            question=response['question'],
            answer=response['answer'],
            sources=sources,
            search_results_count=response['search_results_count'],
            is_general=response.get('is_general', False),
            session_id=session_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/query/conversation", response_model=QueryResponse, tags=["Query"])
async def query_with_conversation(request: QueryRequest):
    try:
        if not request.question or request.question.strip() == "":
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        session_id = request.session_id or str(uuid.uuid4())
        
        if session_id not in sessions:
            sessions[session_id] = QueryPipeline(top_k=10)
        
        pipeline = sessions[session_id]
        response = pipeline.query_with_conversation(request.question)
        
        sources = [
            Source(
                label=source.get('label', ''),
                title=source.get('title', ''),
                url=source.get('url'),
                type=source.get('type', ''),
                similarity=None
            )
            for source in response.get('sources', [])
        ]
        
        return QueryResponse(
            question=response['question'],
            answer=response['answer'],
            sources=sources,
            search_results_count=len(response.get('sources', [])),
            session_id=session_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.delete("/session/{session_id}", tags=["Session"])
async def clear_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} cleared"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
