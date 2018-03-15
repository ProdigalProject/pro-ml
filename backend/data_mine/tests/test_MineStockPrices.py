import requests
from django.test import TestCase
from data_mine.MineStockPrices import MineStockPrices


class MineStockPricesTestCase(TestCase):
    pdg_link = 'http://prodigal-ml.us-east-2.elasticbeanstalk.com/stocks/'
    msp = MineStockPrices()

    def test_get_daily_stocks(self):
        r = self.msp.get_daily_stocks('MSFT')
        assert(r is not None)
