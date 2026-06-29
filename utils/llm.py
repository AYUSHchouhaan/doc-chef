from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
def get_llm():
    llm = ChatOpenAI(
        model_name= "gpt-5-mini",
        temperature = 0
    )
    return llm