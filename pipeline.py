from agents.cv_agent import cv_agent
from agents.job_agent import job_agent
from agents.matching_agent import matching_agent
from agents.interview_agent import interview_agent
from agents.placement_agent import placement_agent
from report_generator import generate_pdf_report

from utils.faiss_store import add_candidate, search_candidates

import re


# =========================
# EMAIL EXTRACTION (ROBUST)
# =========================
def extract_email(text):
    if not text:
        return None

    emails = re.findall(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        text
    )
    return emails[0] if emails else None


# =========================
# SINGLE PIPELINE (ONE CV)
# =========================
def run_pipeline(cv_text, job_text):

    cv_data = cv_agent(cv_text)
    job_data = job_agent(job_text)

    if not cv_data or not job_data:
        return {
            "error": "Failed in parsing stage",
            "cv": cv_data,
            "job": job_data
        }

    # -------------------------
    # EMAIL FIX (CRITICAL)
    # -------------------------
    email = cv_data.get("email")
    if not email:
        email = extract_email(cv_text)

    # -------------------------
    # NORMALIZE SKILLS
    # -------------------------
    cv_skills = [s.lower().strip() for s in cv_data.get("skills", [])]
    job_skills = job_data.get("required_skills_raw", [])

    # -------------------------
    # MATCHING
    # -------------------------
    match_result = matching_agent(cv_skills, job_skills)
    match_score = match_result.get("match_score", 0)

    # -------------------------
    # STORE IN FAISS
    # -------------------------
    add_candidate(
        candidate_id=cv_data.get("name", "unknown"),
        text=cv_text
    )

    # -------------------------
    # INTERVIEW + PLACEMENT
    # -------------------------
    interview_result = interview_agent(
        cv_data,
        job_data,
        match_result
    )

    placement_result = placement_agent(
        cv_data,
        job_data,
        match_result
    )

    # -------------------------
    # FINAL RESULT (FIXED)
    # -------------------------
    result = {
        "cv": cv_data,
        "job": job_data,
        "match": match_result,
        "interview": interview_result,
        "placement": placement_result,

        "candidate_name": cv_data.get("name", "unknown"),

        # FIX: consistent scoring
        "match_score": match_score,

        # FIX: guaranteed email
        "email": email
    }

    result["pdf_report"] = generate_pdf_report(result)

    return result


# =========================
# MULTI PIPELINE (FAISS POWERED)
# =========================
def run_multi_pipeline(cv_texts, job_text):

    results = []

    # STEP 1: PROCESS CVs
    for i, cv_text in enumerate(cv_texts):

        result = run_pipeline(cv_text, job_text)

        if "error" in result:
            continue

        result["candidate_id"] = i + 1
        results.append(result)

    # STEP 2: FAISS SEARCH
    top_matches = search_candidates(job_text, top_k=10)

    # STEP 3: FAISS SCORE ATTACHMENT
    for candidate in results:
        candidate_name = candidate.get("candidate_name")

        faiss_score = next(
            (c["score"] for c in top_matches if c["candidate_id"] == candidate_name),
            0
        )

        candidate["faiss_score"] = faiss_score

    # STEP 4: HYBRID RANKING
    ranked = sorted(
        results,
        key=lambda x: (
            x.get("match_score", 0) * 0.7 +
            x.get("faiss_score", 0) * 0.3
        ),
        reverse=True
    )

    # STEP 5: RANK ASSIGNMENT
    for i, candidate in enumerate(ranked):
        candidate["rank"] = i + 1

    return ranked


# =========================
# LEGACY RANKING
# =========================
def rank_candidates(results_list):

    ranked = sorted(
        results_list,
        key=lambda x: x.get("match", {}).get("match_score", 0),
        reverse=True
    )

    for i, candidate in enumerate(ranked):
        candidate["rank"] = i + 1

    return ranked