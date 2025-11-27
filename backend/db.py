import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "users.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT
                    );''')
    conn.commit()
    return conn
