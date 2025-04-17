from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.db import get_db
from app.services.query_handler import QueryHandler
from app.faiss.faiss_index import FAISSIndex

router = APIRouter()

# Initialize FAISS index
faiss_index = None
try:
    faiss_index = FAISSIndex()
    faiss_index.load_index()
except Exception as e:
    print(f"Warning: Could not load FAISS index: {e}")
    # Will be initialized when needed

# Pydantic models for request/response validation
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    status: str
    message: str
    response: str
    intent: str
    agent: str
    additional_data: Dict[str, Any] = {}

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Process a chat message through the agent pipeline.
    """
    print(f"\n[ChatRouter] Received chat request: {request}")
    try:
        # Initialize query handler with database session
        print(f"[ChatRouter] Initializing QueryHandler with db: {db}")
        query_handler = QueryHandler(db=db, faiss_index=faiss_index)

        # Process the query
        print(f"[ChatRouter] Processing query: '{request.message}'")
        result = query_handler.process_query(
            message=request.message,
            user_id=request.user_id,
            session_id=request.session_id
        )

        print(f"[ChatRouter] Query processed successfully, returning result")
        return result
    except Exception as e:
        print(f"[ChatRouter] Error processing chat: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@router.get("/test")
def test():
    return {"message": "Chat router is working!"}
