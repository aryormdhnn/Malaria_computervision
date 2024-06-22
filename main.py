import streamlit as st
from model import download_model, load_malaria_model
from home import show_home
from upload_image import show_upload_image
from tutorial import show_tutorial
from results import show_results
from authentication import login, logout
import pickle

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border: None;
        border-radius: 5px;
        padding: 10px;
    }
    .stFileUploader>button {
        background-color: #1f77b4;
        color: white;
        border: None;
        border-radius: 5px;
        padding: 10px;
    }
    .stProgress>div>div {
        background-color: #1f77b4;
    }
    .stTextInput>div>div>input {
        color: black;
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

    # Download and load model
    file_id = '17-dxaC04oO95hMExUC_IOoPO0RaRlfkF'
    model_path = 'Nadam_TTS_Epoch50.h5'
    error = download_model(file_id, model_path)
    if error:
        st.error(error)
    else:
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

    # Custom footer
    st.markdown("<p style='text-align: center; color: grey;'>© 2024 Malaria Detection App</p>", unsafe_allow_html=True)
