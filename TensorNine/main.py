# TensorNine/main.py
import streamlit as st
from auth import login, logout, register
from dashboard import show_dashboard
from db import create_tables, insert_default_data
from inventory_form import show_inventory_form

def main():
    create_tables()
    insert_default_data()
    st.title("TensorNine - Sales and Inventory App")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.sidebar.title("Login")
        login_status = login()
        if login_status:
            st.session_state['logged_in'] = True
            st.rerun() # Refresh the page after login
        register() # Add register option

    if st.session_state['logged_in']:
        st.sidebar.title("Navigation")
        if st.sidebar.button("Logout"):
            logout()
            st.session_state['logged_in'] = False
            st.rerun() # Refresh the page after logout

        show_dashboard()
        show_inventory_form()

if __name__ == "__main__":
    main()
