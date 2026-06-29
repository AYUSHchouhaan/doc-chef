import streamlit as st 
import os
from dotenv import load_dotenv
from ingest.loaders.docx_loader import load_docx
from ingest.loaders.pdf_loader import load_pdf
from ingest.loaders.txt_loader import load_txt
from ingest.loaders.csv_loader import load_csv
from ingest.text_splitter import split_text
from ingest.vector_store import create_vector_store
from retrieve.retriever import retrieve_chunks
from retrieve.rag_chain import generate_response
load_dotenv()
st.title("DocuThinker")

st.write("Upload your documents")

if not os.getenv("OPENAI_API_KEY"):
    st.warning("Add OPENAI_API_KEY to a .env file before asking questions about documents.")

uploaded_files = st.file_uploader("Choose your files", type=["pdf", "docx", "txt","csv"], accept_multiple_files=True)

if uploaded_files:
    # aggregate chunks and metadata from all uploaded files
    all_chunks = []
    all_metadatas = []
    file_chunk_counts = {}

    for uploaded_file in uploaded_files:
        st.success(f"Document uploaded successfully: {uploaded_file.name}")
        st.write("filename : ", uploaded_file.name)
        st.write("filetype : ", uploaded_file.type)
        st.write("filesize : ", uploaded_file.size, "bytes")

        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path,"wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Saved {uploaded_file.name} to data/")

        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension == "pdf":
            text = load_pdf(file_path)
        elif file_extension == "docx":
            text = load_docx(file_path)
        elif file_extension == "txt":
            text = load_txt(file_path)
        elif file_extension == "csv":
            text = load_csv(file_path)
        else:
            st.warning(f"Unsupported file type: {file_extension}")
            continue

        chunks = split_text(text)
        file_chunk_counts[uploaded_file.name] = len(chunks)

        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({"source": uploaded_file.name, "chunk_id": i})

    total_chunks = len(all_chunks)
    st.write("Total Chunks across uploads:", total_chunks)
    for fname, cnt in file_chunk_counts.items():
        st.write(f"{fname}: {cnt} chunks")

    if total_chunks == 0:
        st.warning("No extractable text found in the uploaded files.")
        st.stop()

    if not os.getenv("OPENAI_API_KEY"):
        st.warning("OpenAI API key missing; add OPENAI_API_KEY to .env to enable Q&A.")
        st.stop()

    vector_store = create_vector_store(all_chunks, metadatas=all_metadatas)
    st.success("Vector Store Created Successfully")

    query = st.text_input("Ask a question about your uploaded documents")
    if query:
        retrieved_docs = retrieve_chunks(vector_store, query)
        st.subheader("Relevant Chunks:")
        for i, doc in enumerate(retrieved_docs):
            st.write(f"Chunk {i+1} (source: {doc.metadata.get('source', 'unknown')}):")
            st.write(doc.page_content)
            st.divider()
        answer = generate_response(query, retrieved_docs)
        st.subheader("Answer")
        st.write(answer)

    