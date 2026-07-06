import os
from sqlalchemy.orm import Session
from fastapi import UploadFile
from backend.config import KNOWLEDGE_BASE_DIR, INDEX_PATH
from backend.models import Document as DBDocument
from core.rag import RAGPipeline

class DocumentService:
    def __init__(self, db: Session, rag_pipeline: RAGPipeline):
        self.db = db
        self.rag_pipeline = rag_pipeline
        
        # Ensure knowledge base directory exists
        if not os.path.exists(KNOWLEDGE_BASE_DIR):
            os.makedirs(KNOWLEDGE_BASE_DIR)

    def list_documents(self):
        return self.db.query(DBDocument).all()

    def upload_global_document(self, file: UploadFile):
        # Determine paths
        filename = file.filename
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, filename)
        
        # Save file to disk
        contents = file.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
            
        # Parse content to count chunks roughly
        text_content = ""
        file_type = "txt"
        if filename.endswith(".pdf"):
            file_type = "pdf"
            import pypdf
            from io import BytesIO
            try:
                reader = pypdf.PdfReader(BytesIO(contents))
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
            except Exception as e:
                raise RuntimeError(f"Gagal mengekstrak PDF: {e}")
        else:
            try:
                text_content = contents.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    text_content = contents.decode("latin-1")
                except Exception:
                    raise RuntimeError("Gagal decode file teks.")

        # Calculate chunks using RAGPipeline helper
        chunks = self.rag_pipeline.chunk_text(text_content, filename)
        chunk_count = len(chunks)

        # Check if already exists in DB
        db_doc = self.db.query(DBDocument).filter(DBDocument.filename == filename).first()
        if db_doc:
            db_doc.chunk_count = chunk_count
            db_doc.file_type = file_type
        else:
            db_doc = DBDocument(
                filename=filename,
                file_type=file_type,
                chunk_count=chunk_count
            )
            self.db.add(db_doc)
            
        self.db.commit()
        self.db.refresh(db_doc)

        # Trigger RAG Rebuild
        self.rebuild_rag_index()
        
        return db_doc

    def delete_document(self, doc_id: int):
        db_doc = self.db.query(DBDocument).filter(DBDocument.id == doc_id).first()
        if not db_doc:
            return False
            
        # Remove from disk
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, db_doc.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        # Remove from DB
        self.db.delete(db_doc)
        self.db.commit()

        # Trigger RAG Rebuild
        self.rebuild_rag_index()
        return True

    def rebuild_rag_index(self):
        # Rebuild RAG index
        self.rag_pipeline.build_index()
        return True
