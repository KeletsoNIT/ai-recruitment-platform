from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generate_pdf_report(data, filename="candidate_report.pdf"):

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    cv = data.get("cv", {})
    job = data.get("job", {})
    match = data.get("match", {})
    interview = data.get("interview", {})
    placement = data.get("placement", {})

    content.append(Paragraph("AI Recruitment Report", styles["Title"]))
    content.append(Spacer(1, 12))

    # CV SECTION
    content.append(Paragraph("Candidate Skills:", styles["Heading2"]))
    content.append(Paragraph(str(cv.get("skills", [])), styles["Normal"]))
    content.append(Spacer(1, 12))

    # JOB SECTION
    content.append(Paragraph("Job Requirements:", styles["Heading2"]))
    content.append(Paragraph(str(job.get("required_skills_raw", [])), styles["Normal"]))
    content.append(Spacer(1, 12))

    # MATCH SECTION
    content.append(Paragraph("Match Score:", styles["Heading2"]))
    content.append(Paragraph(str(match.get("match_score", 0)), styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Matched Skills:", styles["Heading3"]))
    content.append(Paragraph(str(match.get("matched_skills", [])), styles["Normal"]))

    content.append(Paragraph("Missing Skills:", styles["Heading3"]))
    content.append(Paragraph(str(match.get("missing_skills", [])), styles["Normal"]))

    content.append(Spacer(1, 12))

    # INTERVIEW
    content.append(Paragraph("Interview Feedback:", styles["Heading2"]))
    content.append(Paragraph(str(interview), styles["Normal"]))

    # PLACEMENT
    content.append(Paragraph("Placement Recommendation:", styles["Heading2"]))
    content.append(Paragraph(str(placement), styles["Normal"]))

    doc.build(content)

    return filename