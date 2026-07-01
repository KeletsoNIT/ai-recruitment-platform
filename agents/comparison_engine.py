def compare_candidates(candidate_a, candidate_b):

    def get_scores(candidate):
        match = candidate.get("match", {})

        return {
            "name": candidate.get("candidate_name", "Unknown"),
            "final_score": match.get("match_score", 0),
            "rule_score": match.get("rule_score", 0),
            "semantic_score": match.get("semantic_score", 0),
            "matched_skills": set(match.get("matched_skills", [])),
            "missing_skills": set(match.get("missing_skills", [])),
            "role": candidate.get("placement", {}).get("role", "Unknown"),
            "confidence": candidate.get("placement", {}).get("confidence", "Unknown"),
        }

    a = get_scores(candidate_a)
    b = get_scores(candidate_b)

    # =========================
    # SCORE DIFFERENCE
    # =========================
    score_diff = a["final_score"] - b["final_score"]

    # =========================
    # SKILL OVERLAP ANALYSIS
    # =========================
    a_strength = len(a["matched_skills"])
    b_strength = len(b["matched_skills"])

    a_missing = len(a["missing_skills"])
    b_missing = len(b["missing_skills"])

    # =========================
    # WINNER DECISION
    # =========================
    if a["final_score"] > b["final_score"]:
        winner = a["name"]
    elif b["final_score"] > a["final_score"]:
        winner = b["name"]
    else:
        winner = "Tie"

    # =========================
    # AI REASONING BUILD
    # =========================
    explanation = f"""
## ⚖️ AI Candidate Comparison Report

### 🥇 Candidate A: {a['name']}
- Final Score: {a['final_score']}%
- Rule Score: {a['rule_score']}%
- Semantic Score: {a['semantic_score']}%
- Matched Skills: {', '.join(a['matched_skills']) if a['matched_skills'] else 'None'}
- Missing Skills: {', '.join(a['missing_skills']) if a['missing_skills'] else 'None'}

---

### 🥈 Candidate B: {b['name']}
- Final Score: {b['final_score']}%
- Rule Score: {b['rule_score']}%
- Semantic Score: {b['semantic_score']}%
- Matched Skills: {', '.join(b['matched_skills']) if b['matched_skills'] else 'None'}
- Missing Skills: {', '.join(b['missing_skills']) if b['missing_skills'] else 'None'}

---

## 📊 Key Differences

- Score Difference: {round(score_diff, 2)}%
- Skill Advantage:
  - A matched {a_strength} skills
  - B matched {b_strength} skills

- Skill Gaps:
  - A missing {a_missing} skills
  - B missing {b_missing} skills

---

## 🧠 AI Decision

🏆 **Recommended Candidate: {winner}**

"""

    if winner == "Tie":
        explanation += "Both candidates are equally strong. Recommend human review."

    elif winner == a["name"]:
        explanation += f"{a['name']} performs better due to stronger overall alignment and skill coverage."

    else:
        explanation += f"{b['name']} performs better due to stronger overall alignment and skill coverage."

    return {
        "winner": winner,
        "score_difference": round(score_diff, 2),
        "analysis": explanation
    }