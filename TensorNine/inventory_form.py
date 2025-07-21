# TensorNine/inventory_form.py
import streamlit as st
from db import get_db_connection

def show_inventory_form():
    if 'username' in st.session_state:
        st.sidebar.header("Inventory Management")
        with st.sidebar.form("inventory_form"):
            item_name = st.text_input("Item Name", help="Enter the item name (e.g., 'Laptop')")
            quantity = st.number_input("Quantity", min_value=0, step=1, help="Enter the quantity (must be a positive integer)")
            reorder_level = st.number_input("Reorder Level", min_value=0, step=1, help="Enter the reorder level (must be a positive integer)")
            unit_price = st.number_input("Unit Price", min_value=0.00, step=0.01, help="Enter the unit price (e.g., 10.00)")
            submitted = st.form_submit_button("Add Item")

            if submitted:
                if not item_name:
                    st.error("Item Name is required.")
                elif quantity is None:
                    st.error("Quantity is required.")
                elif reorder_level is None:
                    st.error("Reorder Level is required.")
                elif unit_price is None:
                    st.error("Unit Price is required.")
                else:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO inventory (item_name, quantity, reorder_level, unit_price) VALUES (?, ?, ?, ?)",
                                   (item_name, quantity, reorder_level, unit_price))
                    conn.commit()
                    conn.close()
                    st.success("Item added successfully!")
