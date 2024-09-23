import numpy as np
from .model import load_model
from .preprocessing import preprocess_data

def make_prediction(model_path, csv_file):
    """Load the model, preprocess data, and make predictions."""
    model = load_model(model_path)
    X, _ = preprocess_data(csv_file)
    predictions = model.predict(X)
    return np.argmax(predictions, axis=1)
