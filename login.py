import streamlit as st

def login():
    # Periksa apakah pengguna sudah autentikasi
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        st.write("You are already logged in.")
        return

    st.markdown("<h2>Login</h2>", unsafe_allow_html=True)

    username = st.text_input("", placeholder="Username")
    password = st.text_input("", type="password", placeholder="Password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state["authenticated"] = True
            st.success("Login successful")
            # Menggunakan st.session_state untuk kontrol status login
            st.session_state["login_state"] = True
        else:
            st.error("Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)

def logout():
    st.session_state["authenticated"] = False
    st.success("Logged out successfully")
    # Menggunakan st.session_state untuk kontrol status logout
    st.session_state["login_state"] = False

# Logika utama untuk menentukan tampilan halaman
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login()
else:
    logout()
