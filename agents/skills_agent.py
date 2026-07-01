from semantic_matcher import semantic_match

# =========================
# SKILLS AGENT
# =========================

def skills_agent(candidate_skills, required_skills):

    # -------------------------
    # NORMALIZATION
    # -------------------------
    candidate = {
        s.strip().lower()
        for s in (candidate_skills or [])
        if isinstance(s, str)
    }

    required = {
        s.strip().lower()
        for s in (required_skills or [])
        if isinstance(s, str)
    }

    # -------------------------
    # EDGE CASE
    # -------------------------
    if not required:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "match_ratio": 0,
            "semantic_score": 0,
            "rule_score": 0,
            "final_score": 0,
            "summary": "No required skills provided"
        }

    # -------------------------
    # DOMAIN INTELLIGENCE
    # -------------------------
    skill_groups = {
        "agentic ai": {"langchain", "langgraph", "crewai", "autogen"},
        "machine learning": {
            "ml", "machine learning", "sklearn", "scikit-learn",
            "deep learning", "tensorflow", "pytorch", "nlp",
            "computer vision", "feature engineering", "mlops"
        },
        "llm": {"llm", "gpt", "gemini", "large language model"},
        "rag": {"rag", "vector database", "pinecone", "chromadb"},
        "database": {"sql", "postgresql", "mysql", "mongodb"},
        "cloud": {"aws", "azure", "gcp", "cloud"}
    }

    expanded_candidate = set(candidate)
    expanded_required = set(required)

    # Expand candidate skills
    for skill in candidate:
        for group, synonyms in skill_groups.items():
            if skill in synonyms:
                expanded_candidate.add(group)

    # Expand required skills
    for skill in required:
        for group, synonyms in skill_groups.items():
            if skill in synonyms:
                expanded_required.add(group)

    # -------------------------
    # RULE-BASED MATCHING
    # -------------------------
    matched = expanded_candidate & expanded_required
    missing = expanded_required - expanded_candidate

    rule_score = (len(matched) / len(expanded_required)) * 100

    # -------------------------
    # SEMANTIC MATCHING
    # -------------------------
    semantic_score = semantic_match(list(candidate), list(required))

    # -------------------------
    # FINAL HYBRID SCORE
    # -------------------------
    final_score = (rule_score * 0.5) + (semantic_score * 0.5)

    # -------------------------
    # OUTPUT
    # -------------------------
    return {
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),

        "match_ratio": round(rule_score, 2),
        "rule_score": round(rule_score, 2),
        "semantic_score": round(semantic_score, 2),
        "final_score": round(final_score, 2),

        "summary": f"{len(matched)}/{len(expanded_required)} skills matched"
    }