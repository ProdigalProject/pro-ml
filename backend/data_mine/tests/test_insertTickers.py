import requests
import json
from django.test import TestCase 
from data_mine.InsertTickers import InsertTickers 

class InsertTickersTestCase(TestCase): 
    pdg_link = 'http://prodigal-ml.us-east-2.elasticbeanstalk.com/stocks/'
    it = InsertTickers() 

    def test_get_datelist(self): 
        date_list = self.it.get_datelist(1)
        assert(len(date_list) != 0) 

    def test_get_custom_ticker(self): 
        ticker = 'AAPL'
        cdata = self.it.get_custom_ticker(ticker)
        jsondata = json.loads(cdata) 
        self.assertEqual(jsondata['Meta Data']['2. Symbol'], 'AAPL') 
