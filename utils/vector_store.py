from langchain_core.vectorstores import InMemoryVectorStore

from utils.embeddings import get_embedding_model


def create_vector_store(chunks):

    embedding_model = get_embedding_model()
    vector_store = InMemoryVectorStore.from_texts(

        texts=chunks,

        embedding=embedding_model
    )
    return vector_store