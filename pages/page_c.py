import streamlit as st
import pandas as pd
<<<<<<< HEAD
from datetime import datetime
from db import init_mood_table, insert_mood, load_mood
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
=======
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

<<<<<<< HEAD
username = st.session_state["username"]
=======
def get_conn():
    return sqlite3.connect("users.db")
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3

st.set_page_config(page_title="WarasNesia - Mood Tracker", layout="wide")

init_mood_table()

<<<<<<< HEAD
rows = load_mood(username)
st.session_state["mood_history"] = [
=======
def load_mood():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT tanggal, skor, mood, notes FROM mood_history ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


st.set_page_config(
    page_title="WarasNesia - Mood Tracker",
    layout="wide"
)

init_db()  



db_rows = load_mood()

st.session_state.mood_history = [
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3
    {"Tanggal": r[0], "Skor": r[1], "Mood": r[2], "Catatan": r[3]}
    for r in rows
]

<<<<<<< HEAD
=======

>>>>>>> d1b283ff457cb238825624b743c41be5105095b3
MOOD_OPTIONS = {
    1: "😔 Sangat Buruk",
    2: "😟 Buruk",
    3: "😐 Biasa Saja",
    4: "🙂 Baik",
    5: "😊 Sangat Baik"
}

<<<<<<< HEAD
st.title(f"Mood Tracker — {username}")
=======

def add_mood_entry(score, notes):
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")
    mood_text = MOOD_OPTIONS[score]

    insert_mood(tanggal, score, mood_text, notes)

    st.session_state.mood_history.insert(0, {
        "Tanggal": tanggal,
        "Skor": score,
        "Mood": mood_text,
        "Catatan": notes
    })

    st.toast(f"Mood hari ini ({mood_text}) berhasil dicatat!")


st.title(" WarasNesia — Mood Tracker Harian")
st.markdown("Aplikasi sederhana untuk mencatat dan melacak suasana hati Anda.")
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3
st.markdown("---")

<<<<<<< HEAD
# INPUT MOOD
=======

>>>>>>> d1b283ff457cb238825624b743c41be5105095b3
st.header("1. Catat Mood Anda Sekarang")

with st.form("mood_form", clear_on_submit=True):
    score = st.select_slider(
        "Bagaimana perasaan Anda?",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: MOOD_OPTIONS[x]
    )

    notes = st.text_area("Catatan Harian (opsional):")

    submitted = st.form_submit_button("Simpan Mood")

    if submitted:
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")
        mood_text = MOOD_OPTIONS[score]

<<<<<<< HEAD
        insert_mood(username, tanggal, score, mood_text, notes)

        st.session_state["mood_history"].insert(0, {
            "Tanggal": tanggal,
            "Skor": score,
            "Mood": mood_text,
            "Catatan": notes
        })

        st.toast("Mood berhasil disimpan!")

=======

>>>>>>> d1b283ff457cb238825624b743c41be5105095b3
st.markdown("---")

# BAR CHART + TABEL
st.header("2. Riwayat Mood")

<<<<<<< HEAD
if st.session_state["mood_history"]:
    df = pd.DataFrame(st.session_state["mood_history"])
=======
st.header("2. Riwayat Tren Mood")
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3

    st.subheader("Statistik Mood")

<<<<<<< HEAD
    mood_count = df["Skor"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
=======
    st.subheader("Statistik Mood (Bar Chart)")

    mood_count = df['Skor'].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3

    df_bar = pd.DataFrame({
        "Mood": ["Sangat Buruk", "Buruk", "Biasa", "Baik", "Sangat Baik"],
        "Jumlah": mood_count.values
    })

    st.bar_chart(df_bar.set_index("Mood"))

    st.subheader("Semua Catatan")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Belum ada data mood.")

# EXPORT PDF
def generate_pdf(df):
    pdf_path = "mood_history.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    style = getSampleStyleSheet()

<<<<<<< HEAD
    title = Paragraph("Riwayat Mood Harian", style["Title"])
    data = [list(df.columns)] + df.values.tolist()
=======
st.subheader("Export Data (PDF Only)")

df_export = pd.DataFrame(st.session_state.mood_history)
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3

<<<<<<< HEAD
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
=======
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3

<<<<<<< HEAD
    doc.build([title, table])
    return pdf_path
=======
def generate_pdf(df):
    pdf_path = "mood_history.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3

<<<<<<< HEAD
df_export = pd.DataFrame(st.session_state["mood_history"])
pdf = generate_pdf(df_export)
=======
    style = getSampleStyleSheet()
    title = Paragraph("Riwayat Mood Harian", style["Title"])
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3

<<<<<<< HEAD
with open(pdf, "rb") as f:
    st.download_button(
        "Download PDF",
        f,
        file_name="mood_history.pdf",
        mime="application/pdf"
    )
=======
    data = [list(df.columns)] + df.values.tolist()
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3

<<<<<<< HEAD
if st.button("⬅️ Kembali"):
=======
    table = Table(data, colWidths=[120, 60, 100, 180])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ]))

    doc.build([title, table])
    return pdf_path


pdf_file = generate_pdf(df_export)

with open(pdf_file, "rb") as f:
    st.download_button(
        label="Download PDF",
        data=f,
        file_name="mood_history.pdf",
        mime="application/pdf"
    )


if st.button("⬅️ Kembali "):
>>>>>>> d1b283ff457cb238825624b743c41be5105095b3
    st.switch_page("pages/page2.py")