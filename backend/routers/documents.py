from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.schemas import DocumentResponse, RebuildIndexResponse
from backend.services.document_service import DocumentService
from backend.services.chat_service import ChatService, clear_session_pipelines
from backend.globals import base_pipeline
import pypdf
from io import BytesIO

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

# Helper to get DocumentService
def get_doc_service(db: Session = Depends(get_db)):
    return DocumentService(db, base_pipeline)

# Helper to get ChatService
def get_chat_service(db: Session = Depends(get_db)):
    return ChatService(db, base_pipeline)

@router.get("/", response_model=List[DocumentResponse])
def list_documents(service: DocumentService = Depends(get_doc_service)):
    return service.list_documents()

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_global_document(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_doc_service)
):
    # Validation file extensions
    filename = file.filename
    if not filename.endswith((".pdf", ".txt", ".md")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipe file tidak didukung. Harap unggah file PDF, TXT, atau MD."
        )
        
    try:
        doc = service.upload_global_document(file)
        # Clear all session-specific cached pipelines because base index changed
        clear_session_pipelines()
        return doc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    doc_id: int,
    service: DocumentService = Depends(get_doc_service)
):
    success = service.delete_document(doc_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dokumen dengan ID {doc_id} tidak ditemukan."
        )
    # Clear all session-specific cached pipelines because base index changed
    clear_session_pipelines()
    return

@router.post("/rebuild-index", response_model=RebuildIndexResponse)
def rebuild_index(service: DocumentService = Depends(get_doc_service)):
    try:
        service.rebuild_rag_index()
        clear_session_pipelines()
        return RebuildIndexResponse(
            status="success",
            message="Indeks RAG berhasil dibangun ulang untuk semua dokumen."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/upload-temp/{session_id}", status_code=status.HTTP_200_OK)
async def upload_temp_document(
    session_id: str,
    file: UploadFile = File(...),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Unggah dokumen PDF atau TXT sementara untuk sesi aktif saja (in-memory).
    Dokumen tidak akan disimpan di disk dan hilang jika server restart / session dihapus.
    """
    filename = file.filename
    if not filename.endswith((".pdf", ".txt", ".md")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipe file tidak didukung. Harap unggah file PDF, TXT, atau MD."
        )

    contents = await file.read()
    extracted_text = ""
    
    try:
        if filename.endswith(".pdf"):
            reader = pypdf.PdfReader(BytesIO(contents))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
        else:
            try:
                extracted_text = contents.decode("utf-8")
            except UnicodeDecodeError:
                extracted_text = contents.decode("latin-1")
                
        if not extracted_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File kosong atau tidak dapat diekstrak teksnya."
            )
            
        chat_service.add_temporary_document(session_id, filename, extracted_text)
        return {"status": "success", "message": f"Berhasil mengindeks file sementara '{filename}'."}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal memproses file: {str(e)}"
        )
