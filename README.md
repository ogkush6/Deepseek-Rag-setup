# RAG Project

A Retrieval-Augmented Generation (RAG) implementation with both standalone and client-server versions.

## Project Versions

### v0.2 - Streamlined Version

```
rag-chat/
├── backend/
│   ├── requirements.txt
│   ├── main.py
│   └── src/
│       ├── __init__.py
│       ├── document_loader.py
│       ├── embeddings.py
│       └── rag_engine.py
├── frontend/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx
│       ├── index.css
│       └── main.jsx
└── README.md
```

## Installation

### 1. Clone the repository
```bash
git clone <url>
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```
## Components

### Backend
- Document loading and processing
- Vector embedding generation
- RAG implementation
- FastAPI server (v0.1+)

### Frontend (v0.1+)
- React-based user interface
- Chatbot component
- Tailwind CSS styling

## Start Model
ollama serve

## Start the frontend
cd frontend
npm install  # If you haven't installed dependencies yet
npm run dev

## Start the backend
cd backend
python main.py