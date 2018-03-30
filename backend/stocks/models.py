from django.db import models
import requests


# Create your models here.
class Stock(models.Model):
    """
    Class to represent single row of stock table in database.
    """
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=50)
    high = models.FloatField(blank=True, default=0)
    low = models.FloatField(blank=True, default=0)
    opening = models.FloatField(blank=True, default=0)
    closing = models.FloatField(blank=True, default=0)
    volume = models.IntegerField(blank=True, default=0)
    date = models.DateField(blank=True, null=True)

    @staticmethod
    def update_by_ticker(ticker):
        """
        Get recent stock data of given ticker from AlphaVantage API and POSTs latest data to database, then DELETEs
        oldest data from database.
        Fails if company doesn't exist in database or record for current date exists.
        :param ticker: Ticker symbol to update data
        :return: 0: success, 1: record already exists, 2: company not found in database
        """
        try:
            company_obj = Company.objects.get(ticker=ticker)
        except Company.DoesNotExist:  # company not in database
            return 2
        api_key = "NFBPXFB58FY9UAY0"
        base_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
        base_url = base_url + "&symbol=" + ticker + "&apikey=" + api_key
        response = requests.get(base_url).json()
        meta = response["Meta Data"]
        print(meta)
        last_refresh = meta["3. Last Refreshed"][:10]  # market not closed?????
        stock_objs = Stock.objects.filter(ticker=ticker).order_by('-date')
        try:
            stock_objs.get(date=last_refresh)
            print('record exists')
            return 1
        except Stock.DoesNotExist:
            # Delete oldest entry
            oldest_obj = Stock.objects.last()
            print(oldest_obj.date)
            oldest_obj.delete()
            # Add to database using API
            stock_data = response["Time Series (Daily)"][last_refresh]
            api_data = dict()
            api_data["name"] = company_obj.company_name
            api_data["ticker"] = ticker
            api_data["opening"] = stock_data["1. open"]
            api_data["high"] = stock_data["2. high"]
            api_data["low"] = stock_data["3. low"]
            api_data["closing"] = stock_data["4. close"]
            api_data["volume"] = stock_data["5. volume"]
            api_data["date"] = last_refresh
            print(api_data)
            requests.post("http://127.0.0.1:8000/stocks/", data=api_data)
            return 0

    @staticmethod
    def update_all():
        """
        Updates stock data for all companies in database using Stock.update_by_ticker function.
        :return: Operation result of update on each ticker
        """
        ticker_list = []
        return_dict = {}
        company_obj_all = Company.objects.all()  # get all company records in database
        for company in company_obj_all:
            ticker_list.append(company.ticker)
        print(ticker_list)
        for ticker in ticker_list:
            status = Stock.update_by_ticker(ticker)
            if status == 0:
                return_dict[ticker] = "OK"
            elif status == 1:
                return_dict[ticker] = "Error: record already exists"
            else:
                return_dict[ticker] = "Error: company not found in database"
        return return_dict


class Prediction(models.Model): 
    ticker = models.CharField(max_length=50)
    prediction = models.FloatField(blank=True, default=0)
    date_ran_experiment = models.DateField(blank=True, null=True)


class Company(models.Model): 
    ticker = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, unique=True)
    exchange = models.CharField(max_length=100) 
