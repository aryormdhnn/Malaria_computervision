import streamlit as st
import pandas as pd
import json
import os

def load_results_from_file(file_path='results.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                st.error("Berkas JSON tidak valid atau kosong.")
                return []
    else:
        st.warning(f"Berkas {file_path} tidak ditemukan.")
        return []

def show_results():
    st.markdown("<h1 style='text-align: center; color: Black;'>Hasil Pemeriksaan</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='text-align: center; color: grey;'>
        Ini adalah bagian hasil pemeriksaan dari aplikasi Malaria Detection. Di sini, Anda dapat melihat riwayat pemeriksaan yang telah dilakukan.
        </p>
        """,
        unsafe_allow_html=True
    )

    results = load_results_from_file()

    if results:
        df = pd.DataFrame(results)
        df.index = df.index + 1  # Start indexing from 1
        
        # Drop the 'Gambar' column
        if 'Gambar' in df.columns:
            df = df.drop(columns=['Gambar'])
        
        st.table(df)
    else:
        st.markdown("<p style='text-align: center; color: grey;'>Belum ada hasil pemeriksaan.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_results()
