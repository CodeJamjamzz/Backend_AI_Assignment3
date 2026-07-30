import sqlite3
import os

DB_FILE = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the tasks table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    
    # Seed three example tasks but only if the table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    if count == 0:
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Buy groceries", 0))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Clean the house", 1))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Finish Assignment 2", 0))
    
    conn.commit()
    conn.close()

def reset_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS tasks")
    conn.commit()
    conn.close()
    init_db()
