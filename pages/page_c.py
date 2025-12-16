import streamlit as st
import pandas as pd
from datetime import datetime
from db import init_mood_table, insert_mood, load_mood
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

username = st.session_state.get("username", "Pengguna")

st.set_page_config(
    page_title="WarasNesia - Mood Tracker",
    layout="wide"
)

#sort
def quick_sort(data, key):
    if len(data) <= 1:
        return data

    pivot = data[len(data) // 2][key]
    left = [x for x in data if x[key] < pivot]
    middle = [x for x in data if x[key] == pivot]
    right = [x for x in data if x[key] > pivot]

    return quick_sort(left, key) + middle + quick_sort(right, key)

init_mood_table()
rows = load_mood(username)

st.session_state["mood_history"] = [
    {"Tanggal": r[0], "Skor": r[1], "Mood": r[2], "Catatan": r[3]}
    for r in rows
]

MOOD_OPTIONS = {
    1: "😔 Sangat Buruk",
    2: "😟 Buruk",
    3: "😐 Biasa Saja",
    4: "🙂 Baik",
    5: "😊 Sangat Baik"
}

st.title(f"Mood Tracker — {username}")
st.markdown("---")

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

        insert_mood(username, tanggal, score, mood_text, notes)

        
        st.session_state["mood_history"].insert(0, {
            "Tanggal": tanggal,
            "Skor": score,
            "Mood": mood_text,
            "Catatan": notes
        })

        # reset sorting
        st.session_state.pop("sorted_history", None)

        st.toast("Mood berhasil disimpan!")

st.markdown("---")

st.header("2. Riwayat Mood")

if st.session_state["mood_history"]:
    
    # -------- DISPLAY DATA --------
    display_data = st.session_state.get(
        "sorted_history",
        st.session_state["mood_history"]
    )

    df = pd.DataFrame(display_data)

   
    st.subheader("Statistik Mood")

    mood_count = (
        df["Skor"]
        .value_counts()
        .reindex([1, 2, 3, 4, 5], fill_value=0)
    )

    df_bar = pd.DataFrame({
        "Mood": ["Sangat Buruk", "Buruk", "Biasa", "Baik", "Sangat Baik"],
        "Jumlah": mood_count.values
    })

    st.bar_chart(df_bar.set_index("Mood"))
    
    st.subheader("Urutkan Data Mood")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬆ Skor dari Terendah"):
            st.session_state["sorted_history"] = quick_sort(
                st.session_state["mood_history"], "Skor"
            )

    with col2:
        if st.button("⬇ Skor dari Tertinggi"):
            st.session_state["sorted_history"] = quick_sort(
                st.session_state["mood_history"], "Skor"
            )[::-1]

    with col3:
        if st.button("Reset Urutan"):
            st.session_state.pop("sorted_history", None)

    # TABLE 
    st.subheader("Semua Catatan")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Belum ada data mood.")


def generate_pdf(df):
    if df.empty:
        return None

    pdf_path = "mood_history.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    style = getSampleStyleSheet()

    title = Paragraph("Riwayat Mood Harian", style["Title"])
    data = [list(df.columns)] + df.values.tolist()

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))

    doc.build([title, table])
    return pdf_path

df_export = pd.DataFrame(
    st.session_state.get("sorted_history", st.session_state["mood_history"])
)

if df_export.empty:
    st.info("Belum ada data mood untuk di-export ke PDF.")
else:
    pdf = generate_pdf(df_export)

    if pdf:
        with open(pdf, "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                file_name="mood_history.pdf",
                mime="application/pdf"
            )

if st.button("⬅️ Kembali"):
    st.switch_page("pages/page2.py")
