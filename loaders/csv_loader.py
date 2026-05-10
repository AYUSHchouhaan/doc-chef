from langchain_community.document_loaders import CSVLoader

def load_csv(file_path):
    loader = CSVLoader(file_path)
    documents = loader.load()

    text = ""
    
    for doc in documents:
        
        text += doc.page_content + "\n"

    
    return text