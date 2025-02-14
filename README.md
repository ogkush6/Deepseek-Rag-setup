# RAG Project

A Retrieval-Augmented Generation (RAG) implementation with both standalone and client-server versions.

## Project Versions

### v0.0 - Standalone Version

```
rag_project/
├── data/
│   ├── documents/          # Place your documents here
│   └── vectors/           # Generated embeddings will be stored here
├── src/
│   ├── __init__.py
│   ├── document_loader.py  # Document loading utilities
│   ├── embeddings.py       # Vector embedding generation
│   ├── rag_engine.py       # Main RAG implementation
│   └── utils.py           # Helper functions
├── requirements.txt
└── main.py
```

### v0.1 - Full Stack Version

```
rag-project/                      # Root project directory
├── backend/                     # Backend RAG system
│   ├── data/
│   │   ├── documents/          # Place your documents here
│   │   └── vectors/           # Generated embeddings stored here
│   ├── src/
│   │   ├── __init__.py
│   │   ├── document_loader.py  # Document loading utilities
│   │   ├── embeddings.py       # Vector embedding generation
│   │   ├── rag_engine.py       # Main RAG implementation
│   │   └── utils.py           # Helper functions
│   ├── requirements.txt        # Python dependencies
│   └── main.py                # FastAPI backend server
│
└── frontend/                   # React frontend application
    ├── public/
    │   ├── favicon.ico
    │   ├── index.html
    │   ├── manifest.json
    │   └── robots.txt
    ├── src/
    │   ├── components/
    │   │   └── RAGChatbot.js  # Main chatbot component
    │   ├── App.js             # Root React component
    │   ├── index.js           # React entry point
    │   ├── index.css          # Global styles including Tailwind
    │   └── App.css            # App-specific styles
    ├── package.json           # Node.js dependencies
    ├── tailwind.config.js     # Tailwind CSS configuration
    └── postcss.config.js      # PostCSS configuration
```

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