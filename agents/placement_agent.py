from models.llm import llm
import json
import re


def clean_json(text: str):
    text = text.strip()
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    return text[start:end + 1]


def rule_based_placement(skills, focus, match_score):

    skills_lower = [s.lower() for s in skills]

    agentic_keywords = {
        "langchain", "langgraph", "rag", "llm",
        "crewai", "autogen", "agent", "multi-agent",
        "tool calling", "vector database"
    }

    ml_keywords = {
        "machine learning", "deep learning",
        "tensorflow", "pytorch", "scikit-learn",
        "pandas", "numpy", "nlp"
    }

    agentic_score = sum(
        2 for s in skills_lower
        if any(k in s for k in agentic_keywords)
    )

    ml_score = sum(
        2 for s in skills_lower
        if any(k in s for k in ml_keywords)
    )

    # =========================
    # DECISION LOGIC
    # =========================
    if focus == "Agentic AI":

        placement = "Agentic AI Internship"
        confidence = (
            "High" if agentic_score >= 4
            else "Medium" if match_score >= 60
            else "Low"
        )

        reason = f"Strong Agentic AI signals detected ({agentic_score})."

    elif focus == "Machine Learning":

        placement = "Machine Learning Internship"
        confidence = (
            "High" if ml_score >= 4
            else "Medium" if match_score >= 60
            else "Low"
        )

        reason = f"Strong ML signals detected ({ml_score})."

    else:

        if agentic_score > ml_score:
            placement = "Agentic AI Internship"
            confidence = "Medium"
            reason = "Agentic AI skills dominate profile."

        elif ml_score > agentic_score:
            placement = "Machine Learning Internship"
            confidence = "Medium"
            reason = "Machine Learning skills dominate profile."

        else:
            placement = "General AI Internship"
            confidence = "Low"
            reason = "No strong specialization detected."

    return {
        "placement": placement,
        "confidence": confidence,
        "reason": reason,
        "ml_skill_score": ml_score,
        "agentic_skill_score": agentic_score,
        "match_score": match_score
    }


def placement_agent(cv_data, job_data, match_result):

    skills = cv_data.get("skills", [])
    focus = job_data.get("focus", "General")
    match_score = match_result.get("match_score", 0)

    prompt = f"""
You are a hiring decision engine.

Return ONLY JSON:

{{
    "placement": "",
    "confidence": "",
    "reason": ""
}}

JOB FOCUS:
{focus}

MATCH SCORE:
{match_score}

CANDIDATE SKILLS:
{skills}
"""

    try:
        response = llm.invoke(prompt)
        cleaned = clean_json(response.content)

        if not cleaned:
            return rule_based_placement(skills, focus, match_score)

        result = json.loads(cleaned)

        return {
            "placement": result.get("placement"),
            "confidence": result.get("confidence"),
            "reason": result.get("reason"),
            "ml_skill_score": 0,
            "agentic_skill_score": 0,
            "match_score": match_score
        }

    except Exception:
        return rule_based_placement(skills, focus, match_score)