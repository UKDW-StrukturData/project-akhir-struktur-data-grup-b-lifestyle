# import streamlit as st

# st.set_page_config ("WarasNesia")

# st.title("Selamat Datang sobat waras")

# tab1, tab2 = st.tabs([" Login", " Register"])
# with tab1:
#     st.subheader("Login")
#     username = st.text_input ("Username",)
#     password = st.text_input("Password",type = 'password')
    
#     if st.button("Login"):
#         st.success("Login anda berhasil")
#     else:
#         st.error ("Gagal Login")
    

# with tab2:
#     st.subheader("Register")
#     buat =  st.text_input (" buat Username")
#     buat2 = password = st.text_input("buat Password")
    
#     if st.button("Register"):
#         st.success("Berhasil Registrasi")
#     else:
#         st.error("Username/Password sudah digunakan !")

import streamlit as st
from db import init_user_table, login_user, register_user

st.set_page_config("WarasNesia")

init_user_table()

st.title("Selamat Datang Di WarasNesia")
st.subheader("Silakan Login untuk cek keWarasan")

tab1, tab2 = st.tabs(["🔐 Login", "📄 Register"])

# LOGIN
with tab1:
    st.subheader("Login")

    log_user = st.text_input("Username", key="login_user")
    log_pass = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if login_user(log_user, log_pass):
            st.success("Login berhasil!")

            st.session_state["logged_in"] = True
            st.session_state["username"] = log_user

            st.switch_page("pages/page2.py")

        else:
            st.error("Gagal Login! Username atau password salah")


# REGISTER
with tab2:
    st.subheader("Register")

    reg_user = st.text_input("Buat Username", key="reg_user")
    reg_pass = st.text_input("Buat Password", type="password", key="reg_pass")

    if st.button("Register"):
        if register_user(reg_user, reg_pass):
            st.success("Registrasi berhasil! Silakan login.")
        else:
            st.error("Username sudah digunakan!")
