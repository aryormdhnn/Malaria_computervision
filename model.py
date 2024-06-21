import os
import gdown
from tensorflow.keras.models import load_model

def download_model(file_id, output_path):
    try:
        if not os.path.exists(output_path):
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, output_path, quiet=True)
    except Exception as e:
        return f"Error downloading the model: {e}"
    return None

def load_malaria_model(model_path):
    return load_model(model_path)
