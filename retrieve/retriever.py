def retrieve_chunks(vector_store, query):

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    docs = retriever.invoke(query)

    return docs
