from django.test import TestCase
from stocks.models import Prediction


class PredictionTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        Prediction.objects.create(
            ticker='PDG-ML',
            prediction=179.99,
            date_ran_experiment='2018-03-15')

    def test_prediction_create(self):
        lion = Prediction.objects.get(ticker="PDG-ML")
        self.assertEqual(lion.prediction, 179.99)
