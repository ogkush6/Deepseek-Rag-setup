
# src/document_loader.py
import os
from typing import List, Dict
from pathlib import Path
from pypdf import PdfReader

class DocumentLoader:
    def __init__(self, document_dir: str):
        self.document_dir = Path(document_dir)
        
    def load_text_file(self, file_path: Path) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    def load_pdf_file(self, file_path: Path) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
        
    def load_documents(self) -> List[Dict[str, str]]:
        documents = []
        for file_path in self.document_dir.rglob("*"):
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() in ['.v', '.sv']:
                        content = self.load_text_file(file_path)
                        doc_type = 'hdl'
                    elif file_path.suffix.lower() == '.pdf':
                        content = self.load_pdf_file(file_path)
                        doc_type = 'pdf'
                    else:
                        content = self.load_text_file(file_path)
                        doc_type = 'text'
                        
                    documents.append({
                        'content': content,
                        'metadata': {
                            'source': str(file_path),
                            'type': doc_type
                        }
                    })
                except Exception as e:
                    print(f"Error loading {file_path}: {str(e)}")
                    
        return documents
