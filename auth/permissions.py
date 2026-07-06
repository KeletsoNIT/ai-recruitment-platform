import sqlite3

def is_admin(user_id):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role FROM users WHERE id = ?
    """, (user_id,))

    result = cursor.fetchone()

    if result and result[0] == "admin":
        return True

    return False