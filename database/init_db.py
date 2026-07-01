from database.db import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    print("Creating tables in:", conn)

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'HR',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # JOB VACANCIES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_vacancies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        department TEXT,
        description TEXT NOT NULL,
        requirements TEXT,
        experience_required TEXT,
        closing_date DATE,
        status TEXT DEFAULT 'Active',
        created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # SESSIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recruitment_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        vacancy_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # CANDIDATES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        candidate_name TEXT,
        cv_filename TEXT,
        match_score REAL,
        recommendation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # AI REPORTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        report_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # AUDIT LOGS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # VACANCY NOTIFICATIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancy_notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vacancy_id INTEGER,
        user_id INTEGER,
        seen INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")


if __name__ == "__main__":
    create_tables()