import streamlit as st
import json
import os
from datetime import datetime
import google.generativeai as genai   # SDK Gemini AI terbaru

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu!")
    st.stop()

token = st.session_state['api']
genai.configure(api_key=token)


model = genai.GenerativeModel("gemini-2.5-flash")


def diagnose_gejala(gejala_list):
    prompt = (
        f"Saya mengalami gejala berikut: {', '.join(gejala_list)}.\n"
        "Gejala tersebut mungkin mengarah ke penyakit apa? "
        "Berikan kemungkinan dan saran tindakan awal secara ringkas dan mudah dipahami."
    )

    response = model.generate_content(prompt)
    return response.text


def save_data(data, filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append(data)
    with open(filename, "w") as f:
        json.dump(existing, f, indent=2)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []


st.title("WarasNesia — Diagnosa Penyakit dan Kesehatan")


menu = st.sidebar.selectbox("Menu", ["Diagnosis Gejala", "Health Tracker", "Mood Tracking"])


if menu == "Diagnosis Gejala":
    st.header("Diagnosis Awal Berdasarkan Gejala")
    gejala_input = st.text_area("Masukkan gejala (pisahkan dengan koma):")

    if st.button("Diagnosa"):
        gejala_list = [g.strip() for g in gejala_input.split(",") if g.strip()]
        if gejala_list:
            hasil = diagnose_gejala(gejala_list)
            st.subheader("Hasil Diagnosis (Kemungkinan & Saran):")
            st.write(hasil)
        else:
            st.warning("Silakan masukkan minimal satu gejala.")


elif menu == "Health Tracker":
    st.header("Catat Aktivitas Harian")
    tidur = st.number_input("Jam tidur (jam):", min_value=0.0, max_value=24.0, step=0.5)
    olahraga = st.text_input("Olahraga yang dilakukan:")
    air = st.number_input("Konsumsi air (gelas):", min_value=0, step=1)
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Simpan Aktivitas"):
        data = {
            "timestamp": tanggal,
            "tidur": tidur,
            "olahraga": olahraga,
            "air": air
        }
        save_data(data, "health_tracker.json")
        st.success("Data aktivitas harian disimpan.")

    st.subheader("Riwayat Aktivitas")
    riwayat = load_data("health_tracker.json")
    st.write(riwayat)


elif menu == "Mood Tracking":
    st.header("Catat Mood Harian")
    mood = st.selectbox("Bagaimana suasana hati Anda hari ini?", ["Sangat Buruk", "Buruk", "Netral", "Baik", "Sangat Baik"])
    catatan = st.text_area("Catatan suasana hati (opsional):")
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Simpan Mood"):
        data = {
            "timestamp": tanggal,
            "mood": mood,
            "catatan": catatan
        }
        save_data(data, "mood_log.json")
        st.success("Mood harian disimpan.")

    st.subheader("Riwayat Mood")
    mood_history = load_data("mood_log.json")
    st.write(mood_history)

if st.button("⬅️ Kembali "):
    st.switch_page("pages/page2.py")