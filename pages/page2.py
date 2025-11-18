import streamlit as st

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu!")
    st.stop()

# st.title("Halaman Page 2")
st.write(f"Selamat datang Sobat Waras, {st.session_state['username']} 👋")

st.set_page_config(
    page_title="WarasNesia",
    page_icon="🩺",
    layout="centered"
)

# Title dan subjudul
st.title("🩺 WarasNesia")
st.subheader("Your Personal Health & Wellness Assistant")

st.write("")
st.write(
    "Selamat datang di **WarasNesia**, aplikasi kesehatan digital berbasis web "
    "yang membantu Anda memantau kesehatan harian, menjaga kesehatan mental, "
    "dan mendapatkan diagnosis awal berdasarkan gejala menggunakan teknologi **Gemini AI**."
)

st.write("---")

# Fitur utama
st.header("✨ Fitur Utama")

st.write("### 1. Diagnosis Gejala (Gemini AI)")
st.write(
    "- Pengguna memasukkan gejala yang dirasakan.\n"
    "- Sistem menganalisis gejala dengan Gemini AI.\n"
    "- Memberikan hasil diagnosis awal dan rekomendasi tindakan."
)

st.write("### 2. Health Tracker Harian")
st.write(
    "- Mencatat aktivitas seperti tidur, minum air, pola makan, dan olahraga.\n"
    "- Menampilkan grafik sederhana perkembangan kesehatan harian."
)

st.write("### 3. Mental Wellness")
st.write(
    "- Pencatatan mood harian.\n"
    "- Relaksasi ringan dan saran kesejahteraan mental."
)

st.write("---")
