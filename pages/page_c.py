import streamlit as st
from datetime import datetime
import pandas as pd
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def get_conn():
    return sqlite3.connect("users.db")

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mood_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            skor INTEGER,
            mood TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_mood(tanggal, skor, mood, notes):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO mood_history (tanggal, skor, mood, notes)
        VALUES (?, ?, ?, ?)
    """, (tanggal, skor, mood, notes))
    conn.commit()
    conn.close()

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
    {"Tanggal": r[0], "Skor": r[1], "Mood": r[2], "Catatan": r[3]}
    for r in db_rows
]


MOOD_OPTIONS = {
    1: "😔 Sangat Buruk",
    2: "😟 Buruk",
    3: "😐 Biasa Saja",
    4: "🙂 Baik",
    5: "😊 Sangat Baik"
}
mood_list = list(MOOD_OPTIONS.keys())


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
st.markdown("---")


st.header("1. Catat Mood Anda Sekarang")

with st.form("mood_form", clear_on_submit=True):
    st.markdown("**Bagaimana perasaan Anda hari ini?**")

    selected_score = st.select_slider(
        ' ',
        options=mood_list,
        value=3,
        format_func=lambda x: MOOD_OPTIONS[x]
    )

    notes = st.text_area("Tuliskan sedikit tentang hari Anda (opsional):")

    submitted = st.form_submit_button(" Simpan Mood", type="primary")

    if submitted:
        add_mood_entry(selected_score, notes)


st.markdown("---")


st.header("2. Riwayat Tren Mood")

if st.session_state.mood_history:
    df = pd.DataFrame(st.session_state.mood_history)

    st.subheader("Statistik Mood (Bar Chart)")

    mood_count = df['Skor'].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)

    df_bar = pd.DataFrame({
        "Mood": ["Sangat Buruk", "Buruk", "Cukup", "Baik", "Sangat Baik"],
        "Jumlah": mood_count.values
    })

    st.bar_chart(df_bar.set_index("Mood"))

    st.subheader("Semua Catatan")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Belum ada catatan mood. Silakan catat mood Anda di atas.")
    st.write("Cek jika mood anda tidak stabil")
    if st.button("Cek Gejala Penyakit"):
        st.switch_page("pages/page_a.py")


st.subheader("Export Data (PDF Only)")

df_export = pd.DataFrame(st.session_state.mood_history)


def generate_pdf(df):
    pdf_path = "mood_history.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)

    style = getSampleStyleSheet()
    title = Paragraph("Riwayat Mood Harian", style["Title"])

    data = [list(df.columns)] + df.values.tolist()

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
    st.switch_page("pages/page2.py")