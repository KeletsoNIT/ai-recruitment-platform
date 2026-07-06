import streamlit as st

from database.recruitment_repo import (
    get_user_sessions,
    get_session_candidates
)

# =========================
# HISTORY PAGE
# =========================

def history_page():

    st.title("📊 Recruitment History")
    st.caption("View all previous recruitment sessions and candidate evaluations.")

    user_id = st.session_state.user_id
    sessions = get_user_sessions(user_id)

    if not sessions:
        st.info("No recruitment history available yet.")
        return

    for session in sessions:

        with st.expander(f"🧾 {session['title']}"):

            # =========================
            # Vacancy Information
            # =========================
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Job Title", session["title"])
                st.metric("Department", session["department"])

            with col2:
                st.metric("Status", session["status"])
                st.metric("Date", session["created_at"])

            st.divider()

            # =========================
            # Candidate Results
            # =========================
            candidates = get_session_candidates(session["id"])

            if not candidates:
                st.info("No candidates were evaluated for this recruitment session.")
                continue

            st.subheader("🏆 Candidate Rankings")

            for index, candidate in enumerate(candidates, start=1):

                score = candidate["match_score"]

                if score >= 80:
                    badge = "🟢 Excellent Match"
                    score_box = st.success
                elif score >= 60:
                    badge = "🟡 Good Match"
                    score_box = st.warning
                else:
                    badge = "🔴 Low Match"
                    score_box = st.error

                st.markdown(f"### {index}. {candidate['candidate_name']}")

                score_box(f"Match Score: **{score}%** • {badge}")

                st.progress(score / 100)

                st.write(f"**Recommendation:** {candidate['recommendation']}")

                st.divider()