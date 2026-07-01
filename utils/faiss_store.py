import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384
index = faiss.IndexFlatL2(dimension)

candidate_store = []


# =========================
# ADD CANDIDATE
# =========================
def add_candidate(candidate_id, text):

    embedding = _model.encode([text])[0].astype("float32")

    index.add(np.array([embedding]))

    candidate_store.append({
        "id": candidate_id,
        "text": text
    })


# =========================
# SEARCH CANDIDATES
# =========================
def search_candidates(query, top_k=5):

    query_vec = _model.encode([query])[0].astype("float32")

    distances, indices = index.search(
        np.array([query_vec]),
        top_k
    )

    results = []

    for i, idx in enumerate(indices[0]):

        if idx < len(candidate_store):

            results.append({
                "candidate_id": candidate_store[idx]["id"],
                "score": float(1 / (1 + distances[0][i]))
            })

    return results