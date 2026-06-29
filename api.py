from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from ingest.text_splitter import split_text
from ingest.vector_store import create_vector_store
from ingest.loaders.csv_loader import load_csv
from ingest.loaders.docx_loader import load_docx
from ingest.loaders.pdf_loader import load_pdf
from ingest.loaders.txt_loader import load_txt
from ingest.embeddings import get_embedding_model
from retrieve.retriever import retrieve_chunks
from retrieve.rag_chain import generate_response
from langchain_community.vectorstores import Chroma

app = FastAPI(title="DocuThinker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _ensure_data_dir():
    os.makedirs("data", exist_ok=True)


def _get_vector_store(persist_directory: str = "vector_store"):
    """Load an existing Chroma store or return None if not present."""
    embedding = get_embedding_model()
    if os.path.exists(persist_directory):
        # load existing
        return Chroma(persist_directory=persist_directory, embedding_function=embedding)
    return None


@app.post("/ingest")
async def ingest_files(files: List[UploadFile] = File(...)):
    """Ingest uploaded files into the persistent Chroma vector store."""
    _ensure_data_dir()
    all_chunks = []
    all_metadatas = []

    for uploaded in files:
        filename = uploaded.filename
        file_ext = filename.split(".")[-1].lower()
        file_path = os.path.join("data", filename)
        with open(file_path, "wb") as f:
            f.write(await uploaded.read())

        if file_ext == "pdf":
            text = load_pdf(file_path)
        elif file_ext == "docx":
            text = load_docx(file_path)
        elif file_ext == "txt":
            text = load_txt(file_path)
        elif file_ext == "csv":
            text = load_csv(file_path)
        else:
            continue

        chunks = split_text(text)
        for i, c in enumerate(chunks):
            all_chunks.append(c)
            all_metadatas.append({"source": filename, "chunk_id": i})

    if not all_chunks:
        raise HTTPException(status_code=400, detail="No text extracted from uploaded files")

    store = create_vector_store(all_chunks, metadatas=all_metadatas, persist_directory="vector_store")
    return {"status": "ok", "chunks_indexed": len(all_chunks)}


class QueryRequest(BaseModel):
    q: str


@app.post("/query")
async def query_docs(payload: QueryRequest):
    """Query the persisted vector store and return retrieved chunks and an answer.

    Accepts JSON body: {"q": "your question"}
    """
    q = payload.q

    store = _get_vector_store("vector_store")
    if store is None:
        raise HTTPException(status_code=404, detail="Vector store not found. Ingest files first.")

    docs = retrieve_chunks(store, q)

    answer = generate_response(q, docs)
    results = []
    for doc in docs:
        results.append({"text": doc.page_content, "metadata": doc.metadata})

    return {"answer": answer, "results": results}
