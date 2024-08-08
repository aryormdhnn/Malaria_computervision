import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image
import pickle
import json
import os
from datetime import datetime

# Fungsi untuk melakukan preprocessing gambar
def preprocess_image(img, target_size):
    img = img.resize(target_size)  # Mengubah ukuran gambar
    array = image.img_to_array(img)  # Mengubah gambar menjadi array
    array = np.expand_dims(array, axis=0)  # Menambahkan dimensi baru di axis 0
    return array

# Fungsi untuk memeriksa apakah gambar valid
def is_valid_image(img):
    return img.mode == 'RGB' and len(img.getbands()) == 3  # Memastikan gambar berwarna (RGB)

# Fungsi untuk menghitung histogram dari gambar
def calculate_histogram(image):
    image = cv2.resize(image, (128, 128))  # Mengubah ukuran gambar
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])  # Menghitung histogram
    hist = cv2.normalize(hist, hist).flatten()  # Menormalisasi histogram dan meratakannya
    return hist

# Fungsi untuk memuat histogram dari file
def load_histograms(histogram_file):
    with open(histogram_file, 'rb') as file:  # Membuka file histogram
        histograms = pickle.load(file)  # Memuat data histogram
    return [np.array(hist, dtype=np.float32) for hist in histograms]  # Mengonversi histogram ke array NumPy

# Fungsi untuk membandingkan histogram gambar dengan histogram referensi
def compare_histograms(image_hist, reference_histograms):
    highest_similarity = -1
    for ref_hist in reference_histograms:
        similarity = cv2.compareHist(np.array(image_hist, dtype=np.float32), np.array(ref_hist, dtype=np.float32), cv2.HISTCMP_CORREL)  # Membandingkan histogram
        if similarity > highest_similarity:
            highest_similarity = similarity
    return highest_similarity

# Fungsi untuk menyimpan hasil ke file JSON
def save_results_to_file(results, file_path='results.json'):
    with open(file_path, 'w') as f:
        json.dump(results, f)  # Menyimpan data hasil ke file JSON

# Fungsi untuk memuat hasil dari file JSON
def load_results_from_file(file_path='results.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)  # Memuat data hasil dari file JSON
                return data
            except json.JSONDecodeError:
                st.error("Berkas JSON tidak valid atau kosong.")
                return []
    else:
        st.warning(f"Berkas {file_path} tidak ditemukan.")
        return []

# Fungsi utama untuk menampilkan antarmuka unggah gambar dan melakukan deteksi malaria
def show_upload_image(model, infected_histograms, uninfected_histograms):
    st.markdown("<h1 style='text-align: center; color: Black;'>Aplikasi Deteksi Malaria</h1>", unsafe_allow_html=True)  # Menampilkan judul aplikasi
    patient_name = st.text_input("Masukkan Nama Pasien:")  # Input nama pasien
    uploaded_file = st.file_uploader("Unggah gambar untuk mendeteksi malaria. Ukuran file maksimum adalah 100 KB.", type=["png", "jpg", "jpeg", "bmp"], help="Limit 100KB per file • PNG, JPG, JPEG, BMP")  # Unggah file gambar

    if uploaded_file is not None and patient_name:
        file_size = uploaded_file.size
        if file_size > 100 * 1024:  # Batas ukuran file 100 KB
            st.warning("Gambar yang diunggah terlalu besar. Silakan unggah gambar yang lebih kecil dari 100 KB.")
        else:
            try:
                img = Image.open(uploaded_file)

                if not is_valid_image(img):
                    st.warning("Gambar yang diunggah tidak sesuai dengan karakteristik yang diharapkan dari dataset. Silakan unggah gambar berwarna (RGB).")
                else:
                    img_array = preprocess_image(img, target_size=(128, 128))  # Mengubah ukuran gambar untuk masukan model
                    img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)  # Mengubah gambar menjadi grayscale

                    image_hist = calculate_histogram(img_gray)  # Menghitung histogram gambar
                    infected_similarity = compare_histograms(image_hist, infected_histograms)  # Membandingkan histogram dengan referensi terinfeksi
                    uninfected_similarity = compare_histograms(image_hist, uninfected_histograms)  # Membandingkan histogram dengan referensi tidak terinfeksi

                    similarity_threshold = 0.1  # Nilai threshold kesamaan histogram

                    if infected_similarity > similarity_threshold or uninfected_similarity > similarity_threshold:
                        with st.spinner('Mengklasifikasikan...'):
                            prediction = model.predict(img_array)  # Melakukan prediksi dengan model
                            malaria_probability = prediction[0][0] * 100  # Probabilitas malaria
                            classification_result = 'Malaria' if malaria_probability > 50 else 'Bukan Malaria'  # Hasil klasifikasi

                            # Jika probabilitas malaria 0%, beri notifikasi tidak valid
                            if malaria_probability == 0:
                                st.warning("Gambar tidak valid untuk deteksi malaria.")
                            else:
                                st.markdown(f"<h3 style='text-align: center; color: black;'>Prediksi: {classification_result}</h3>", unsafe_allow_html=True)  # Menampilkan hasil prediksi
                                st.markdown(f"<p style='text-align: center; color: #515455;'>Kemungkinan: {malaria_probability:.2f}%</p>", unsafe_allow_html=True)  # Menampilkan probabilitas

                                st.image(uploaded_file, caption="Unggah Gambar", use_column_width=True)  # Menampilkan gambar yang diunggah
                                st.progress(malaria_probability / 100)  # Menampilkan progress bar

                                if 'results' not in st.session_state:
                                    st.session_state['results'] = load_results_from_file()  # Memuat hasil dari file jika belum ada di session state

                                upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Waktu pengunggahan

                                st.session_state['results'].append({
                                    "Nama Pasien": patient_name,
                                    "Gambar": uploaded_file.name,
                                    "Prediksi": classification_result,
                                    "Probabilitas": f"{malaria_probability:.2f}%",
                                    "Tanggal Upload": upload_time
                                })  # Menambahkan hasil ke session state

                                save_results_to_file(st.session_state['results'])  # Menyimpan hasil ke file

                    else:
                        st.warning("Gambar yang diunggah tidak sesuai dengan gambar sel darah. Silakan unggah gambar yang benar.")
            except Exception as e:
                st.warning(f"Terjadi kesalahan saat memproses gambar: {e}")

if __name__ == "__main__":
    from tensorflow.keras.models import load_model
    model = load_model('Nadam_TTS_Epoch50.h5')  # Memuat model yang telah dilatih
    infected_histograms = load_histograms('infected_histograms.pkl')  # Memuat histogram Infected yang telah disimpan
    uninfected_histograms = load_histograms('uninfected_histograms.pkl')  # Memuat histogram Uninfected yang telah disimpan
    show_upload_image(model, infected_histograms, uninfected_histograms)  # Menjalankan fungsi utama untuk menampilkan antarmuka unggah gambar
