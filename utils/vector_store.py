from langchain_community.vectorstores import Chroma

from utils.embeddings import get_embedding_model


def create_vector_store(chunks, metadatas=None, persist_directory="vector_store"):
    """Create a Chroma vector store from texts.

    Args:
        chunks (list[str]): list of text chunks
        metadatas (list[dict], optional): per-chunk metadata
        persist_directory (str): directory to persist Chroma DB

    Returns:
        Chroma: a Chroma vector store instance
    """

    embedding_model = get_embedding_model()
    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        metadatas=metadatas,
        persist_directory=persist_directory,
    )

    return vector_store