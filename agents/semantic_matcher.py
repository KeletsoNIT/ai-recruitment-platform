from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GOOGLE_API_KEY

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

# =========================
# LAZY EMBEDDINGS
# =========================

_embeddings = None

def get_embeddings():
    global _embeddings

    if _embeddings is None:
        if not GOOGLE_API_KEY:
            raise ValueError("Missing GOOGLE_API_KEY")

        _embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )

    return _embeddings


# =========================
# SEMANTIC MATCH FUNCTION
# =========================

def semantic_match(cv_skills, jd_skills):

    if not cv_skills or not jd_skills:
        return 0

    model = get_embeddings()

    cv_vectors = model.embed_documents(cv_skills)
    jd_vectors = model.embed_documents(jd_skills)

    similarities = []

    for jd_vector in jd_vectors:
        scores = cosine_similarity([jd_vector], cv_vectors)[0]
        similarities.append(max(scores))

    return round(np.mean(similarities) * 100, 2)