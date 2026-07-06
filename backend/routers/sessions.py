from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from backend.database import get_db
from backend.schemas import SessionResponse, SessionCreate
from backend.services.chat_service import ChatService
from backend.globals import base_pipeline

router = APIRouter(
    prefix="/api/sessions",
    tags=["Sessions"]
)

# Helper to get ChatService
def get_chat_service(db: Session = Depends(get_db)):
    return ChatService(db, base_pipeline)

@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(session_in: SessionCreate, service: ChatService = Depends(get_chat_service)):
    session_id = session_in.id or str(uuid.uuid4())
    session = service.get_or_create_session(session_id, title=session_in.title)
    return session

@router.get("/", response_model=List[SessionResponse])
def list_sessions(service: ChatService = Depends(get_chat_service)):
    return service.list_sessions()

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: str, service: ChatService = Depends(get_chat_service)):
    success = service.delete_session(session_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sesi dengan ID {session_id} tidak ditemukan."
        )
    return
