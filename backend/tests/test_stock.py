from django.test import TestCase
from stocks.models import Stock


class StockTestCase(TestCase):
    def setup(self):
        Stock.objects.create(name="lion", ticker="LIO")

    def test_stock_create(self):
        lion = Stock.objects.get(name="lion")
        self.assertEqual(lion["ticker"], "LIO")
