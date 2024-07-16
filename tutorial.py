import streamlit as st

def show_tutorial():
    st.markdown("<h1 style='text-align: center; color: Black;'>Tata Cara Penggunaan Aplikasi</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <ol style='color: #515455;'>
            <li>Buka aplikasi.</li>
            <li>Pastikan anda sudah mengcrop gambar malarianya menjadi sebuah eritrosit.</li>
            <li>Jika belum anda harus memotong gambarnya terlebih dahulu sebelum mengguggah gambarnya</li>
            <li>Pilih menu "Upload Image" untuk mengunggah gambar.</li>
            <li>Unggah gambar sampel darah yang ingin dianalisis.</li>
            <li>Tunggu beberapa saat hingga aplikasi selesai menganalisis gambar.</li>
            <li>Lihat hasil prediksi pada menu "Results".</li>
        </ol>
        """,
        unsafe_allow_html=True
    )
    
    # Create two columns for horizontal layout
    col1, col2 = st.columns(2)

    # Display the images in the columns
    with col1:
        st.image("example.jpg", caption="Contoh gambar yang sudah dipotong", width=200)
    with col2:
        st.image("malaria.jpg", caption="Contoh gambar yang belum dipotong", width=200)

show_tutorial()
