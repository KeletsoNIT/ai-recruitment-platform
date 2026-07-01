import streamlit as st
from database.db import get_connection
from auth.auth_utils import verify_password


def login_page():

    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, full_name, email, password_hash, role
            FROM users
            WHERE email = ?
        """, (email,))

        user = cursor.fetchone()

        if user is None:
            st.error("User not found")
            return

        user_id, full_name, email, password_hash, role = user

        if verify_password(password, password_hash):

            # 🔥 SESSION STATE (VERY IMPORTANT)
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.user_name = full_name
            st.session_state.user_role = role

            st.success(f"Welcome {full_name}")
            st.write("ROLE FROM DB:", role)
            st.rerun()

        else:
            st.error("Incorrect password")