# TensorNine/db.py
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('tensornine.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT,
            product_name TEXT,
            quantity INTEGER,
            price REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            quantity INTEGER,
            reorder_level INTEGER,
            unit_price REAL
        )
    """)

    conn.commit()
    conn.close()

def insert_default_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Example default sales data
    cursor.execute("INSERT OR IGNORE INTO sales (sale_date, product_name, quantity, price) VALUES (?, ?, ?, ?)",
                   ('2024-01-15', 'Product A', 10, 25.00))
    cursor.execute("INSERT OR IGNORE INTO sales (sale_date, product_name, quantity, price) VALUES (?, ?, ?, ?)",
                   ('2024-01-16', 'Product B', 5, 50.00))

    # Example default inventory data
    cursor.execute("INSERT OR IGNORE INTO inventory (item_name, quantity, reorder_level, unit_price) VALUES (?, ?, ?, ?)",
                   ('Item X', 50, 20, 10.00))
    cursor.execute("INSERT OR IGNORE INTO inventory (item_name, quantity, reorder_level, unit_price) VALUES (?, ?, ?, ?)",
                   ('Item Y', 10, 5, 20.00))

    conn.commit()
    conn.close()
