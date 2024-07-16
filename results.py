import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

def load_results_from_file(file_path='results.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def save_result_to_file(result, file_path='results.json'):
    results = load_results_from_file(file_path)
    results.append(result)
    with open(file_path, 'w') as f:
        json.dump(results, f)

def add_new_result(data, file_path='results.json'):
    # Add the current date and time to the data
    data['date_uploaded'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_result_to_file(data, file_path)

def show_results():
    st.markdown("<h1 style='text-align: center; color: Black;'>Hasil Pemeriksaan</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='text-align: center; color: #515455;'>
        Ini adalah bagian hasil pemeriksaan dari aplikasi Malaria Detection. Di sini, Anda dapat melihat riwayat pemeriksaan yang telah dilakukan.
        </p>
        """,
        unsafe_allow_html=True
    )

    results = load_results_from_file()

    if results:
        df = pd.DataFrame(results)
        df.index = df.index + 1  # Start indexing from 1
        st.table(df)
    else:
        st.markdown("<p style='text-align: center; color: #515455;'>Belum ada hasil pemeriksaan.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    # Example of adding a new result (this should be replaced with actual data addition logic)
    example_data = {
        "result_id": 1,
        "patient_name": "John Doe",
        "malaria_result": "Negative",
        # Add other relevant fields
    }
    add_new_result(example_data)

    show_results()
