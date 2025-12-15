import streamlit as st
import random

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu!")
    st.stop()
st.set_page_config(
    page_title="Sobat Waras",
    page_icon="👐",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align:center;'>Selamat Datang Sobat Waras 👐</h1>",
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='text-align:center; font-size:18px;'>Halo, {st.session_state['username']} 👋</p>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='text-align:center; font-size:18px; margin-top:10px;'>
        Yuk cek kondisi tubuh sobat waras
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("## Silakan pilih menu berikut:")

left_col, right_col = st.columns(2)

with left_col:
    if st.button("Cek Gejala Penyakit", use_container_width=True):
        st.switch_page("pages/page_a.py")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Cek Kesehatan Harian", use_container_width=True):
        st.switch_page("pages/page_b.py")


with right_col:
    if st.button("Mood Tracker", use_container_width=True):
        st.switch_page("pages/page_c.py")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Cek Kesehatan Harian", use_container_width=True):
        st.switch_page("pages/nutrisi.py")


quotes = [
    "Jaga tubuhmu, karena itu adalah rumah pertama bagi jiwamu.",
    "Pola hidup sehat adalah investasi terbaik untuk masa depan.",
    "Minum air putih dulu, tubuhmu butuh itu!",
    "Hidup sehat dimulai dari hal kecil—tidur cukup, makan baik, hati tenang.",
    "Kesehatan bukan tujuan, tetapi perjalanan setiap hari.",
    "Tubuh sehat membuat pikiran kuat. Jaga keduanya!",
    "Istirahat bukan malas. Istirahat adalah kebutuhan tubuh.",
]

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Quotes Semangat Waras:")
st.info(random.choice(quotes))

st.markdown("<hr>", unsafe_allow_html=True)

if st.button("Logout", type="primary"):
    st.session_state.clear()
    st.switch_page("login.py")
