import os
import gdown
from tensorflow.keras.models import load_model

def download_model(file_id, output_path):
    try:
        if not os.path.exists(output_path):
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, output_path, quiet=True)
        if not os.path.exists(output_path) or os.path.getsize(output_path) < 1024:
            return "Model download failed or file size is too small"
    except Exception as e:
        return f"Error downloading the model: {e}"
    return None

def load_malaria_model(model_path):
    try:
        model = load_model(model_path)
    except Exception as e:
        return f"Error loading the model: {e}"
    return model

# Misalkan Anda memiliki ID file Google Drive dan path output untuk model
file_id = '17-dxaC04oO95hMExUC_IOoPO0RaRlfkF'
model_path = 'Nadam_TTS_Epoch50.h5'

# Unduh model
error = download_model(file_id, model_path)
if error:
    print(error)
else:
    model = load_malaria_model(model_path)
    if isinstance(model, str):
        print(model)
    else:
        print("Model loaded successfully")
