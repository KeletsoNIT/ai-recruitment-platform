from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
import streamlit as st
from database.vacancy_repo import get_all_vacancies, get_vacancy

from auth.login import login_page
from auth.signup import signup_page


from database.recruitment_repo import save_session, save_candidate

from pages.history import history_page
from pages.analytics import analytics_page
from pages.admin import admin_page

from pipeline import run_pipeline, rank_candidates
from utils.pdf_reader import read_pdf
from agents.explainer import explain_top_candidate
from services.email_dispatcher import send_candidate_email


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Recruitment AI | New Island Technologies",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================
# SIGNATURE ELEMENT: MATCH SIGNAL DIAL
# =========================

def match_dial(score, size=120, stroke=10, label="MATCH SIGNAL"):
    score = max(0, min(100, score))
    r = (size - stroke) / 2
    cx = cy = size / 2
    circumference = 2 * 3.14159265 * r
    offset = circumference * (1 - score / 100)

    if score >= 80:
        color = "var(--teal)"
    elif score >= 60:
        color = "var(--amber)"
    else:
        color = "var(--coral)"

    value_size = round(size * 0.22)
    label_size = max(8, round(size * 0.072))

    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none"
                stroke="var(--border)" stroke-width="{stroke}" />
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none"
                stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"
                stroke-dasharray="{circumference:.2f}"
                stroke-dashoffset="{offset:.2f}"
                transform="rotate(-90 {cx} {cy})"
                style="transition: stroke-dashoffset 0.6s ease;" />
        <text x="{cx}" y="{cy - 2}" text-anchor="middle"
              font-family="'IBM Plex Mono', monospace" font-weight="600"
              font-size="{value_size}" fill="{color}">{score}%</text>
        <text x="{cx}" y="{cy + label_size + 10}" text-anchor="middle"
              font-family="'IBM Plex Mono', monospace" font-weight="500"
              font-size="{label_size}" letter-spacing="1" fill="var(--text-muted)">{label}</text>
    </svg>
    """


def tier_of(score):
    if score >= 80:
        return "STRONG SIGNAL", "teal"
    elif score >= 60:
        return "MODERATE SIGNAL", "amber"
    else:
        return "WEAK SIGNAL", "coral"


# =========================
# GLOBAL THEME / CSS — "Screening Console"
# =========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    --ink: #0A1628;
    --ink-raised: #0F1F3A;
    --ink-card: #13284A;
    --border: #21385F;
    --amber: #FFB020;
    --amber-soft: rgba(255, 176, 32, 0.12);
    --teal: #2DD9C4;
    --teal-soft: rgba(45, 217, 196, 0.12);
    --coral: #FF6B5B;
    --coral-soft: rgba(255, 107, 91, 0.12);
    --text-primary: #EDF1F7;
    --text-muted: #8FA0BD;
    --text-faint: #4F6182;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

.stApp {
    background-color: var(--ink);
    background-image:
        repeating-linear-gradient(0deg, rgba(255,255,255,0.025) 0px, rgba(255,255,255,0.025) 1px, transparent 1px, transparent 48px),
        repeating-linear-gradient(90deg, rgba(255,255,255,0.025) 0px, rgba(255,255,255,0.025) 1px, transparent 1px, transparent 48px);
}

#MainMenu, footer { visibility: hidden; }

h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: var(--text-primary); }

::selection { background: var(--amber-soft); color: var(--amber); }

button:focus-visible, input:focus-visible, textarea:focus-visible {
    outline: 2px solid var(--amber) !important;
    outline-offset: 2px;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: var(--ink-raised);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
}
section[data-testid="stSidebar"] hr { border-color: var(--border); }
section[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: var(--teal-soft) !important;
    border: 1px solid var(--teal) !important;
    border-radius: 8px;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    background: var(--amber);
    color: var(--ink);
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.4px;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: #FFC04D;
    transform: translateY(-1px);
}

.stDownloadButton > button {
    background: transparent;
    color: var(--amber);
    border: 1.5px solid var(--amber);
    border-radius: 8px;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.78rem;
    padding: 0.5rem 1.1rem;
    transition: all 0.15s ease;
}
.stDownloadButton > button:hover {
    background: var(--amber-soft);
}

/* ---------- INPUTS ---------- */
.stTextArea textarea, .stTextInput input {
    background: var(--ink-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 1px var(--amber) !important;
}
.stTextInput label, .stTextArea label, .stRadio label, .stSelectbox label {
    color: var(--text-muted) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ---------- FILE UPLOADER ---------- */
[data-testid="stFileUploaderDropzone"] {
    background: var(--ink-card) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--amber) !important; }
[data-testid="stFileUploaderDropzone"] small, [data-testid="stFileUploaderDropzone"] span {
    color: var(--text-muted) !important;
}

/* ---------- ALERTS ---------- */
[data-testid="stAlert"] {
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
}

/* ---------- EXPANDER ---------- */
.streamlit-expanderHeader, details summary {
    background: var(--ink-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
}
details {
    background: var(--ink-card) !important;
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}

/* ---------- CONSOLE HEADER ---------- */
.console-header {
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 30px 36px;
    margin-bottom: 26px;
    background: linear-gradient(135deg, var(--ink-raised), var(--ink-card));
    position: relative;
    overflow: hidden;
}
.console-header::before {
    content: "";
    position: absolute;
    top: -40%; right: -10%;
    width: 280px; height: 280px;
    background: radial-gradient(circle, var(--amber-soft), transparent 70%);
    pointer-events: none;
}
.console-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 1px;
    color: var(--teal);
    text-transform: uppercase;
    margin-bottom: 14px;
}
.console-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--teal);
    box-shadow: 0 0 0 0 rgba(45,217,196,0.6);
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0% { box-shadow: 0 0 0 0 rgba(45,217,196,0.5); }
    70% { box-shadow: 0 0 0 7px rgba(45,217,196,0); }
    100% { box-shadow: 0 0 0 0 rgba(45,217,196,0); }
}
.console-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.1rem;
    margin: 0;
    color: var(--text-primary);
}
.console-sub {
    color: var(--text-muted);
    font-size: 0.98rem;
    margin-top: 10px;
    max-width: 600px;
    line-height: 1.55;
}

/* ---------- STAGE LABELS ---------- */
.stage-label {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin: 34px 0 16px 0;
}
.stage-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 1.5px;
    color: var(--amber);
    background: var(--amber-soft);
    border: 1px solid rgba(255,176,32,0.35);
    border-radius: 5px;
    padding: 3px 9px;
    white-space: nowrap;
}
.stage-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.15rem;
    color: var(--text-primary);
}

/* ---------- STAT STRIP ---------- */
.stat-strip { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 6px; }
.stat-tile {
    flex: 1; min-width: 160px;
    background: var(--ink-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 18px;
}
.stat-tile .stat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 1px;
    color: var(--text-faint);
    text-transform: uppercase;
}
.stat-tile .stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.5rem;
    color: var(--text-primary);
    margin-top: 4px;
}

/* ---------- DOSSIER CARD (candidate) ---------- */
.dossier-card {
    position: relative;
    background: var(--ink-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px 26px 22px 26px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: wrap;
    transition: border-color 0.15s ease;
}
.dossier-card:hover { border-color: var(--text-faint); }
.dossier-rank {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.4rem;
    color: var(--border);
    line-height: 1;
    min-width: 56px;
}
.dossier-main { flex: 1; min-width: 220px; }
.dossier-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.2rem;
    color: var(--text-primary);
}
.dossier-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 6px;
    display: flex; gap: 16px; flex-wrap: wrap;
}
.tier-chip {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.6px;
    padding: 3px 9px;
    border-radius: 5px;
    margin-top: 10px;
}
.tier-teal { background: var(--teal-soft); color: var(--teal); border: 1px solid rgba(45,217,196,0.35); }
.tier-amber { background: var(--amber-soft); color: var(--amber); border: 1px solid rgba(255,176,32,0.35); }
.tier-coral { background: var(--coral-soft); color: var(--coral); border: 1px solid rgba(255,107,91,0.35); }

/* ---------- BEST CANDIDATE BANNER ---------- */
.flagged-banner {
    background: var(--ink-card);
    border: 1px solid var(--amber);
    box-shadow: 0 0 0 1px rgba(255,176,32,0.15), 0 16px 40px rgba(255,176,32,0.08);
    border-radius: 16px;
    padding: 28px 30px;
    margin: 18px 0 30px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    flex-wrap: wrap;
}
.flagged-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.74rem;
    letter-spacing: 1.5px;
    color: var(--amber);
    text-transform: uppercase;
}
.flagged-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.7rem;
    margin: 6px 0 10px 0;
    color: var(--text-primary);
}
.flagged-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-muted);
    display: flex; gap: 18px; flex-wrap: wrap;
}
.flagged-meta b { color: var(--text-primary); }

/* ---------- SKILL CHIPS ---------- */
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
.chip {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.74rem;
    padding: 4px 10px;
    border-radius: 6px;
}
.chip-match { background: var(--teal-soft); color: var(--teal); border: 1px solid rgba(45,217,196,0.3); }
.chip-missing { background: var(--coral-soft); color: var(--coral); border: 1px solid rgba(255,107,91,0.3); text-decoration: line-through; }

/* ---------- DIVIDER ---------- */
.console-divider {
    border: none; height: 1px;
    background: var(--border);
    margin: 26px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================
# CONSOLE HEADER
# =========================

st.markdown("""
<div class="console-header">
    <div class="console-status"><span class="console-dot"></span> SCREENING ENGINE · ONLINE</div>
    <h1 class="console-title">🛰️ New Island Technologies</h1>
    <div class="console-sub">
        Recruitment AI Console — upload CVs, drop in a role brief, and let the screening
        pipeline parse, match, rank, and prep interview material for every candidate in one pass.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# SESSION STATE INIT
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_role" not in st.session_state:
    st.session_state.user_role = "hr"

if "admin_verified" not in st.session_state:
    st.session_state.admin_verified = False

if "ranked_results" not in st.session_state:
    st.session_state.ranked_results = []


# =========================
# AUTH ROUTING
# =========================

if (
    not st.session_state.logged_in
    and not st.session_state.admin_verified
):

    st.markdown('<div class="stage-label"><span class="stage-tag">ACCESS</span>'
                '<span class="stage-title">Recruitment AI Portal</span></div>',
                unsafe_allow_html=True)

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Sign Up", "Admin"]
    )

    if menu == "Login":
        login_page()

    elif menu == "Sign Up":
        signup_page()

    elif menu == "Admin":

        st.markdown('<div class="stage-label"><span class="stage-tag">ADMIN</span>'
                    '<span class="stage-title">Administrator Login</span></div>',
                    unsafe_allow_html=True)

        name = st.text_input("Full Name", key="admin_name")
        email = st.text_input("Email", key="admin_email")
        password = st.text_input("Password", type="password", key="admin_password")

        if st.button("Access Admin Panel", key="admin_login_btn"):

            if (
                name == "Keletso Kelly Makalela"
                and email == "keletsomakalela@icloud.com"
                and password == "admin123"
            ):
                st.session_state.admin_verified = True
                st.session_state.user_role = "admin"
                st.session_state.user_name = "Administrator"
                st.success("Access Granted")
                st.rerun()

            else:
                st.error("Invalid admin credentials")

    st.stop()


# =========================
# SIDEBAR NAVIGATION
# =========================

if st.session_state.admin_verified:

    st.sidebar.markdown('<div class="console-status"><span class="console-dot"></span> ADMIN SESSION</div>',
                        unsafe_allow_html=True)

    page = st.sidebar.radio("Navigation", ["Admin"])

else:

    st.sidebar.markdown(
        f'<div class="console-status"><span class="console-dot"></span> '
        f'{st.session_state.user_name.upper()} · {st.session_state.user_role.upper()}</div>',
        unsafe_allow_html=True
    )

    page = st.sidebar.radio(
        "Navigation",
        ["Recruitment Tool", "History", "Analytics"]
    )

page = page.strip().lower()


# =========================
# LOGOUT
# =========================

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

if st.sidebar.button("🚪 Log Out"):
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = ""
    st.session_state.user_role = "hr"
    st.session_state.admin_verified = False
    st.session_state.ranked_results = []
    st.rerun()


# =========================
# PAGE ROUTING
# =========================

if page == "history":
    history_page()
    st.stop()

elif page == "analytics":
    analytics_page()
    st.stop()

elif page == "admin":

    if not st.session_state.admin_verified:
        st.error("Admin access denied")
        st.stop()

    st.markdown('<div class="stage-label"><span class="stage-tag">ADMIN</span>'
                '<span class="stage-title">Admin Dashboard</span></div>',
                unsafe_allow_html=True)

    admin_page()
    st.stop()


# =========================
# MAIN RECRUITMENT TOOL
# =========================

st.markdown(
    f'<div class="stage-label"><span class="stage-tag">STAGE 01 · INTAKE</span>'
    f'<span class="stage-title">Welcome back, {st.session_state.user_name}</span></div>',
    unsafe_allow_html=True
)

uploaded_cvs = st.file_uploader(
    "Drop CVs here (PDF only) — multiple files supported",
    type=["pdf"],
    accept_multiple_files=True
)

st.markdown(f"""
<div class="stat-strip">
    <div class="stat-tile">
        <div class="stat-label">CVs Queued</div>
        <div class="stat-value">{len(uploaded_cvs) if uploaded_cvs else 0}</div>
    </div>
    <div class="stat-tile">
        <div class="stat-label">Operator</div>
        <div class="stat-value" style="font-size:1.15rem;">{st.session_state.user_name}</div>
    </div>
    <div class="stat-tile">
        <div class="stat-label">Engine Status</div>
        <div class="stat-value" style="color:var(--teal); font-size:1.15rem;">Online</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="stage-label"><span class="stage-tag">STAGE 02 · ROLE SELECTION</span>'
    '<span class="stage-title">Select Vacancy</span></div>',
    unsafe_allow_html=True
)

vacancies = get_all_vacancies()

if not vacancies:
    st.warning("No active vacancies available. Please ask admin to create one.")
    st.stop()

vacancy_dict = {
    f"{v[1]} ({v[2]})": v[0]
    for v in vacancies
}

selected_vacancy_label = st.selectbox(
    "Choose Job Vacancy",
    list(vacancy_dict.keys())
)

vacancy_id = vacancy_dict[selected_vacancy_label]
vacancy = get_vacancy(vacancy_id)

job_title = vacancy[1]
job_description = vacancy[3]
job_requirements = vacancy[4]
experience_required = vacancy[5]

st.write("")
run_clicked = st.button("▶ Run Screening")


# =========================
# RUN PIPELINE
# =========================

if run_clicked:

    if not uploaded_cvs or not job_description:
        st.warning(
            "Upload at least one CV and paste a job description to run the pipeline."
        )

    else:

        results = []

        session_id = save_session(
            st.session_state.user_id,
            vacancy_id,
            job_title
        )

        with st.spinner("Parsing CVs, matching skills, and ranking candidates..."):

            for cv_file in uploaded_cvs:

                cv_text = read_pdf(cv_file)

                result = run_pipeline(
                    cv_text,
                    f"""
JOB TITLE: {job_title}

DESCRIPTION:
{job_description}

REQUIREMENTS:
{job_requirements}

EXPERIENCE:
{experience_required}
"""
                )

                result["candidate_name"] = cv_file.name
                results.append(result)

        # Rank and store in session state so results survive reruns
        st.session_state.ranked_results = rank_candidates(results)


# =========================
# RESULTS — rendered from session state
# =========================

if st.session_state.ranked_results:

    ranked_results = st.session_state.ranked_results

    st.markdown(
        '<div class="stage-label"><span class="stage-tag">STAGE 03 · RESULTS</span>'
        '<span class="stage-title">Candidate Leaderboard</span></div>',
        unsafe_allow_html=True
    )

    # Save candidates to DB (only when pipeline just ran)
    if run_clicked:
        for candidate in ranked_results:
            save_candidate(
                session_id=session_id,
                candidate_name=candidate["candidate_name"],
                score=candidate["match"]["match_score"],
                recommendation=candidate["placement"].get("role", "N/A")
            )

    # ----- TOP CANDIDATE BANNER -----
    best = ranked_results[0]
    best_score = best["match"]["match_score"]

    col_dial, col_info = st.columns([1, 4])

    with col_dial:
        st.markdown(
            f'<div style="display:flex; justify-content:center;">'
            f'{match_dial(best_score, size=120, stroke=10, label="TOP SIGNAL")}</div>',
            unsafe_allow_html=True
        )

    with col_info:
        st.markdown(f"""
        <div class="flagged-banner" style="margin:0;">
            <div>
                <div class="flagged-eyebrow">🚩 Flagged — Top Match</div>
                <div class="flagged-name">{best['candidate_name']}</div>
                <div class="flagged-meta">
                    <span>ROLE&nbsp;&nbsp;<b>{best['placement'].get('role', 'N/A')}</b></span>
                    <span>CONFIDENCE&nbsp;&nbsp;<b>{best['placement'].get('confidence', 'N/A')}</b></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🧠 Why this candidate is #1 — AI explanation"):
        explanation = explain_top_candidate(best)
        st.markdown(explanation)

    with open(best["pdf_report"], "rb") as pdf_file:
        st.download_button(
            label="DOWNLOAD TOP CANDIDATE REPORT ↓",
            data=pdf_file,
            file_name=f"{best['candidate_name']}_report.pdf",
            mime="application/pdf"
        )

    st.markdown('<hr class="console-divider">', unsafe_allow_html=True)

    # ----- CANDIDATE LEADERBOARD CARDS -----
    for candidate in ranked_results:

        score = candidate["match"]["match_score"]
        tier_label, tier_color = tier_of(score)

        col_card, col_dial2 = st.columns([4, 1])

        with col_card:
            st.markdown(f"""
            <div class="dossier-card" style="margin-bottom:0;">
                <div class="dossier-rank">{candidate['rank']:02d}</div>
                <div class="dossier-main">
                    <div class="dossier-name">{candidate['candidate_name']}</div>
                    <div class="dossier-meta">
                        <span>ROLE: {candidate['placement'].get('role', 'N/A')}</span>
                        <span>CONFIDENCE: {candidate['placement'].get('confidence', 'N/A')}</span>
                    </div>
                    <span class="tier-chip tier-{tier_color}">{tier_label} · {score}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "📧 Send Email",
                key=f"email_{candidate['candidate_name']}"
            ):
                payload = {
                    "name": candidate.get("candidate_name"),
                    "email": candidate.get("email"),
                    "score": score
                }
                st.write("EMAIL DEBUG")
                st.json(payload)
                email_result = send_candidate_email(payload, job_title)
                if email_result["success"]:
                    st.success(f"Email sent → {email_result['email_type']}")
                else:
                    st.error(email_result["message"])

        with col_dial2:
            st.markdown(
                f'<div style="display:flex; justify-content:center; align-items:center; height:100%;">'
                f'{match_dial(score, size=86, stroke=7, label="MATCH")}</div>',
                unsafe_allow_html=True
            )

        with open(candidate["pdf_report"], "rb") as pdf_file:
            st.download_button(
                "DOWNLOAD REPORT ↓",
                data=pdf_file,
                file_name=f"{candidate['candidate_name']}_report.pdf",
                mime="application/pdf",
                key=f"pdf_{candidate['candidate_name']}"
            )

        with st.expander("View full candidate analysis"):

            st.markdown("**Skills Breakdown**")

            matched = candidate["match"].get("matched_skills", [])
            missing = candidate["match"].get("missing_skills", [])

            chips_html = '<div class="chip-row">'
            for skill in matched:
                chips_html += f'<span class="chip chip-match">✓ {skill}</span>'
            for skill in missing:
                chips_html += f'<span class="chip chip-missing">{skill}</span>'
            chips_html += '</div>'

            st.markdown(chips_html, unsafe_allow_html=True)

            st.markdown("**Interview Questions**")

            questions = candidate["interview"].get("questions", [])

            if isinstance(questions, str):
                questions = questions.split("\n")

            for i, q in enumerate(questions, start=1):
                q = q.strip()
                if q:
                    st.markdown(
                        f"<span style='font-family:\"IBM Plex Mono\",monospace; color:var(--amber);'>Q{i:02d}</span> &nbsp;{q}",
                        unsafe_allow_html=True
                    )

            st.markdown("**Placement Reason**")
            st.write(candidate["placement"].get("reason", "N/A"))

        st.markdown('<hr class="console-divider">', unsafe_allow_html=True)