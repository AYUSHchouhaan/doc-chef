from langchain_community.document_loaders import Docx2txtLoader


def load_docx(file_path):
    loader = Docx2txtLoader(file_path)
    documents = loader.load()
    text = ""
    for doc in documents:
        text += doc.page_content
    return text
