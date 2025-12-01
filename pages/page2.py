import streamlit as st

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu!")
    st.stop()

st.title("Selamat Datang Sobat Waras")
st.write(f"Halo, {st.session_state['username']}")
st.write("Silakan pilih menu berikut:")

col1, col2 = st.columns(2)

with col1:
    if st.button("➡️ Cek Gejala Penyakit"):
        st.switch_page("pages/page_a.py")

with col2:
    if st.button("➡️ Cek Kesehatan Harian"):
        st.switch_page("pages/page_b.py")

if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("login.py")
