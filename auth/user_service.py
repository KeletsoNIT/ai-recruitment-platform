from database.db import get_connection

# CREATE USER
def create_user(full_name, email, password_hash):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (full_name, email, password_hash)
        VALUES (?, ?, ?)
    """, (full_name, email, password_hash))

    conn.commit()
    conn.close()


# GET USER BY EMAIL
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()

    return user