mport streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="WarasNesia - Mood Tracker",
    layout="wide"
)

if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

MOOD_OPTIONS = {
    1: "😔 Sangat Buruk",
    2: "😟 Buruk",
    3: "😐 Biasa Saja",
    4: "🙂 Baik",
    5: "😊 Sangat Baik"
}
mood_list = list(MOOD_OPTIONS.keys())

def add_mood_entry(score, notes):
    """Menambahkan entri mood baru ke session state."""
    new_entry = {
        "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Skor": score,
        "Mood": MOOD_OPTIONS[score],
        "Catatan": notes
    }
    st.session_state.mood_history.insert(0, new_entry)
    st.toast(f"Mood hari ini ({MOOD_OPTIONS[score]}) berhasil dicatat!")

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
    
    st.subheader("Tren Mood (Skor)")
    
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df_chart = df.set_index('Tanggal')
    
    st.line_chart(df_chart['Skor'])

    st.subheader("Semua Catatan")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Belum ada catatan mood. Silakan catat mood Anda di atas.")
    
    st.write("Cek jika mood anda tidak stabil")
    if st.button("Cek Gejala Penyakit"):
        st.switch_page("pages/page_a.py")

if st.button("⬅️ Kembali "):
    st.switch_page("pages/page2.py")