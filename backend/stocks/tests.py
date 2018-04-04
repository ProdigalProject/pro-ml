from django.test import TestCase
from stocks.models import Stock, Company
import datetime


class ViewTestCase(TestCase):
    def setUp(self):
        Company.objects.create(company_name='Microsoft Corporation', ticker='MSFT', exchange='Nasdaq Stock Exchange')
        Company.objects.create(company_name='Amazon.com, Inc.', ticker='AMZN', exchange='Nasdaq Stock Exchange')
        Company.objects.create(company_name='Alphabet Inc.', ticker='GOOG', exchange='Nasdaq Stock Exchange')

    def test_get_stock_history(self):
        response = self.client.get('/stocks/AAPL?ordering=-date&format=json', follow=True)
        self.assertEqual(response.status_code, 200)  # if not existing in db, should populate
        json_data = response.json()
        self.assertEqual(len(json_data), 100)

    def test_get_invalid_stock_history(self):
        response = self.client.get('/stocks/XYZA?ordering=-date&format=json', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_get_all_stock_history(self):
        response = self.client.get('/stocks', follow=True)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 100)

    def test_company_ticker(self):
        response = self.client.get('/companies/MSFT', follow=True)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data[0]['company_name'], 'Microsoft Corporation')

    def test_invalid_company_ticker(self):
        response = self.client.get('/companies/XYZA', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_all_companies(self):
        response = self.client.get('/companies', follow=True)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 3)

    def test_run_experiment(self):
        response = self.client.get('/stocks/AAPL/runexpr', follow=True)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 5)

    def test_run_invalid_experiment(self):
        response = self.client.get('/stocks/XYZA/runexpr', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_update_ticker(self):
        # fill in stock data
        response = self.client.get('/stocks/AAPL?ordering=-date&format=json', follow=True)
        self.assertEqual(response.status_code, 200)
        # delete latest data
        latest_obj = Stock.objects.get(ticker='AAPL').latest('date')
        latest_date = latest_obj.date
        latest_obj.delete()
        oldest_date = Stock.objects.get(ticker='AAPL').earliest('date').date
        # add dummy oldest data to be deleted upon call on update
        dummy_date = oldest_date + datetime.timedelta(days=-1)
        Stock.objects.create(ticker='AAPL', date=dummy_date, high=0, low=0, opening=0, closing=0, volume=100)
        # call update endpoint
        response = self.client.get('/stocks/AAPL/update', follow=True)
        self.assertEqual(response.status_code, 200)
        # check data length and date
        response = self.client.get('/stocks/AAPL?ordering=-date&format=json', follow=True)
        json_data = response.json()
        self.assertEqual(len(json_data), 100)
        self.assertEqual(json_data[0]['date'], latest_date)

    def test_update_ticker_already_latest(self):
        # fill in stock data
        self.client.get('/stocks/AAPL?ordering=-date&format=json', follow=True)
        # call update without deleting latest data
        response = self.client.get('/stocks/AAPL/update', follow=True)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['error'], 'Record already exists')

    def test_update_invalid_ticker(self):
        response = self.client.get('/stocks/XYZA/update', follow=True)
        self.assertEqual(response.status_code, 404)
