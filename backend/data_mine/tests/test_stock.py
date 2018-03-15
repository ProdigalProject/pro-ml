from django.test import TestCase
from stocks.models import Stock


class StockTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        Stock.objects.create(name="lion", ticker="LIONARDO")

    def test_stock_create(self):
        lion = Stock.objects.get(name="lion")
        self.assertEqual(lion.ticker, "LIONARDO")
