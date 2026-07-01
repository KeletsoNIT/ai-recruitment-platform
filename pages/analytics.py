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
    all_roles = []
    tier_counter = Counter()
    skill_counter = Counter()

    for s in sessions:
        candidates = get_session_candidates(s["id"])

        for c in candidates:

            score = c.get("match_score", 0)
            all_scores.append(score)

            role = c.get("recommendation", "Unknown")
            all_roles.append(role)

            # =========================
            # TIER CLASSIFICATION
            # =========================
            if score >= 80:
                tier = "Strong"
            elif score >= 60:
                tier = "Medium"
            else:
                tier = "Weak"

            tier_counter[tier] += 1

            # =========================
            # SKILL INSIGHTS (if stored)
            # =========================
            skills = c.get("matched_skills", [])
            if isinstance(skills, list):
                for s in skills:
                    skill_counter[s] += 1

    # =========================
    # 1. AVERAGE SCORE
    # =========================
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
    st.metric("📈 Average Match Score", f"{avg_score:.2f}%")

    # =========================
    # 2. HIRING QUALITY DISTRIBUTION
    # =========================
    st.subheader("🎯 Candidate Quality Distribution")

    st.bar_chart(dict(tier_counter))

    # =========================
    # 3. TOP ROLES
    # =========================
    st.subheader("🔥 Top Roles / Demand")

    role_counter = Counter(all_roles)

    for role, count in role_counter.most_common(5):
        st.write(f"**{role}** → {count} candidates")

    # =========================
    # 4. TOP SKILLS IN MARKET
    # =========================
    st.subheader("🧠 Most In-Demand Skills")

    for skill, count in skill_counter.most_common(10):
        st.write(f"**{skill}** → {count} mentions")

    # =========================
    # 5. HIRING TRENDS
    # =========================
    st.subheader("📅 Hiring Trends")

    trend = {}

    for s in sessions:
        date = str(s["created_at"])[:10]
        trend[date] = trend.get(date, 0) + 1

    st.line_chart(trend)

    # =========================
    # 6. HIRING EFFICIENCY SCORE
    # =========================
    st.subheader("⚡ Hiring Efficiency")

    strong = tier_counter.get("Strong", 0)
    total = sum(tier_counter.values())

    efficiency = (strong / total * 100) if total > 0 else 0

    st.metric("Strong Hire Rate", f"{efficiency:.2f}%")