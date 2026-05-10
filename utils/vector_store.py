from langchain_community.vectorstores import Chroma

from utils.embeddings import get_embedding_model


def create_vector_store(chunks):

    embedding_model = get_embedding_model()
    vector_store = Chroma.from_texts(

        texts=chunks,

        embedding=embedding_model,

        persist_directory="vector_store"
    )
    return vector_store