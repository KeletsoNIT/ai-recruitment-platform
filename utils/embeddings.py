from config import GOOGLE_API_KEY
from langchain_google_genai import GoogleGenerativeAIEmbeddings

_embeddings = None

def get_embeddings():
    global _embeddings

    if _embeddings is None:
        if not GOOGLE_API_KEY:
            raise ValueError("Missing GOOGLE_API_KEY")

        _embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",  # fallback safe wrapper mode
            google_api_key=GOOGLE_API_KEY,
            task_type="retrieval_document"
        )

    return _embeddings