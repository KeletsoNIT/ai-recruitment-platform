import re

def _count_keywords(text, keywords):
    return sum(
        1 for kw in keywords
        if re.search(r'\b' + re.escape(kw) + r'\b', text)
    )


def job_agent(job_text):

    job_text_lower = job_text.lower()

    ML_KEYWORDS = [
        "machine learning", "ml", "tensorflow", "pytorch",
        "scikit-learn", "deep learning", "neural network",
        "sql", "data science", "nlp", "data analysis"
    ]

    AGENTIC_AI_KEYWORDS = [
        "agentic", "agent", "ai agent", "llm",
        "langchain", "langgraph", "crewai", "autogen",
        "rag", "vector database", "pinecone", "chromadb"
    ]

    ml_score = _count_keywords(job_text_lower, ML_KEYWORDS)
    agentic_score = _count_keywords(job_text_lower, AGENTIC_AI_KEYWORDS)

    if ml_score > agentic_score:
        role = "Machine Learning Internship"
    elif agentic_score > ml_score:
        role = "Agentic AI Internship"
    else:
        role = "Software Internship"

    SKILL_MAP = {
        "python": "Python",
        "sql": "SQL",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "scikit-learn": "Scikit-Learn",
        "langchain": "LangChain",
        "langgraph": "LangGraph",
        "crewai": "CrewAI",
        "autogen": "AutoGen",
        "llm": "LLM",
        "rag": "RAG",
        "docker": "Docker",
        "aws": "AWS",
        "kubernetes": "Kubernetes",
        "machine learning": "Machine Learning",
        "deep learning": "Deep Learning",
        "nlp": "Natural Language Processing"
    }

    skills = []
    skills_raw = []

    for keyword, label in SKILL_MAP.items():
        if re.search(r"\b" + re.escape(keyword) + r"\b", job_text_lower):
            skills.append(label)
            skills_raw.append(keyword)

    return {
        "role": role,
        "required_skills": skills,          # DISPLAY
        "required_skills_raw": skills_raw,  # MATCHING INPUT (IMPORTANT)
        "ml_score": ml_score,
        "agentic_score": agentic_score
    }