from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text = ""
    for doc in documents:
        text += doc.page_content
    return text