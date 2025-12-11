import sqlite3

DB_NAME = "warasnesia.db"  

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_user_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def init_mood_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mood_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            tanggal TEXT,
            skor INTEGER,
            mood TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def login_user(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    conn.close()
    return result

def insert_mood(username, tanggal, skor, mood, notes):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO mood_history (username, tanggal, skor, mood, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (username, tanggal, skor, mood, notes))
    conn.commit()
    conn.close()

def load_mood(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT tanggal, skor, mood, notes 
        FROM mood_history 
        WHERE username=? 
        ORDER BY id DESC
    """, (username,))
    rows = cur.fetchall()
    conn.close()
    return rows
