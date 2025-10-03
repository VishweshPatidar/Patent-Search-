# Technical Document Search Platform

A full-stack semantic search system for technical documents using real data from OpenAlex (research papers) and PatentsView (patents) APIs with Milvus vector database.

## Features
- **Semantic Search**: Uses Sentence Transformers for intelligent document matching
- **Vector Database**: Milvus for high-performance vector storage and retrieval
- **Real Data Sources**: OpenAlex API (research papers)
- **FastAPI Backend**: RESTful API with `/search` endpoint
- **Nuxt 3 Frontend**: Modern Vue.js interface with Tailwind CSS

## Quick Start (Windows)

### 🚀 One-Click Setup
```bash
# Run this once to set up everything
setup_project.bat
```

### 🎯 Start the Application
```bash
# Option 1: Start both services at once
start_all.bat

# Option 2: Start services separately
start_backend.bat    # Terminal 1
start_frontend.bat   # Terminal 2
```

### 🌐 Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

## Manual Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker + Docker Compose

### Backend Setup
```bash
# Start Milvus
docker-compose up -d

# Setup Python backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python real_data_integration.py
python data_loader.py
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Project Structure
```
SearchPatent/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── embeddings.py          # Sentence Transformers
│   ├── milvus_client.py       # Milvus vector database
│   ├── data_loader.py         # Data ingestion
│   ├── create_large_datasets.py
│   └── requirements.txt
├── frontend/
│   ├── pages/index.vue        # Search interface
│   ├── components/ResultsList.vue
│   └── package.json
├── data/
│   ├── real_data_combined.csv # Combined real data from APIs
│   ├── real_papers.csv        # OpenAlex research papers
│   └── real_patents.csv       # PatentsView patents
├── docker-compose.yml         # Milvus setup
├── setup_project.bat          # One-time setup
├── start_all.bat              # Start both services
├── start_backend.bat          # Backend only
└── start_frontend.bat         # Frontend only
```

## Search Examples
Try these queries in the search interface:
- "machine learning algorithms"
- "quantum computing applications" 
- "medical diagnosis systems"
- "renewable energy technology"
- "cybersecurity protection"

## Dataset Information
- **Data Sources**: Real APIs (OpenAlex + PatentsView)
- **Research Papers**: OpenAlex API (up to 10,000 papers)
- **Patents**: PatentsView API (up to 15,000 patents)
- **Vector Dimensions**: 384 (all-MiniLM-L6-v2)
- **Search Results**: Top 50 semantic matches with duplicate filtering

## Troubleshooting
- **Port conflicts**: Services use ports 3000 (frontend), 8000 (backend), 19530 (Milvus)
- **Docker issues**: Ensure Docker Desktop is running before setup
- **Memory usage**: Large dataset requires ~2GB RAM for embeddings
- **First run**: Initial setup downloads ML models (~500MB)
- **Milvus connection**: Wait 15 seconds after `docker-compose up -d` before loading data
