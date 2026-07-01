import math

def rank_candidates(results_list, shortlist_top_n=None):

    # =========================
    # SCORE EXTRACTION (ROBUST)
    # =========================
    def extract_score(candidate):

        if not isinstance(candidate, dict):
            return 0.0

        match = candidate.get("match", {})

        # NEW: support hybrid scores
        match_score = match.get("match_score", 0)
        semantic_score = match.get("semantic_score", 0)
        rule_score = match.get("rule_score", 0)

        # fallback support
        raw = match_score or semantic_score or rule_score or 0

        if raw is None:
            return 0.0

        if isinstance(raw, str):
            raw = raw.replace("%", "").strip()

        try:
            return float(raw)
        except (ValueError, TypeError):
            return 0.0

    # =========================
    # TIER SYSTEM
    # =========================
    def get_tier(score):
        if score >= 80:
            return "Strong Match"
        elif score >= 65:
            return "Good Match"
        elif score >= 50:
            return "Potential Match"
        else:
            return "Weak Match"

    # =========================
    # EMPTY CHECK
    # =========================
    if not results_list:
        return {
            "ranked_candidates": [],
            "shortlist": [],
            "summary": {
                "total_candidates": 0,
                "average_score": 0,
                "top_candidate": None
            }
        }

    # =========================
    # SORTING
    # =========================
    ranked = sorted(results_list, key=extract_score, reverse=True)

    total = len(ranked)

    # =========================
    # ENRICH CANDIDATES
    # =========================
    for i, candidate in enumerate(ranked):

        score = extract_score(candidate)

        candidate["rank"] = i + 1
        candidate["match_score"] = round(score, 2)
        candidate["tier"] = get_tier(score)

        # percentile ranking
        candidate["percentile"] = round(((total - i) / total) * 100, 2)

        # =========================
        # EXPLAINABILITY (NEW)
        # =========================
        match_data = candidate.get("match", {})

        candidate["ranking_reason"] = {
            "match_score": match_data.get("match_score", 0),
            "rule_score": match_data.get("rule_score", 0),
            "semantic_score": match_data.get("semantic_score", 0),
            "tier": candidate["tier"]
        }

    # =========================
    # SHORTLIST LOGIC
    # =========================
    shortlisted = ranked[:shortlist_top_n] if shortlist_top_n else ranked

    # =========================
    # SAFE AVERAGE CALCULATION
    # =========================
    scores = [extract_score(c) for c in ranked]
    average_score = round(sum(scores) / max(len(scores), 1), 2)

    # =========================
    # SUMMARY
    # =========================
    summary = {
        "total_candidates": total,
        "average_score": average_score,
        "top_candidate": ranked[0] if ranked else None,
        "best_score": ranked[0]["match_score"] if ranked else 0,
        "worst_score": ranked[-1]["match_score"] if ranked else 0
    }

    # =========================
    # FINAL OUTPUT
    # =========================
    return {
        "ranked_candidates": ranked,
        "shortlist": shortlisted,
        "summary": summary
    }