import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_connection
from database.vacancy_repo import (
    save_vacancy,
    get_all_vacancies,
    close_vacancy
)

ADMIN_NAME = "Keletso Kelly Makalela"
ADMIN_EMAIL = "keletsomakalela@icloud.com"
ADMIN_PASSWORD = "admin123"


# =========================
# MODULE 4.3 — SKILL GAP ANALYSIS
# =========================
def compute_skill_gaps(job_description, candidate_texts):

    import re

    job_skills = set(re.findall(r"[a-zA-Z]+", job_description.lower()))

    gaps = []

    for text in candidate_texts:
        candidate_skills = set(re.findall(r"[a-zA-Z]+", str(text).lower()))
        missing = job_skills - candidate_skills
        gaps.append(list(missing))

    return job_skills, gaps


def admin_page():

    st.set_page_config(page_title="Enterprise Admin", layout="wide")
    st.title("🏢 Enterprise Admin Control Center")

    # =========================
    # AUTH
    # =========================
    if "admin_verified" not in st.session_state:
        st.session_state.admin_verified = False

    if not st.session_state.admin_verified:

        st.subheader("🔐 Secure Admin Login")

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login to Admin Panel"):
            if name == ADMIN_NAME and email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                st.session_state.admin_verified = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # SAFE DATA LOADING
    # =========================
    users = cursor.execute("""
        SELECT id, full_name, email, role, created_at FROM users
    """).fetchall()

    # FIX: columns now match the actual SELECT (vacancy_id, not job_description)
    sessions = cursor.execute("""
        SELECT id, user_id, vacancy_id, job_title, created_at
        FROM recruitment_sessions
    """).fetchall()

    candidates = cursor.execute("""
        SELECT id, session_id, candidate_name, cv_filename,
               match_score, recommendation, created_at
        FROM candidates
    """).fetchall()

    vacancies = get_all_vacancies()

    # =========================
    # DATAFRAMES
    # =========================
    users_df = pd.DataFrame(
        users,
        columns=["id", "full_name", "email", "role", "created_at"]
    ) if users else pd.DataFrame()

    # FIX: column names now match the 5 columns returned above
    sessions_df = pd.DataFrame(
        sessions,
        columns=["id", "user_id", "vacancy_id", "job_title", "created_at"]
    ) if sessions else pd.DataFrame()

    candidates_df = pd.DataFrame(
        candidates,
        columns=["id", "session_id", "candidate_name", "cv_filename",
                 "match_score", "recommendation", "created_at"]
    ) if candidates else pd.DataFrame()

    if not candidates_df.empty:
        candidates_df["match_score"] = pd.to_numeric(candidates_df["match_score"], errors="coerce")

    # =========================
    # SIDEBAR
    # =========================
    menu = st.sidebar.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "👥 HR Intelligence",
            "📁 Recruitment Audit",
            "🔍 Search",
            "📈 Analytics",
            "📤 Export",
            "📢 Vacancies",
            "📊 Vacancy Insights"
        ]
    )

    # =========================
    # 📊 DASHBOARD
    # =========================
    if menu == "📊 Dashboard":

        st.header("Executive Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Users", len(users_df))
        col2.metric("Sessions", len(sessions_df))
        col3.metric("Candidates", len(candidates_df))
        col4.metric("Vacancies", len(vacancies))

        avg_score = candidates_df["match_score"].mean() if not candidates_df.empty else 0
        st.metric("Avg Match Score", round(avg_score, 2))

    # =========================
    # 📢 VACANCIES
    # =========================
    elif menu == "📢 Vacancies":

        st.header("Job Vacancy Management")

        with st.form("vacancy_form"):
            title = st.text_input("Job Title")
            department = st.text_input("Department")
            description = st.text_area("Job Description")
            requirements = st.text_area("Required Skills")
            experience = st.text_input("Experience Required")
            closing_date = st.date_input("Closing Date")

            submit = st.form_submit_button("Create Vacancy")

            if submit:
                save_vacancy(
                    title,
                    department,
                    description,
                    requirements,
                    experience,
                    closing_date,
                    st.session_state.user_id
                )
                st.success("Vacancy created successfully!")
                st.rerun()

        st.markdown("---")
        st.subheader("📋 All Vacancies")

        if not vacancies:
            st.info("No vacancies created yet.")
        else:
            for v in vacancies:

                st.markdown(f"### {v[1]}")
                st.write(f"📌 Department: {v[2]}")
                st.write(f"📝 Description: {v[3]}")
                st.write(f"🧠 Requirements: {v[4]}")
                st.write(f"🎯 Experience: {v[5]}")
                st.write(f"📅 Closing Date: {v[6]}")
                st.write(f"📊 Status: {v[7]}")

                if v[7] == "Active":
                    if st.button(f"❌ Close Vacancy {v[0]}", key=f"close_{v[0]}"):
                        close_vacancy(v[0])
                        st.success("Vacancy closed successfully!")
                        st.rerun()

                st.markdown("---")

    # =========================
    # 📊 VACANCY INSIGHTS
    # =========================
    elif menu == "📊 Vacancy Insights":

        st.header("📊 Vacancy Intelligence Dashboard")

        # FIX: JOIN to job_vacancies to get job_description
        sessions_raw = cursor.execute("""
            SELECT rs.id, rs.user_id, rs.job_title, jv.description
            FROM recruitment_sessions rs
            LEFT JOIN job_vacancies jv ON rs.vacancy_id = jv.id
        """).fetchall()

        cand_raw = cursor.execute("""
            SELECT session_id, match_score
            FROM candidates
        """).fetchall()

        if not sessions_raw or not cand_raw:
            st.info("Not enough data yet for insights.")
            st.stop()

        sessions_df = pd.DataFrame(
            sessions_raw,
            columns=["session_id", "user_id", "job_title", "job_description"]
        )

        cand_df = pd.DataFrame(
            cand_raw,
            columns=["session_id", "score"]
        )

        merged = sessions_df.merge(cand_df, on="session_id", how="inner")

        if merged.empty:
            st.info("No matching session-candidate data.")
            st.stop()

        vacancy_stats = merged.groupby("job_title").agg(
            avg_score=("score", "mean"),
            total_candidates=("score", "count")
        ).reset_index()

        st.subheader("📌 Vacancy Performance Overview")
        st.dataframe(vacancy_stats)

        fig = px.bar(
            vacancy_stats,
            x="job_title",
            y="avg_score",
            title="Average Candidate Quality per Job"
        )
        st.plotly_chart(fig, use_container_width=True)

        # =========================
        # 🧠 SKILL GAP ANALYSIS
        # =========================
        st.subheader("🧠 Skill Gap Analysis (Module 4.3)")

        gap_results = []

        for job in vacancy_stats["job_title"]:

            job_data = sessions_df[sessions_df["job_title"] == job]

            if job_data.empty:
                continue

            job_desc = job_data["job_description"].iloc[0]

            # Guard: skip if no description found (vacancy may have been deleted)
            if not job_desc:
                continue

            candidate_scores = merged[merged["job_title"] == job]["score"].tolist()

            job_skills, gaps = compute_skill_gaps(job_desc, candidate_scores)

            avg_gap = sum(len(g) for g in gaps) / len(gaps) if gaps else 0

            gap_results.append({
                "Job Title": job,
                "Required Skills": len(job_skills),
                "Avg Missing Skills": round(avg_gap, 2)
            })

        gap_df = pd.DataFrame(gap_results)

        if gap_df.empty:
            st.info("No skill gap data available.")
        else:
            st.dataframe(gap_df)

            fig2 = px.bar(
                gap_df,
                x="Job Title",
                y="Avg Missing Skills",
                title="Skill Gap Intensity per Vacancy"
            )
            st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # OTHER MODULES
    # =========================
    elif menu == "👥 HR Intelligence":
        st.header("HR Performance Panel")
        st.dataframe(users_df)

    elif menu == "📁 Recruitment Audit":
        st.header("Recruitment History")
        st.dataframe(sessions_df)

    elif menu == "🔍 Search":
        st.header("Global Search")

    elif menu == "📈 Analytics":
        st.header("System Analytics")

    elif menu == "📤 Export":
        st.header("Export Data")