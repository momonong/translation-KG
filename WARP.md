# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview
Translation-KG is a bilingual knowledge graph-powered translation system that combines:
- **Knowledge Graph**: Built from ConceptNet data to provide contextual relationships between terms
- **AI Translation**: Context-aware translation using Google's Gemini LLM with web search grounding
- **PDF Processing**: Upload, view, and process PDF documents for translation
- **FastAPI Backend**: RESTful API serving knowledge graph queries and translation services

## Architecture

### Core Components
- **Knowledge Graph Engine**: NetworkX-based multilingual graph (`/c/en/` and `/c/zh/` nodes)
- **Translation Pipeline**: Gemini 2.5 Flash with Google Search grounding for context-aware translations
- **PDF Management**: File upload/download with temporary storage and automatic cleanup
- **API Layer**: FastAPI with CORS-enabled endpoints for browser extension integration

### Data Flow
1. **Graph Building**: CSV → NetworkX MultiDiGraph → JSONL serialization
2. **Translation**: Text + Context → Language Detection → Gemini LLM → HTML-formatted response
3. **Knowledge Queries**: Term → Graph traversal → Related terms with weights and relationships

## Development Commands

### Environment Setup
```bash
# Install dependencies using Poetry (requires Python 3.11-3.12)
poetry install

# Download required spaCy model
poetry run python -m spacy download en_core_web_sm
```

### Data Pipeline
```bash
# Build knowledge graph from ConceptNet data
poetry run python -m scripts.csv_filter     # Filter CSV data
poetry run python -m scripts.build_graph    # Build NetworkX graph
poetry run python -m scripts.export_graph   # Export to JSONL format
```

### Development Server
```bash
# Run development server with auto-reload
poetry run uvicorn api.main:app --reload

# Production server (Docker)
docker build --platform linux/amd64 -t lexilight:latest .
```

### Testing & Development
```bash
# Test knowledge graph functionality
poetry run python scripts/build_graph.py

# Test translation with sample cases
poetry run python tools/translate_llm.py

# Check data integrity
poetry run python tests/csv_check.py
```

## Key Configuration

### Environment Variables
Create `.env` file with:
- `GEMINI_API_KEY`: Google Gemini API key for translation services

### Data Requirements
- `data/conceptnet_filtered.csv`: Preprocessed ConceptNet relations
- `data/graph_data.jsonl`: Serialized knowledge graph for fast loading

## API Endpoints Structure
- `/api/translate`: Context-aware translation (POST)
- `/api/keywords`: Extract keywords from text (GET)
- `/api/related_terms`: Find related terms in knowledge graph (GET)
- `/api/graph`: Graph visualization data (GET)
- `/api/upload_pdf`: PDF file upload (POST)
- `/api/view_pdf`: PDF viewer interface (GET)
- `/api/download_pdf`: PDF file download (GET)

## Browser Extension Integration
The API is configured with permissive CORS for Chrome extension integration, supporting cross-origin requests from extension contexts.

## Data Management
- PDF files are automatically cleaned up using cron job: `0 4 * * * cd /your/project/path && python -c "from routers.pdf_manage import clean_old_pdfs; clean_old_pdfs(2)"`
- Knowledge graph data is loaded once at startup for performance
- Chinese text processing includes Simplified-to-Traditional conversion using OpenCC
