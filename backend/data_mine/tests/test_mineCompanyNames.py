import requests
from django.test import TestCase
from data_mine.MineCompanyNames import MineCompanyNames


class MineCompanyNamesTestCase(TestCase):
    pdg_link = 'http://prodigal-ml.us-east-2.elasticbeanstalk.com/companies/'
    mcn = MineCompanyNames()

    def test_post_to_api(self):
        companies = [{'company_name': 'Prodigal-ml',
                      'exchange': 'UIUC stock exchange',
                      'ticker': 'PDG-ML'}]
        self.mcn.post_to_api(companies)
        r = requests.get(self.pdg_link + 'PDG-ML')
        json = r.json()[0]
        self.assertEqual(json['ticker'], 'PDG-ML')

    def tearDown(self):
        r = requests.delete(self.pdg_link + 'PDG-ML')
