# TensorNine/auth.py
import streamlit as st
import sqlite3
import bcrypt
import re

from db import get_db_connection, create_tables, insert_default_data

def register():
    with st.expander("Register"):
        username = st.text_input("Username", key="register_username")
        password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")

        # Email validation
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        # Password complexity validation
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"

        if st.button("Register"):
            if not username:
                st.error("Username is required.")
            elif not re.match(email_pattern, username):
                st.error("Please enter a valid email address.")
            elif not password:
                st.error("Password is required.")
            elif not re.match(password_pattern, password):
                st.error("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password.decode('utf-8')))
                    conn.commit()
                    st.success("Registration successful! Please login.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists.")
                finally:
                    conn.close()

def login():
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                st.success("Logged in successfully!")
                st.session_state['username'] = username
                return True
            else:
                st.error("Incorrect password")
        else:
            st.error("Username not found")
    return False

def logout():
    st.session_state.pop('username', None)
    st.success("Logged out successfully!")
