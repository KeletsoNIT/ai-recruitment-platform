import streamlit as st

from auth.auth_utils import hash_password
from auth.user_service import create_user, get_user_by_email


def signup_page():

    st.title("HR Signup")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):

        if not full_name or not email or not password:
            st.error("Please fill all fields")
            return

        # Check if user already exists
        existing_user = get_user_by_email(email)

        if existing_user:
            st.error("User already exists with this email")
            return

        password_hash = hash_password(password)

        create_user(full_name, email, password_hash)

        st.success("Account created successfully. You can now login.")