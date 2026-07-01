from models.llm import llm


def interview_agent(cv_data, job_data, match_result=None):

    candidate_skills = cv_data.get("skills") or []
    required_skills = job_data.get("required_skills") or []

    matched_skills = []
    missing_skills = []
    match_score = 0

    if match_result:
        matched_skills = match_result.get("matched_skills", [])
        missing_skills = match_result.get("missing_skills", [])
        match_score = match_result.get("match_score", 0)

    focus = job_data.get("focus", "General")
    role = job_data.get("role", "Candidate")

    prompt = f"""
You are a senior technical recruiter.

Generate 8 interview questions.

JOB ROLE: {role}
FOCUS: {focus}
MATCH SCORE: {match_score}

CANDIDATE SKILLS:
{candidate_skills}

MATCHED SKILLS:
{matched_skills}

MISSING SKILLS:
{missing_skills}

Return ONLY numbered questions (1-8).
"""

    try:
        response = llm.invoke(prompt)

        text = response.content.strip()

        questions = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        return {
            "questions": questions,
            "meta": {
                "match_score": match_score,
                "focus": focus,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills
            }
        }

    except Exception:

        return {
            "questions": [
                "Explain your experience with relevant technologies.",
                "Describe a challenging project you worked on.",
                "How do you debug complex systems?",
                "How do you handle pressure?",
                "Tell me about teamwork experience.",
                "How do you learn new technologies?",
                "Describe a difficult bug you solved.",
                "Why are you a good fit for this role?"
            ],
            "meta": {
                "match_score": match_score,
                "focus": focus
            }
        }