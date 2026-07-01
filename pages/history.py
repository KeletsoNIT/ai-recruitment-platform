import streamlit as st

from database.recruitment_repo import (
    get_user_sessions,
    get_session_candidates
)

# =========================
# HISTORY PAGE
# =========================

def history_page():

    st.title("📊 My Recruitment History")

    user_id = st.session_state.user_id

    sessions = get_user_sessions(user_id)

    if not sessions:
        st.info("No recruitment history yet.")
        return

    for session in sessions:

        with st.expander(f"🧾 {session['job_description'][:60]}..."):

            st.write("**Job Description:**")
            st.write(session["job_description"])

            st.write("**Date:**")
            st.write(session["created_at"])

            candidates = get_session_candidates(session["id"])

            if candidates:

                st.subheader("🏆 Candidates")

                for c in candidates:

                    score = c["match_score"]

                    if score >= 80:
                        st.success(f"{c['candidate_name']} — {score}%")
                    elif score >= 60:
                        st.warning(f"{c['candidate_name']} — {score}%")
                    else:
                        st.error(f"{c['candidate_name']} — {score}%")

                    st.write(f"Recommendation: {c['recommendation']}")

                    st.progress(score / 100)

            else:
                st.info("No candidates found for this session.")