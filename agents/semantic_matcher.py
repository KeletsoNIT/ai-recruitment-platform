from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

_model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_match(cv_skills, jd_skills):

    if not cv_skills or not jd_skills:
        return 0

    cv_vectors = _model.encode(cv_skills)
    jd_vectors = _model.encode(jd_skills)

    similarities = []

    for jd_vec in jd_vectors:
        scores = cosine_similarity([jd_vec], cv_vectors)[0]
        similarities.append(max(scores))

    return round(np.mean(similarities) * 100, 2)