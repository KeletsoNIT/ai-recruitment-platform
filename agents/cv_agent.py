import re


# =========================
# EMAIL EXTRACTION
# =========================
def extract_email(text):
    if not text:
        return None

    # normalize common PDF/text issues
    text = text.replace("(at)", "@").replace(" at ", "@")

    emails = re.findall(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        text
    )

    return emails[0] if emails else None


# =========================
# CV AGENT
# =========================
def cv_agent(cv_text):

    if not cv_text:
        return {
            "skills": [],
            "experience": "N/A",
            "education": "N/A",
            "email": None
        }

    # CLEAN TEXT (VERY IMPORTANT FOR PDF PARSING)
    text = cv_text.replace("\n", " ").lower()

    # =========================
    # EMAIL
    # =========================
    email = extract_email(text)

    # =========================
    # SKILL KEYWORDS
    # =========================
    skill_keywords = [
        # Programming Languages
        "python", "java", "javascript", "typescript", "c++", "c#",

        # Frontend
        "react", "angular", "vue",

        # Backend
        "node.js", "express", "django", "flask", "fastapi",

        # Databases
        "sql", "mysql", "postgresql", "mongodb",

        # Cloud & DevOps
        "docker", "kubernetes", "aws", "azure", "gcp",
        "linux", "git", "github",

        # AI / Data
        "machine learning", "deep learning", "tensorflow",
        "pytorch", "scikit-learn", "pandas", "numpy",
        "nlp", "llm", "langchain", "opencv"
    ]

    skills = []

    for skill in skill_keywords:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            skills.append(skill)

    skills = sorted(set(skills))

    # =========================
    # EXPERIENCE
    # =========================
    experience = "N/A"
    matches = re.findall(r"(\d+)\+?\s*(years|yrs)", text)

    if matches:
        experience = f"{max(int(m[0]) for m in matches)} years experience"

    # =========================
    # EDUCATION
    # =========================
    education = "N/A"

    if "phd" in text:
        education = "PhD"
    elif "master" in text or "msc" in text:
        education = "Master's Degree"
    elif "bachelor" in text or "bsc" in text or "degree" in text:
        education = "Bachelor's Degree"
    elif "diploma" in text:
        education = "Diploma"

    # =========================
    # FINAL OUTPUT
    # =========================
    return {
        "skills": skills,
        "experience": experience,
        "education": education,
        "email": email
    }