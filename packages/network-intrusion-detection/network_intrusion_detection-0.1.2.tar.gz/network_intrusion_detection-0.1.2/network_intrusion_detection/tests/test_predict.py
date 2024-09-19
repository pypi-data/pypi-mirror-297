import unittest
from network_intrusion_detection.predict import make_prediction

class TestPredict(unittest.TestCase):
    def test_make_prediction(self):
        predictions = make_prediction('path_to_model.h5', 'tests/sample_data.csv')
        self.assertTrue(all(pred in [0, 1] for pred in predictions))

if __name__ == '__main__':
    unittest.main()
