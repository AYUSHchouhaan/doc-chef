from langchain_community.document_loaders import TextLoader


def load_txt(file_path):
    loader = TextLoader(file_path)
    documents = loader.load()
    text = ""
    for doc in documents:
        text += doc.page_content
    return text
