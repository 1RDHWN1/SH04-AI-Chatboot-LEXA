from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Message Schemas
class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    session_id: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

# Session Schemas
class SessionBase(BaseModel):
    title: Optional[str] = "Percakapan Baru"

class SessionCreate(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = "Percakapan Baru"

class SessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

# Chat Schemas
class ChatRequest(BaseModel):
    message: str

class ReferenceMetadata(BaseModel):
    source: str
    document_title: str

class ReferenceChunk(BaseModel):
    content: str
    metadata: ReferenceMetadata

class ReferenceItem(BaseModel):
    chunk: ReferenceChunk
    score: float

class ChatResponse(BaseModel):
    response: str
    references: List[ReferenceItem]

# Document Schemas
class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    chunk_count: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class RebuildIndexResponse(BaseModel):
    status: str
    message: str
