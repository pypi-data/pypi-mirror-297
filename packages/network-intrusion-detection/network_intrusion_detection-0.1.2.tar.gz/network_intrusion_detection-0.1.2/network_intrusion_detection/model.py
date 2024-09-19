import tensorflow as tf
import pkg_resources  # To access package resources

def load_model():
    # Automatically locate the model within the package
    model_path = pkg_resources.resource_filename('network_intrusion_detection', 'cnn_lstm_unsw_finetuned.h5')
    
    # Load the pre-trained model from the path
    model = tf.keras.models.load_model(model_path)
    
    return model
