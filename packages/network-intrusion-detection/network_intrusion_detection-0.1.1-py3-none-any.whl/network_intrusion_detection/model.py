import tensorflow as tf

def load_model(model_path):
    """Load the trained model from a file."""
    model = tf.keras.models.load_model(model_path)
    return model
