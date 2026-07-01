from config import GOOGLE_API_KEY
from langchain_google_genai import GoogleGenerativeAIEmbeddings

_embeddings = None

def get_embeddings():
    global _embeddings

    if _embeddings is None:
        if not GOOGLE_API_KEY:
            raise ValueError("Missing GOOGLE_API_KEY in config")

        _embeddings = GoogleGenerativeAIEmbeddings(
            model="text-embedding-004",
            google_api_key=GOOGLE_API_KEY
        )

    return _embeddings