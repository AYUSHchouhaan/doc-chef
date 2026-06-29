# DocuThinker RAG

DocuThinker is a Streamlit app for uploading PDF, DOCX, TXT, and CSV files, splitting their text into chunks, storing embeddings in an in-memory LangChain vector store, and answering questions with OpenAI through LangChain.

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key.

```env
OPENAI_API_KEY=your_api_key_here
```

## Run

```powershell
streamlit run main.py
```

Then open the local URL printed by Streamlit, usually `http://localhost:8501`.

Uploaded files are saved under `data/`, which is ignored by Git. Vector search data is kept in memory for the current app session.
