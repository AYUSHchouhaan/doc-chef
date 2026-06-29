from retrieve.llm import get_llm


def generate_response(query, retrieved_docs):
    llm = get_llm()
    context = ""
    for doc in retrieved_docs:
        context += doc.page_content + "\n\n"
    prompt = f"""
    Answer the question using ONLY the provided context.
    Context:{context}
    Question:{query}
    """
    response = llm.invoke(prompt)

    return response.content
