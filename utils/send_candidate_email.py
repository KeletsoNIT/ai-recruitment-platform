from email_sender import send_email

def send_candidate_email(payload, job_title):

    email = payload.get("email")
    name = payload.get("name")
    score = payload.get("score")

    if not email:
        return {"success": False, "message": "Email not found in payload"}

    if score >= 80:
        email_type = "Shortlist"
        subject = f"You've been shortlisted for {job_title}"
        body = f"Hi {name},\n\nYou have been shortlisted.\nScore: {score}"

    elif score >= 50:
        email_type = "Interview"
        subject = f"Interview Invitation - {job_title}"
        body = f"Hi {name},\n\nPlease attend interview.\nScore: {score}"

    else:
        email_type = "Rejection"
        subject = f"Application Update - {job_title}"
        body = f"Hi {name},\n\nThank you for applying.\nScore: {score}"

    result = send_email(email, subject, body)

    result["email_type"] = email_type
    return result