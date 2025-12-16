import streamlit as st
import requests

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu!")
    st.stop()

st.set_page_config(
    page_title="Cek Nutrisi + Stack",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 Cek Nutrisi Makanan")
st.caption("Menggunakan Stack (LIFO) untuk riwayat pencarian")

# ======================
# INIT STACK
# ======================
if "stack" not in st.session_state:
    st.session_state.stack = []

food = st.text_input("Masukkan nama makanan", placeholder="contoh: milk, biscuit, instant noodle")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Cari Nutrisi"):
        if food == "":
            st.warning("Masukkan nama makanan")
        else:
            st.session_state.stack.append(food)  # PUSH

            url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={food}&search_simple=1&action=process&json=1&page_size=1"

            try:
                response = requests.get(url)
                data = response.json()

                if data["count"] > 0:
                    product = data["products"][0]
                    nutriments = product.get("nutriments", {})

                    st.subheader("🍽️ Informasi Produk")
                    st.write(product.get("product_name", "Nama tidak tersedia"))

                    st.subheader("📊 Nutrisi per 100g")
                    c1, c2 = st.columns(2)

                    c1.metric("🔥 Kalori", f"{nutriments.get('energy-kcal_100g', 0)} kcal")
                    c1.metric("🥑 Lemak", f"{nutriments.get('fat_100g', 0)} g")
                    c1.metric("🍬 Gula", f"{nutriments.get('sugars_100g', 0)} g")

                    c2.metric("🍞 Karbohidrat", f"{nutriments.get('carbohydrates_100g', 0)} g")
                    c2.metric("🥩 Protein", f"{nutriments.get('proteins_100g', 0)} g")
                    c2.metric("🧂 Garam", f"{nutriments.get('salt_100g', 0)} g")

                else:
                    st.error("Produk tidak ditemukan")

            except:
                st.error("Gagal mengambil data dari API")

with col2:
    if st.button("↩️ Undo Pencarian"):
        if st.session_state.stack:
            removed = st.session_state.stack.pop()  # POP
            st.info(f"Pencarian terakhir dibatalkan: **{removed}**")
        else:
            st.warning("Stack kosong")

# SHOW STACK
st.subheader("📚 Riwayat Pencarian (Stack - LIFO)")
if st.session_state.stack:
    for i, item in enumerate(reversed(st.session_state.stack), 1):
        st.write(f"{i}. {item}")
else:
    st.write("Belum ada pencarian")

if st.button("⬅️ Kembali "):
    st.switch_page("pages/page2.py")