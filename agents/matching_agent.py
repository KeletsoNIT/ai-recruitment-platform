from sentence_transformers import SentenceTransformer
import numpy as np

_model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# SEMANTIC SCORING (FIXED)
# =========================

def semantic_skill_score(candidate_skills, required_skills):

    if not candidate_skills or not required_skills:
        return 0.0

    cv_vectors = _model.encode(candidate_skills)
    jd_vectors = _model.encode(required_skills)

    scores = []

    for jd_vec in jd_vectors:
        # direct dot product similarity (faster + stable)
        sims = np.dot(cv_vectors, jd_vec)

        # convert to numpy array safety
        sims = np.array(sims)

        scores.append(np.max(sims))

    if len(scores) == 0:
        return 0.0

    return round(float(np.mean(scores)) * 100, 2)


# =========================
# SKILL MATCHING AGENT (FIXED)
# =========================

def matching_agent(candidate_skills, required_skills):

    # -------------------------
    # NORMALIZATION
    # -------------------------
    candidate_set = {
        s.strip().lower()
        for s in (candidate_skills or [])
        if isinstance(s, str)
    }

    required_set = {
        s.strip().lower()
        for s in (required_skills or [])
        if isinstance(s, str)
    }

    # -------------------------
    # EDGE CASE
    # -------------------------
    if not required_set:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "recommendation": "No job requirements provided",
            "rule_score": 0,
            "semantic_score": 0
        }

    # -------------------------
    # SKILL GROUPING
    # -------------------------
    skill_groups = {
        "agentic ai": {"langchain", "langgraph", "crewai", "autogen", "agent"},
        "machine learning": {
            "ml", "machine learning", "sklearn", "scikit-learn",
            "deep learning", "tensorflow", "pytorch",
            "nlp", "computer vision", "feature engineering",
            "mlops", "data preprocessing", "sql"
        },
        "llm": {"llm", "gpt", "gemini", "large language model"},
        "rag": {"rag", "vector database", "pinecone", "chromadb"}
    }

    expanded_candidate = set(candidate_set)
    expanded_required = set(required_set)

    # -------------------------
    # EXPAND SKILLS
    # -------------------------
    for skill in candidate_set:
        for group, synonyms in skill_groups.items():
            if skill in synonyms:
                expanded_candidate.add(group)

    for skill in required_set:
        for group, synonyms in skill_groups.items():
            if skill in synonyms:
                expanded_required.add(group)

    # -------------------------
    # RULE MATCHING
    # -------------------------
    matched = expanded_candidate & expanded_required
    missing = expanded_required - expanded_candidate

    rule_score = (len(matched) / len(expanded_required)) * 100

    # -------------------------
    # SEMANTIC SCORE
    # -------------------------
    semantic_score = semantic_skill_score(
        list(candidate_set),
        list(required_set)
    )

    # -------------------------
    # FINAL HYBRID SCORE
    # -------------------------
    match_score = (rule_score * 0.5) + (semantic_score * 0.5)

    # -------------------------
    # RECOMMENDATION
    # -------------------------
    if match_score >= 80:
        recommendation = "Strong Match"
    elif match_score >= 65:
        recommendation = "Good Match"
    elif match_score >= 50:
        recommendation = "Potential Match"
    else:
        recommendation = "Weak Match"

    # -------------------------
    # RETURN
    # -------------------------
    return {
        "match_score": round(match_score, 2),
        "rule_score": round(rule_score, 2),
        "semantic_score": round(semantic_score, 2),
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),
        "recommendation": recommendation
    }