import streamlit as st

# Cek login
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu!")
    st.stop()

st.title("📄 Page B")
st.header("Ini coming soon ehee ")


if st.button("⬅️ Kembali ke Halaman Utama"):
    st.switch_page("pages/page2.py")
