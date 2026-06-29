import streamlit as st
import os
import io
import requests
from dotenv import load_dotenv

load_dotenv()

st.title("DocuThinker (UI)")

st.write("Upload your documents to the API-backed service")

# API base URL — change if your API runs on another host/port
API_BASE = st.text_input("API base URL", value=os.getenv("DOCUTHINKER_API_URL", "http://localhost:8000"))

uploaded_files = st.file_uploader("Choose your files", type=["pdf", "docx", "txt", "csv"], accept_multiple_files=True)

if uploaded_files:
    st.write("Files selected:")
    for f in uploaded_files:
        st.write(f"- {f.name} ({f.type}) {f.size} bytes")

    if st.button("Ingest to API"):
        files_payload = []
        for f in uploaded_files:
            content = f.getbuffer().tobytes()
            files_payload.append(("files", (f.name, io.BytesIO(content), f.type or "application/octet-stream")))

        try:
            resp = requests.post(f"{API_BASE}/ingest", files=files_payload, timeout=120)
        except requests.RequestException as e:
            st.error(f"Failed to contact API: {e}")
        else:
            if resp.status_code == 200:
                st.success(f"Ingested: {resp.json().get('chunks_indexed')} chunks indexed")
            else:
                st.error(f"API error ({resp.status_code}): {resp.text}")

query = st.text_input("Ask a question about your uploaded documents")
if query and st.button("Query API"):
    try:
        resp = requests.post(f"{API_BASE}/query", json={"q": query}, timeout=60)
    except requests.RequestException as e:
        st.error(f"Failed to contact API: {e}")
    else:
        if resp.status_code == 200:
            body = resp.json()
            st.subheader("Answer")
            st.write(body.get("answer"))
            st.subheader("Retrieved Chunks")
            for i, r in enumerate(body.get("results", [])):
                meta = r.get("metadata") or {}
                st.write(f"Chunk {i+1} (source: {meta.get('source', 'unknown')}):")
                st.write(r.get("text"))
                st.divider()
        else:
            st.error(f"API error ({resp.status_code}): {resp.text}")

    