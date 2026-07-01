from database.db import get_connection


# =========================
# GET ALL VACANCIES
# =========================
def get_all_vacancies():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM job_vacancies
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def get_vacancy(vacancy_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM job_vacancies
        WHERE id = ?
    """, (vacancy_id,))

    row = cursor.fetchone()
    conn.close()
    return row


# =========================
# GET ACTIVE VACANCIES
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

    rows = cursor.fetchall()
    conn.close()
    return rows


# =========================
# CREATE VACANCY + NOTIFY HR
# =========================
def save_vacancy(
    title,
    department,
    description,
    requirements,
    experience,
    closing_date,
    created_by
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO job_vacancies (
            title,
            department,
            description,
            requirements,
            experience_required,
            closing_date,
            created_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        department,
        description,
        requirements,
        experience,
        closing_date,
        created_by
    ))

    vacancy_id = cursor.lastrowid

    cursor.execute("""
        SELECT id FROM users WHERE role = 'HR'
    """)
    hr_users = cursor.fetchall()

    for hr in hr_users:
        cursor.execute("""
            INSERT INTO vacancy_notifications (
                vacancy_id,
                user_id,
                seen
            )
            VALUES (?, ?, 0)
        """, (vacancy_id, hr[0]))

    conn.commit()
    conn.close()

    return vacancy_id


# =========================
# CLOSE VACANCY
# =========================
def close_vacancy(vacancy_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE job_vacancies
        SET status = 'Closed'
        WHERE id = ?
    """, (vacancy_id,))

    conn.commit()
    conn.close()