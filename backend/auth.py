import bcrypt
from backend.db import get_connection

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

def create_user(username: str, password: str, role: str) -> bool:
    conn = get_connection()
    try:
        conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                     (username, hash_password(password), role))
        conn.commit()
        return True
    except:
        return False

def authenticate_user(username: str, password: str):
    conn = get_connection()
    cur = conn.execute("SELECT id, username, password, role FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    if row:
        uid, user, hashed, role = row
        if verify_password(password, hashed):
            return {"id": uid, "username": user, "role": role}
    return None

def get_all_users():
    conn = get_connection()
    return conn.execute("SELECT username, role FROM users").fetchall()
