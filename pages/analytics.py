import streamlit as st
from collections import Counter

from database.recruitment_repo import (
    get_user_sessions,
    get_session_candidates
)


def analytics_page():

    st.title("📊 HR Intelligence Dashboard")

    user_id = st.session_state.user_id
    sessions = get_user_sessions(user_id)

    if not sessions:
        st.info("No recruitment history found yet.")
        return

    # =========================
    # DATA COLLECTION
    # =========================
    all_scores = []
    all_recommendations = []
    tier_counter = Counter()

    for session in sessions:
        candidates = get_session_candidates(session["id"])

        for candidate in candidates:

            score = candidate["match_score"]
            recommendation = candidate["recommendation"]

            all_scores.append(score)
            all_recommendations.append(recommendation)

            # Candidate Tier
            if score >= 80:
                tier = "Strong"
            elif score >= 60:
                tier = "Medium"
            else:
                tier = "Weak"

            tier_counter[tier] += 1

    # =========================
    # SUMMARY METRICS
    # =========================
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Recruitment Sessions", len(sessions))

    with col2:
        st.metric("Candidates Reviewed", len(all_scores))

    with col3:
        st.metric("Average Match", f"{avg_score:.1f}%")

    st.divider()

    # =========================
    # QUALITY DISTRIBUTION
    # =========================
    st.subheader("🎯 Candidate Quality Distribution")
    st.bar_chart(dict(tier_counter))

    # =========================
    # RECOMMENDATIONS
    # =========================
    st.subheader("🤖 AI Recommendations")

    recommendation_counter = Counter(all_recommendations)

    for recommendation, count in recommendation_counter.most_common():
        st.write(f"**{recommendation}** — {count} candidates")

    # =========================
    # HIRING TRENDS
    # =========================
    st.subheader("📅 Recruitment Activity")

    trend = {}

    for session in sessions:
        date = str(session["created_at"])[:10]
        trend[date] = trend.get(date, 0) + 1

    st.line_chart(trend)

    # =========================
    # HIRING EFFICIENCY
    # =========================
    st.subheader("⚡ Hiring Efficiency")

    strong = tier_counter["Strong"]
    total = sum(tier_counter.values())

    efficiency = (strong / total * 100) if total else 0

    st.metric("Strong Candidate Rate", f"{efficiency:.1f}%")