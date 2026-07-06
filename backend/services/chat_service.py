import datetime
from sqlalchemy.orm import Session
from backend.models import Session as DBSession, Message as DBMessage
from core.llm import LexaChatbot
from core.rag import RAGPipeline
from typing import Dict

# Dictionary to store session-specific RAG pipelines (with temporary documents)
_session_pipelines: Dict[str, RAGPipeline] = {}

def get_session_pipeline(session_id: str, base_pipeline: RAGPipeline) -> RAGPipeline:
    """
    Get or create a session-specific RAGPipeline.
    If it's new, it starts by loading the base vector store.
    """
    if session_id not in _session_pipelines:
        # Create a new pipeline instance for this session
        sess_pipeline = RAGPipeline()
        # Load from disk (main index cache)
        sess_pipeline.load_or_build()
        _session_pipelines[session_id] = sess_pipeline
    return _session_pipelines[session_id]

def clear_session_pipelines():
    """Clear all session-specific pipelines (call when main index changes)"""
    _session_pipelines.clear()

class ChatService:
    def __init__(self, db: Session, base_pipeline: RAGPipeline):
        self.db = db
        self.base_pipeline = base_pipeline

    def get_or_create_session(self, session_id: str, title: str = "Percakapan Baru") -> DBSession:
        session = self.db.query(DBSession).filter(DBSession.id == session_id).first()
        if not session:
            session = DBSession(id=session_id, title=title)
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
        return session

    def list_sessions(self):
        return self.db.query(DBSession).order_by(DBSession.updated_at.desc()).all()

    def get_session_history(self, session_id: str):
        # Ensure session exists
        self.get_or_create_session(session_id)
        return self.db.query(DBMessage).filter(DBMessage.session_id == session_id).order_by(DBMessage.created_at.asc()).all()

    def delete_session(self, session_id: str):
        session = self.db.query(DBSession).filter(DBSession.id == session_id).first()
        if not session:
            return False
        
        # Remove session pipeline cache
        if session_id in _session_pipelines:
            del _session_pipelines[session_id]
            
        self.db.delete(session)
        self.db.commit()
        return True

    def add_temporary_document(self, session_id: str, filename: str, text: str):
        # Ensure session exists
        self.get_or_create_session(session_id)
        # Get the session specific pipeline
        pipeline = get_session_pipeline(session_id, self.base_pipeline)
        pipeline.add_temporary_document(filename, text)

    def send_chat_message(self, session_id: str, user_message: str):
        # 1. Get or create session
        session = self.get_or_create_session(session_id)
        
        # Update title if it's still default and this is the first real message
        db_messages = self.db.query(DBMessage).filter(DBMessage.session_id == session_id).all()
        if session.title == "Percakapan Baru" and len(user_message) > 0:
            session.title = user_message[:50] + ("..." if len(user_message) > 50 else "")
            
        # 2. Get session pipeline
        pipeline = get_session_pipeline(session_id, self.base_pipeline)
        
        # 3. Initialize chatbot
        chatbot = LexaChatbot(rag_pipeline=pipeline)
        
        # 4. Reconstruct chatbot history from DB messages
        chatbot.reset_chat() # Sets system prompt
        for msg in db_messages:
            chatbot.history.append({"role": msg.role, "content": msg.content})

        # Save user message to database
        db_user_msg = DBMessage(
            session_id=session_id,
            role="user",
            content=user_message
        )
        self.db.add(db_user_msg)
        session.updated_at = datetime.datetime.utcnow()
        self.db.commit()

        # 5. Call Chatbot
        bot_response = chatbot.send_message(user_message)
        
        # Save assistant message to database
        db_assistant_msg = DBMessage(
            session_id=session_id,
            role="assistant",
            content=bot_response
        )
        self.db.add(db_assistant_msg)
        self.db.commit()

        return {
            "response": bot_response,
            "references": chatbot.last_references
        }
