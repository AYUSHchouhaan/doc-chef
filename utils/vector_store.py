from langchain_core.vectorstores import InMemoryVectorStore

from utils.embeddings import get_embedding_model


def create_vector_store(chunks, metadatas=None):

    embedding_model = get_embedding_model()
    # InMemoryVectorStore.from_texts supports an optional `metadatas` list
    vector_store = InMemoryVectorStore.from_texts(
        texts=chunks,
        embedding=embedding_model,
        metadatas=metadatas,
    )
    return vector_store