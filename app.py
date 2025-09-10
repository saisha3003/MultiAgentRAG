import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Ensure src directory is on the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from utils.logging_config import setup_logging
from orchestrator.master_orchestrator import MasterOrchestrator

# Initialize logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(title="Multi-Agent RAG API", version="1.0")

# Define request and response schemas
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    qa_passed: bool

# Instantiate orchestrator with your collection names
knowledge_collections = ["my_documents"]
orchestrator = MasterOrchestrator(knowledge_collections)

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    user_query = request.query.strip()
    if not user_query:
        raise HTTPException(status_code=400, detail="Query must not be empty")
    try:
        # Run the pipeline
        result = await orchestrator.run_pipeline(user_query)
        return QueryResponse(
            answer=result["answer"],
            qa_passed=result["quality_assurance"].get("approved", False)
        )
    except Exception as e:
        logger.error(f"Error handling query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
def health_check():
    return {"status": "ok"}
