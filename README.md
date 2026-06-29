# DocuThinker — Retrieval-Augmented Generation (RAG)

DocuThinker is a lightweight Retrieval-Augmented Generation (RAG) project for local use and rapid prototyping. It provides a Streamlit front-end to upload documents and a FastAPI backend to ingest documents into a Chroma vector store and answer natural-language queries using OpenAI embeddings and LangChain orchestration.

**Key features:**
- Upload and ingest PDF, DOCX, TXT, and CSV files.
- Split documents into chunks and compute embeddings with OpenAI.
- Persist vectors using Chroma (disk-backed) for reuse across sessions.
- Retrieve relevant chunks and generate answers via LangChain + OpenAI.
- Simple Streamlit UI and HTTP API for integrations.

---

**Quick Start**

- Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- Install dependencies:

```powershell
pip install -r requirements.txt
```

- Create a `.env` file in the repository root and set your OpenAI key:

```env
OPENAI_API_KEY=your_api_key_here
DOCUTHINKER_API_URL=http://localhost:8000
```

---

**Run the project**

- Start the FastAPI backend (default port 8000):

```powershell
uvicorn api:app --reload --port 8000
```

- Start the Streamlit UI (optional):

```powershell
streamlit run main.py
```

Open Streamlit at `http://localhost:8501` (or use the API directly).

---

**API Endpoints**

- POST `/ingest` — Ingest files into the vector store.
	- Multipart form with `files` field (one or more files).
	- Returns JSON: `{'status': 'ok', 'chunks_indexed': N}` on success.

- POST `/query` — Query the persisted vector store.
	- JSON body: `{'q': 'your question'}`
	- Returns JSON: `{'answer': <generated answer>, 'results': [{ 'text': ..., 'metadata': {...} }, ...]}`

Example curl (query):

```bash
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"q":"What is in the documents?"}'
```

---

**Project layout**

- `api.py` — FastAPI app exposing `/ingest` and `/query`.
- `main.py` — Streamlit UI that talks to the API.
- `ingest/` — ingestion helpers: loaders, splitter, embeddings, vector store.
- `retrieve/` — retrieval logic, retriever and RAG chain.
- `vector_store/` — persisted Chroma data directory (created at runtime).

---

**Developer notes**

- Vector store persistence: the project uses a `vector_store` directory to persist Chroma data. If you change the persist directory, update calls in `api.py` and `ingest/vector_store.py`.
- Embeddings: `ingest/embeddings.py` constructs the `OpenAIEmbeddings` instance. Adjust the model in that file if needed.
- Chroma compatibility: The code adapts to the installed `langchain_community`/`chromadb` versions; if you see constructor kwarg errors, ensure dependencies are current.

**Troubleshooting**

- If you encounter an error when creating or loading the vector store, check that `chromadb` is installed and that `persist_directory` is writable.
- For OpenAI API issues, confirm `OPENAI_API_KEY` is set and network access is available.

---

If you'd like, I can also add example Python snippets for programmatic ingestion/querying, or a minimal test script to validate the API endpoints quickly.

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key.

```env
OPENAI_API_KEY=your_api_key_here
```

## Run

```powershell
streamlit run main.py
```

Then open the local URL printed by Streamlit, usually `http://localhost:8501`.

Uploaded files are saved under `data/`, which is ignored by Git. Vector search data is kept in memory for the current app session.
