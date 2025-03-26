import asyncio
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging

from src.document_loader import DocumentLoader
from src.embeddings import VectorStore
from src.rag_engine import RAGEngine

from pydantic import BaseModel
from typing import Optional, Dict
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="RAG API with Deepseek")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize paths
BASE_DIR = Path(__file__).resolve().parent
DOCUMENT_DIR = BASE_DIR / "data" / "documents"
VECTOR_DIR = BASE_DIR / "data" / "vectors"

# Create directories if they don't exist
DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

# Initialize components
loader = DocumentLoader(str(DOCUMENT_DIR))
vector_store = VectorStore(str(VECTOR_DIR))
rag_engine = RAGEngine(vector_store)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    metrics: Optional[Dict] = None

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        # Get response from RAG engine
        response_data = await rag_engine.generate_response(request.query)
        
        # Transform the response to match the QueryResponse model
        return {
            'response': response_data['content'],
            'metrics': response_data.get('metrics', {})
        }

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your query: {str(e)}"
        )
    
@app.get("/")
async def read_root():
    return {
        "status": "active",
        "message": "RAG API is running",
        "endpoints": {
            "POST /upload": "Upload a document",
            "POST /query": "Query the RAG system",
            "GET /documents": "List uploaded documents"
        }
    }

@app.post("/upload")
async def upload_file(file: UploadFile):
    try:
        # Validate file type
        allowed_extensions = {'.pdf', '.sv', '.v', '.txt'}
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
            )

        # Save file
        file_path = DOCUMENT_DIR / file.filename
        content = await file.read()
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        logger.info(f"File saved: {file_path}")

        # Load and index documents
        try:
            documents = loader.load_documents()
            vector_store.add_documents(documents)
            logger.info("Documents indexed successfully")
            
            return {
                "status": "success",
                "message": "File uploaded and indexed successfully",
                "filename": file.filename
            }
        except Exception as e:
            logger.error(f"Error indexing documents: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error processing and indexing the document"
            )

    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/documents")
async def list_documents():
    try:
        documents = []
        for file_path in DOCUMENT_DIR.glob("*"):
            if file_path.is_file():
                documents.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "last_modified": file_path.stat().st_mtime
                })
        return {
            "status": "success",
            "documents": documents
        }
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error listing documents"
        )

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up RAG API...")
    # Initialize existing documents if any
    try:
        documents = loader.load_documents()
        if documents:
            vector_store.add_documents(documents)
            logger.info(f"Initialized with {len(documents)} existing documents")
    except Exception as e:
        logger.error(f"Error initializing documents: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

@app.delete("/document/{filename}")
async def delete_document(filename: str):
    try:
        file_path = DOCUMENT_DIR / filename
        if file_path.exists():
            file_path.unlink()
            logger.info(f"File deleted: {file_path}")
            
            vector_store.clear()
            # If any documents remain, reindex them
            documents = loader.load_documents()
            if documents:
                vector_store.add_documents(documents)
            else:
                # If no documents left, ensure the collection is empty
                vector_store.collection.delete(where={})
            
            return {
                "status": "success",
                "message": "File {document} deleted and documents re-indexed"
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error deleting document"
        )