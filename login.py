import streamlit as st

def login():
    # Periksa apakah pengguna sudah autentikasi
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        st.write("Anda sudah masuk.")
        return

    st.markdown("<h2>Login</h2>", unsafe_allow_html=True)

    username = st.text_input("", placeholder="Username")
    password = st.text_input("", type="password", placeholder="Password")

    if st.button("Login"):
        if (username == "user1" and password == "user1") or \
                (username == "user" and password == "user"):
            st.session_state["authenticated"] = True
            st.success("Login Berhasil")
            # Menggunakan st.session_state untuk kontrol status login
            st.session_state["login_state"] = True
        else:
            st.error("Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)

def logout():
    st.session_state["authenticated"] = False
    st.success("Berhasil keluar")
    # Menggunakan st.session_state untuk kontrol status logout
    st.session_state["login_state"] = False

# Logika utama untuk menentukan tampilan halaman
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login()
else:
    logout()
