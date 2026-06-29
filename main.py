import streamlit as st 
import os
from dotenv import load_dotenv
from loaders.docx_loader import load_docx
from loaders.pdf_loader import load_pdf
from loaders.txt_loader import load_txt
from loaders.csv_loader import load_csv
from utils.text_splitter import split_text
from utils.vector_store import create_vector_store
from utils.retriever import retrieve_chunks
from utils.rag_chain import generate_response
load_dotenv()
st.title("DocuThinker")

st.write("Upload your documents")

if not os.getenv("OPENAI_API_KEY"):
    st.warning("Add OPENAI_API_KEY to a .env file before asking questions about documents.")

uploaded_file = st.file_uploader("Choose your file", type=["pdf", "docx", "txt","csv"])

if uploaded_file is not None: 
    st.success("Document uploaded successfully")
    st.write("filename : ",uploaded_file.name)
    st.write("filetype : ",uploaded_file.type)
    st.write("filesize : ",uploaded_file.size, "bytes")
    
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path,"wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File Saved Successfully")

    st.write("Saved Path:", file_path)

    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == "pdf":
        text = load_pdf(file_path)
        st.subheader("Extracted Text")
        chunks = split_text(text)
        
        st.write("Total Chunks : ",len(chunks))
        st.subheader("First Chunk")
        if chunks:
            st.write(chunks[0])
        else:
            st.warning("No text could be extracted from this document.")
            st.stop()
        if not os.getenv("OPENAI_API_KEY"):
            st.stop()
        vector_store = create_vector_store(chunks)
        st.success("Vector Store Created Successfully")
        query = st.text_input("Ask a question about your document")
        if query:
            retrieved_docs = retrieve_chunks(vector_store, query)
            st.subheader("Relevant Chunks:")
            for i,doc in enumerate(retrieved_docs):
                st.write(f"Chunk {i+1}:")
                st.write(doc.page_content)
                st.divider()
            answer = generate_response(query, retrieved_docs)
            st.subheader("Answer")
            st.write(answer)

    elif file_extension == "docx":
        text = load_docx(file_path)
        st.subheader("Extracted Text")
        chunks = split_text(text)
        st.write("Total Chunks : ",len(chunks))
        st.subheader("First Chunk")
        if chunks:
            st.write(chunks[0])
        else:
            st.warning("No text could be extracted from this document.")
            st.stop()
        if not os.getenv("OPENAI_API_KEY"):
            st.stop()
        vector_store = create_vector_store(chunks)
        st.success("Vector Store Created Successfully")
        query = st.text_input("Ask a question about your document")
        if query:
            retrieved_docs = retrieve_chunks(vector_store, query)
            st.subheader("Relevant Chunks:")
            for i,doc in enumerate(retrieved_docs):
                st.write(f"Chunk {i+1}:")
                st.write(doc.page_content)
                st.divider()
            answer = generate_response(query, retrieved_docs)
            st.subheader("Answer")
            st.write(answer)

    elif file_extension == "txt":
        text = load_txt(file_path)
        st.subheader("Extracted Text")
        chunks = split_text(text)
        st.write("Total Chunks : ",len(chunks))
        st.subheader("First Chunk")
        if chunks:
            st.write(chunks[0])
        else:
            st.warning("No text could be extracted from this document.")
            st.stop()
        if not os.getenv("OPENAI_API_KEY"):
            st.stop()
        vector_store = create_vector_store(chunks)
        st.success("Vector Store Created Successfully")
        query = st.text_input("Ask a question about your document")
        if query:
            retrieved_docs = retrieve_chunks(vector_store, query)
            st.subheader("Relevant Chunks:")
            for i,doc in enumerate(retrieved_docs):
                st.write(f"Chunk {i+1}:")
                st.write(doc.page_content)
                st.divider()
            answer = generate_response(query, retrieved_docs)
            st.subheader("Answer")
            st.write(answer)

    elif file_extension == "csv":
        text = load_csv(file_path)
        st.subheader("Extracted Text")
        chunks = split_text(text)
        st.write("Total Chunks : ",len(chunks))
        st.subheader("First Chunk")
        if chunks:
            st.write(chunks[0])
        else:
            st.warning("No text could be extracted from this document.")
            st.stop()
        if not os.getenv("OPENAI_API_KEY"):
            st.stop()
        vector_store = create_vector_store(chunks)
        st.success("Vector Store Created Successfully")
        query = st.text_input("Ask a question about your document")
        if query:
            retrieved_docs = retrieve_chunks(vector_store, query)
            st.subheader("Relevant Chunks:")
            for i,doc in enumerate(retrieved_docs):
                st.write(f"Chunk {i+1}:")
                st.write(doc.page_content)
                st.divider()
            answer = generate_response(query, retrieved_docs)
            st.subheader("Answer")
            st.write(answer)

    