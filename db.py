import sqlite3

DB_NAME = "memories.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT NOT NULL,
            title TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_memory(user_key, title, text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memories (user_key, title, text) VALUES (?, ?, ?)",
        (user_key, title, text)
    )
    conn.commit()
    conn.close()

def get_memories(user_key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT title, text FROM memories WHERE user_key = ?",
        (user_key,)
    )
    rows = c.fetchall()
    conn.close()

    # WICHTIG: Rückgabe IMMER als Dictionary
    return [{"title": r[0], "text": r[1]} for r in rows]

init_db()
