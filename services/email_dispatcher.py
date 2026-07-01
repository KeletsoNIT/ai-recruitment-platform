from services.email_service import send_email
from services.email_templates import load_template


def decide_email_type(score):
    if score >= 85:
        return "interview"
    elif score >= 70:
        return "shortlisted"
    else:
        return "rejection"


def send_candidate_email(candidate, job_title):

    # SAFE EXTRACTION (VERY IMPORTANT)
    name = candidate.get("name")
    email = candidate.get("email")
    score = candidate.get("score", 0)

    print("DISPATCHER DEBUG:", candidate)

    if not email:
        return {
            "success": False,
            "message": "Missing email address",
            "email_type": None
        }

    email_type = decide_email_type(score)

    body = load_template(email_type, {
        "name": name,
        "job_title": job_title
    })

    if email_type == "interview":
        subject = f"Interview Invitation - {job_title}"
    elif email_type == "shortlisted":
        subject = f"Shortlisted - {job_title}"
    else:
        subject = f"Application Update - {job_title}"

    success, message = send_email(email, subject, body)

    return {
        "success": success,
        "message": message,
        "email_type": email_type
    }