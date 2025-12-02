import streamlit as st

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu!")
    st.stop()
    
st.set_page_config("WarasNesia")
import streamlit as st
import requests
import json
from datetime import datetime
import os


RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") or "175800c079mshc73c4de1d473049p1e7957jsn591174a77204"
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")


def hitung_bmi(feet, inches, lbs):
    url = "https://nutrition-calculator.p.rapidapi.com/api/bmi"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
    }
    params = {
        "measurement_units": "std",
        "feet": str(int(feet)),
        "inches": str(int(inches)),
        "lbs": str(int(lbs))
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def hitung_kalori(makanan):
    if not NUTRITIONIX_APP_ID or not NUTRITIONIX_API_KEY:
        return "API Nutritionix belum dikonfigurasi"

    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"query": makanan}

    try:
        res = requests.post(url, json=payload, headers=headers)
        data = res.json()
        if "foods" in data:
            return data["foods"][0]["nf_calories"]
        return "Tidak ditemukan"
    except:
        return "Error API"


def save_health_data(data, filename="health_tracker.json"):
    try:
        with open(filename, "r") as f:
            existing = json.load(f)
    except:
        existing = []
    existing.append(data)
    with open(filename, "w") as f:
        json.dump(existing, f, indent=4)


st.title("Health Tracker Harian + BMI & Nutrisi 🇮🇩")

# Input manual
tidur = st.number_input("Durasi tidur (jam)", 0.0, 24.0, step=0.5)
air = st.number_input("Jumlah air minum (gelas)", 0, 50)
olahraga = st.text_input("Aktivitas olahraga")


st.write("---")
st.subheader("📍 Analisis BMI (gunakan cm dan kg)")
tinggi_cm = st.number_input("Tinggi (cm)", 50, 250)
berat_kg = st.number_input("Berat badan (kg)", 20, 200)

total_inches = tinggi_cm / 2.54
feet = int(total_inches // 12)
inches = int(total_inches % 12)
lbs = berat_kg * 2.20462

# Submit
if st.button("Simpan & Analisis"):
    bmi_data = hitung_bmi(feet, inches, lbs)

    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tidur": tidur,
        "air": air,
        "olahraga": olahraga,
        "BMI": bmi_data
    }
    save_health_data(data)
    st.success("Data berhasil disimpan!")


    st.write("Hasil Analisis")
    if "bmi" in bmi_data:
        try:
            st.write(f" **BMI:** {float(bmi_data['bmi']):.2f}")
        except:
            st.write(f" **BMI:** {bmi_data['bmi']}")
        st.write(f"Konversi tinggi: {tinggi_cm} cm → {feet} ft {inches} in")
        st.write(f"Berat: {berat_kg} kg → {lbs:.1f} lbs")


    st.write("---")
    st.subheader("Rekomendasi Kesehatan")
    if tidur < 6:
        st.warning("Tidur kurang dari 6 jam! Disarankan tidur cukup.")
    else:
        st.success("Tidur sudah cukup baik.")

    if air < 8:
        st.warning("Asupan air kurang dari 8 gelas, tingkatkan!")
    else:
        st.success("Asupan air harian sudah cukup baik!")



if st.button("Kembali ke Halaman Utama"):
    st.switch_page("pages/page2.py")