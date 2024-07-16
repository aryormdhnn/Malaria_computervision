import streamlit as st
from model import load_malaria_model
from home import show_home
from upload_image import show_upload_image
from tutorial import show_tutorial
from results import show_results
from login import login, logout
import pickle

# Load histograms
def load_histograms(histogram_file):
    with open(histogram_file, 'rb') as file:
        histograms = pickle.load(file)
    return histograms

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Check authentication
if not st.session_state["authenticated"]:
    login()
else:
    st.sidebar.button("Logout", on_click=logout)

    # Sidebar menu
    menu = st.sidebar.radio(
        "Menu",
        ("Home", "Unggah Gambar", "Hasil Pemeriksaan", "Tutorial Penggunaan Aplikasi")
    )

    # Load model
    model_path = 'Nadam_TTS_Epoch50.h5'
    model = load_malaria_model(model_path)
    infected_histograms = load_histograms('infected_histograms.pkl')
    uninfected_histograms = load_histograms('uninfected_histograms.pkl')

    # Display sections based on menu selection
    if menu == "Home":
        show_home()
    elif menu == "Unggah Gambar":
        show_upload_image(model, infected_histograms, uninfected_histograms)
    elif menu == "Hasil Pemeriksaan":
        show_results()
    elif menu == "Tutorial Penggunaan Aplikasi":
        show_tutorial()
