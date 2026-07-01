from database.db import get_connection


# =========================
# CREATE RECRUITMENT SESSION (UPDATED)
# =========================
def save_session(user_id, vacancy_id, job_title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO recruitment_sessions (user_id, vacancy_id, job_title)
        VALUES (?, ?, ?)
    """, (user_id, vacancy_id, job_title))

    conn.commit()
    session_id = cursor.lastrowid
    conn.close()

    return session_id


# =========================
# SAVE CANDIDATE RESULT (UNCHANGED)
# =========================
def save_candidate(session_id, candidate_name, score, recommendation):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidates (
            session_id,
            candidate_name,
            match_score,
            recommendation
        )
        VALUES (?, ?, ?, ?)
    """, (session_id, candidate_name, score, recommendation))

    conn.commit()
    conn.close()


# =========================
# GET USER HISTORY (UPDATED JOIN READY)
# =========================
def get_user_sessions(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT rs.id,
               rs.user_id,
               rs.vacancy_id,
               rs.created_at,
               jv.title,
               jv.department,
               jv.status
        FROM recruitment_sessions rs
        LEFT JOIN job_vacancies jv
        ON rs.vacancy_id = jv.id
        WHERE rs.user_id = ?
        ORDER BY rs.created_at DESC
    """, (user_id,))

    return cursor.fetchall()


# =========================
# GET SESSION CANDIDATES (UNCHANGED)
# =========================
def get_session_candidates(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM candidates
        WHERE session_id = ?
        ORDER BY match_score DESC
    """, (session_id,))

    return cursor.fetchall()


# =========================
# GET VACANCY DETAILS (NEW - IMPORTANT)
# =========================
def get_vacancy(vacancy_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM job_vacancies
        WHERE id = ?
    """, (vacancy_id,))

    return cursor.fetchone()


# =========================
# GET ALL ACTIVE VACANCIES (NEW)
# =========================
def get_active_vacancies():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM job_vacancies
        WHERE status = 'Active'
        ORDER BY created_at DESC
    """)

    return cursor.fetchall()