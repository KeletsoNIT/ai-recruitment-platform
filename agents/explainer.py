def explain_top_candidate(candidate):

    match = candidate.get("match", {})

    score = match.get("match_score", 0)
    rule_score = match.get("rule_score", 0)
    semantic_score = match.get("semantic_score", 0)

    matched = match.get("matched_skills", [])
    missing = match.get("missing_skills", [])

    role = candidate.get("placement", {}).get("role", "Unknown")
    confidence = candidate.get("placement", {}).get("confidence", "Unknown")

    # =========================
    # DECISION LOGIC EXPLANATION
    # =========================
    if rule_score > semantic_score:
        dominant_signal = "rule-based matching (exact skill alignment)"
    elif semantic_score > rule_score:
        dominant_signal = "semantic AI understanding (skill meaning similarity)"
    else:
        dominant_signal = "balanced rule + semantic evaluation"

    # =========================
    # PERFORMANCE INSIGHT
    # =========================
    if score >= 80:
        performance = "Exceptional match for this role"
    elif score >= 65:
        performance = "Strong candidate with good alignment"
    elif score >= 50:
        performance = "Moderate fit with some gaps"
    else:
        performance = "Weak alignment with job requirements"

    # =========================
    # EXPLANATION BUILD
    # =========================
    explanation = f"""
## 🧠 AI Candidate Explanation (Explainable AI Layer)

### 👤 Candidate
**{candidate.get('candidate_name', 'Unknown')}**

---

## 📊 Final Evaluation

- **Final Score:** {score}%
- **Rule-Based Score:** {rule_score}%
- **Semantic Score:** {semantic_score}%
- **AI Assessment:** {performance}

---

## ⚖️ How the AI Made This Decision

This candidate was evaluated using a **hybrid scoring system**, combining:

- Rule-based skill matching (exact keyword + grouped skills)
- Semantic similarity (AI understanding of skill meaning)

👉 The dominant factor in this decision was:
**{dominant_signal}**

---

## ✅ Strengths Identified
{', '.join(matched) if matched else 'No strong matches detected'}

---

## ❌ Skill Gaps
{', '.join(missing) if missing else 'No major gaps detected'}

---

## 🎯 Hiring Recommendation
This candidate is considered a **{role}** with a confidence level of **{confidence}**.

The AI prioritised:
- Technical skill alignment
- Semantic similarity of experience
- Overall job fit consistency

---

## 🧠 Final AI Insight
{performance}. This recommendation is based on a hybrid AI model that balances strict skill requirements with contextual understanding of candidate experience.
"""

    return explanation