# Intrusion Detection Package

This package provides a CNN-LSTM-based intrusion detection model that can be used to classify network traffic as benign or malicious.

## Installation

You can install the package using pip:

pip install net_intrusion_detection


## Usage

To use the model, follow these steps:

1. Load your pre-trained model (.h5 file).
2. Preprocess your network traffic data (CSV format).
3. Make predictions on the data.

Example:

```python
from network_intrusion_detection import make_prediction

predictions = make_prediction('path_to_model.h5', 'path_to_csv_file.csv')
print(predictions)
