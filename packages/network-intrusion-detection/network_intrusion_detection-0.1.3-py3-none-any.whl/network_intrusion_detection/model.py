import tensorflow as tf
import pkg_resources

def load_model():
    """
    Loads the pre-trained CNN-LSTM model for network intrusion detection and compiles it with the necessary metrics.
    
    Returns:
        model: A compiled Keras model.
    """
    # Get the path to the model file included in the package
    model_path = pkg_resources.resource_filename(__name__, 'cnn_lstm_unsw_finetuned.h5')

    # Load the model from the package
    model = tf.keras.models.load_model(model_path)

    # Compile the model with metrics for evaluation
    model.compile(optimizer='adam',  # you can use the optimizer that fits your model
                  loss='binary_crossentropy',  # assuming it's a binary classification
                  metrics=['accuracy', 'Precision', 'Recall'])

    return model
