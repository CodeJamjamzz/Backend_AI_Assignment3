import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the tasks table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    
    # Seed three example tasks but only if the table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()['count']
    
    if count == 0:
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Buy groceries", False))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Clean the house", True))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Finish Assignment 2", False))
    
    conn.commit()
    conn.close()

def reset_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS tasks")
    conn.commit()
    conn.close()
    init_db()
