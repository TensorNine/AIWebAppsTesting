# TensorNine/dashboard.py
import streamlit as st
import pandas as pd
from db import get_db_connection

def show_dashboard():
    st.header("Sales Dashboard")

    conn = get_db_connection()
    sales_data = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()

    if not sales_data.empty:
        tab1, tab2 = st.tabs(["Sales Data", "Sales by Product"])

        with tab1:
            st.subheader("Sales Data")
            st.dataframe(sales_data)

        with tab2:
            st.subheader("Sales by Product")
            sales_by_product = sales_data.groupby('product_name')['quantity'].sum().reset_index()
            st.bar_chart(sales_by_product.set_index('product_name'))
    else:
        st.write("No sales data available.")
