from django.test import TestCase


class ViewTestCase(TestCase):
    def test_get_stock_history(self):
        response = self.client.get('/stocks/AAPL?ordering=-date&format=json')
        # json_data = response.json()
        self.assertEqual(200, response.status_code)
