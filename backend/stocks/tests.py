from django.test import TestCase
import pycodestyle
from stocks.models import Stock
import datetime


class ViewTestCase(TestCase):

    def test_get_stock_history(self):
        """
        Tests valid /stocks/<ticker> endpoint call.
        """
        response = self.client.get('/stocks/AAPL?ordering=-date&format=json'
                                   '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        # if not existing in db, should populate
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 100)

    def test_get_invalid_stock_history(self):
        """
        Tests /stocks/<ticker> endpoint call on non-existing company.
        """
        response = self.client.get('/stocks/XYZA?ordering=-date&format=json'
                                   '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 404)

    def test_get_stock_history_api_key_check(self):
        """
        Tests /stocks/<ticker> endpoint call without api key.
        """
        response = self.client.get('/stocks/AAPL?ordering=-date&format=json',
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_stock_history_invalid_api_key(self):
        """
        Tests /stocks/<ticker> endpoint call with wrong api key.
        """
        response = self.client.get('/stocks/AAPL?ordering=-date&format=json'
                                   '&apikey=invalid_key',
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_all_stock_history(self):
        """
        Tests valid /stocks endpoint call.
        """
        # fill in data for 2 companies
        self.client.get('/stocks/AAPL?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=', follow=True)
        self.client.get('/stocks/MSFT?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=', follow=True)
        # get all data
        response = self.client.get('/stocks'
                                   '?apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 200)

    def test_get_all_stock_history_api_key_check(self):
        """
        Tests /stocks endpoint call without api key.
        """
        response = self.client.get('/stocks'
                                   '?apikey=invalidkey',
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_all_stock_history_invalid_api_key(self):
        """
        Tests /stocks endpoint call with wrong api key.
        """
        response = self.client.get('/stocks', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_run_experiment(self):
        """
        Tests valid /stocks/<ticker>/runexpr endpoint call.
        """
        # fill in data
        self.client.get('/stocks/AAPL?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=', follow=True)
        # run experiment
        response = self.client.get('/stocks/AAPL/runexpr'
                                   '?apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 5)

    def test_run_invalid_experiment(self):
        """
        Tests /stocks/<ticker>/runexpr endpoint call on non-existing company.
        :return:
        """
        response = self.client.get('/stocks/XYZA/runexpr'
                                   '?apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 404)

    def test_run_experiment_api_key_check(self):
        """
        Tests /stocks/<ticker>/runexpr endpoint call without api key.
        """
        # fill in data
        self.client.get('/stocks/AAPL?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=', follow=True)
        # run experiment without api key
        response = self.client.get('/stocks/AAPL/runexpr', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_run_experiment_invalid_api_key(self):
        """
        Tests /stocks/<ticker>/runexpr endpoint call with wrong api key.
        """
        # fill in data
        self.client.get('/stocks/AAPL?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=', follow=True)
        # run experiment without api key
        response = self.client.get('/stocks/AAPL/runexpr'
                                   '?apikey=invalid_key',
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_update_ticker(self):
        """
        Tests valid /stocks/<ticker>/update endpoint call.
        """
        # fill in stock data
        self.client.get('/stocks/AAPL?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                        follow=True)
        # delete latest data
        latest_obj = Stock.objects.filter(ticker='AAPL').latest('date')
        latest_date = latest_obj.date
        latest_obj.delete()
        oldest_date = Stock.objects.filter(ticker='AAPL').earliest('date').date
        # add dummy oldest data to be deleted upon call on update
        dummy_date = oldest_date + datetime.timedelta(days=-1)
        Stock.objects.create(ticker='AAPL', date=dummy_date, high=0, low=0,
                             opening=0, closing=0, volume=100)
        # call update endpoint
        response = self.client.get('/stocks/AAPL/update'
                                   '?apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        # check data length and date
        response = self.client.get('/stocks/AAPL?ordering=-date&format=json'
                                   '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        json_data = response.json()
        self.assertEqual(len(json_data), 100)
        self.assertEqual(json_data[0]['date'], str(latest_date))

    def test_update_ticker_already_latest(self):
        """
        Tests /stocks/<ticker>/update endpoint call on already
        up to date company.
        """
        # fill in stock data
        self.client.get('/stocks/AAPL?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=', follow=True)
        # call update without deleting latest data
        response = self.client.get('/stocks/AAPL/update'
                                   '?apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['error'], 'Record already exists')

    def test_update_invalid_ticker(self):
        """
        Tests /stocks/<ticker>/update endpoint call on non-existing company.
        """
        response = self.client.get('/stocks/XYZA/update'
                                   '?apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 404)

    def test_update_ticker_api_key_check(self):
        """
        Tests /stocks/<ticker>/update endpoint call without api key.
        """
        # fill in stock data
        self.client.get('/stocks/AAPL?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                        follow=True)
        # delete latest data
        latest_obj = Stock.objects.filter(ticker='AAPL').latest('date')
        latest_obj.delete()
        oldest_date = Stock.objects.filter(ticker='AAPL').earliest('date').date
        # add dummy oldest data to be deleted upon call on update
        dummy_date = oldest_date + datetime.timedelta(days=-1)
        Stock.objects.create(ticker='AAPL', date=dummy_date, high=0, low=0,
                             opening=0, closing=0, volume=100)
        # call update endpoint without api key
        response = self.client.get('/stocks/AAPL/update', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_update_ticker_invalid_api_key(self):
        """
        Tests /stocks/<ticker>/update endpoint call with wrong api key.
        """
        # fill in stock data
        self.client.get('/stocks/AAPL?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                        follow=True)
        # delete latest data
        latest_obj = Stock.objects.filter(ticker='AAPL').latest('date')
        latest_obj.delete()
        oldest_date = Stock.objects.filter(ticker='AAPL').earliest('date').date
        # add dummy oldest data to be deleted upon call on update
        dummy_date = oldest_date + datetime.timedelta(days=-1)
        Stock.objects.create(ticker='AAPL', date=dummy_date, high=0, low=0,
                             opening=0, closing=0, volume=100)
        # call update endpoint without api key
        response = self.client.get('/stocks/AAPL/update'
                                   '?apikey=invalid_key',
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_update_all(self):
        """
        Tests valid /stocks/update endpoint call.
        """
        # fill in stock data for 2 tickers
        response = self.client.get('/stocks/AAPL?ordering=-date&format=json'
                                   '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/stocks/MSFT?ordering=-date&format=json'
                                   '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        # delete latest data
        latest_obj = Stock.objects.filter(ticker='AAPL').latest('date')
        latest_date_aapl = latest_obj.date
        latest_obj.delete()
        oldest_obj_aapl = Stock.objects.filter(ticker='AAPL').earliest('date')
        oldest_date_aapl = oldest_obj_aapl.date
        latest_obj = Stock.objects.filter(ticker='MSFT').latest('date')
        latest_date_msft = latest_obj.date
        latest_obj.delete()
        oldest_obj_msft = Stock.objects.filter(ticker='MSFT').earliest('date')
        oldest_date_msft = oldest_obj_msft.date
        # add dummy oldest data to be deleted upon call on update
        dummy_date_aapl = oldest_date_aapl + datetime.timedelta(days=-1)
        dummy_date_msft = oldest_date_msft + datetime.timedelta(days=-1)
        Stock.objects.create(ticker='AAPL', date=dummy_date_aapl, high=0,
                             low=0, opening=0, closing=0, volume=100)
        Stock.objects.create(ticker='MSFT', date=dummy_date_msft, high=0,
                             low=0, opening=0, closing=0, volume=100)
        # call update endpoint
        response = self.client.get('/stocks/update'
                                   '?apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        # check data length and date
        response = self.client.get('/stocks/AAPL?ordering=-date&format=json'
                                   '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        json_data = response.json()
        self.assertEqual(len(json_data), 100)
        self.assertEqual(json_data[0]['date'], str(latest_date_aapl))
        response = self.client.get('/stocks/MSFT?ordering=-date&format=json'
                                   '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        json_data = response.json()
        self.assertEqual(len(json_data), 100)
        self.assertEqual(json_data[0]['date'], str(latest_date_msft))

    def test_update_all_existing(self):
        """
        Tests /stocks/update endpoint call, with some data already
        up to date in database.
        """
        # fill in stock data for 2 tickers
        self.client.get('/stocks/AAPL?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                        follow=True)
        self.client.get('/stocks/MSFT?ordering=-date&format=json'
                        '&apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                        follow=True)
        # delete latest data of AAPL
        latest_obj = Stock.objects.filter(ticker='AAPL').latest('date')
        latest_obj.delete()
        oldest_obj_aapl = Stock.objects.filter(ticker='AAPL').earliest('date')
        oldest_date_aapl = oldest_obj_aapl.date
        # add dummy oldest data to be deleted upon call on update
        dummy_date_aapl = oldest_date_aapl + datetime.timedelta(days=-1)
        Stock.objects.create(ticker='AAPL', date=dummy_date_aapl, high=0,
                             low=0, opening=0, closing=0, volume=100)
        # call update endpoint
        response = self.client.get('/stocks/update'
                                   '?apikey=cHJvZGlnYWxfYXBwX2FwaV9rZXk=',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['AAPL'], 'OK')
        self.assertEqual(json_data['MSFT'], 'Error: record already exists')

    def test_update_all_api_key_check(self):
        """
        Tests /stocks/update endpoint call without api key.
        """
        # call update endpoint
        response = self.client.get('/stocks/update', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_update_all_invalid_api_key(self):
        """
        Tests /stocks/update endpoint call with wrong api key.
        """
        # call update endpoint
        response = self.client.get('/stocks/update'
                                   '?apikey=invalid_key',
                                   follow=True)
        self.assertEqual(response.status_code, 403)


class CodeStyleTestCase(TestCase):

    def test_pep8(self):
        """
        Checks if all files in test_files are PEP8 compliant.
        """
        pep = pycodestyle.StyleGuide()
        test_files = ['stocks/linear_regression.py', 'stocks/models.py',
                      'stocks/serializers.py', 'stocks/urls.py',
                      'stocks/utilities.py', 'stocks/views.py',
                      'stocks/tests.py']
        result = pep.check_files(test_files)
        self.assertEqual(result.total_errors, 0)
