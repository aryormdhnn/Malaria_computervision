from tensorflow.keras.models import load_model

def load_malaria_model(model_path):
    return load_model(model_path)
