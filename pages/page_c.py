import streamlit as st
from datetime import datetime
import pandas as pd
import sqlite3


# ==============================
#  DATABASE
# ==============================
def get_conn():
    return sqlite3.connect("users.db")


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mood_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            mood TEXT NOT NULL,
            notes TEXT
        )
    """)
    conn.commit()

init_db()


# ==============================
#   FUNGSI CRUD
# ==============================
def add_mood(mood, notes):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO mood_history (date, mood, notes) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mood, notes)
    )
    conn.commit()


def get_moods():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM mood_history ORDER BY id DESC", conn)
    return df


# ==============================
#          UI
# ==============================
st.title("📘 Mood Harian")

st.subheader("Input Mood")
mood = st.selectbox("Pilih mood:", ["Senang", "Sedih", "Stress", "Tenang", "Capek"])
notes = st.text_area("Catatan")

if st.button("Simpan"):
    add_mood(mood, notes)
    st.success("Mood berhasil disimpan!")

st.subheader("Riwayat Mood")
df = get_moods()
st.dataframe(df)


# ==============================
#       EXPORT TANPA PDF
# ==============================
st.subheader("Export Data")

# CSV
csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv_data, "mood.csv", "text/csv")

# Excel
excel = df.to_excel("mood.xlsx", index=False)
with open("mood.xlsx", "rb") as f:
    st.download_button("Download Excel", f, file_name="mood.xlsx")

# JSON
json_data = df.to_json(orient="records").encode("utf-8")
st.download_button("Download JSON", json_data, "mood.json", "application/json")
