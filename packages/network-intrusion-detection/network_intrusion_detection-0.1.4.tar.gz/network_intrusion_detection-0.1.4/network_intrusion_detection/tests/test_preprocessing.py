import unittest
import pandas as pd
from network_intrusion_detection.preprocessing import preprocess_data

class TestPreprocessing(unittest.TestCase):
    def test_preprocess_data(self):
        # Assuming a sample CSV file is available in the tests directory
        X, y = preprocess_data('tests/sample_data.csv')
        self.assertEqual(X.shape[0], y.shape[0])
        self.assertIn('Label', y.columns)

if __name__ == '__main__':
    unittest.main()
