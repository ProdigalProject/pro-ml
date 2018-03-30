import requests
from stocks.models import Stock, Company


class AlphaAPICaller:
    """
    Utility class to make calls to AlphaVantage API.
    """
    api_key = "NFBPXFB58FY9UAY0"

    def get_compact_date(self, ticker, meta=False):
        """
        Calls AlphaVantage API on given ticker, gets compact (100) history data and returns formatted json.
        If meta=True, result will contain metadata of call to AlphaVantage API and list of result data.
        :param ticker: Ticker symbol to get history results
        :param meta: (Optional) Option to attach metadata on result. Default: False
        :return: Returns metadata with history data on True, only history data if False.
        """
        base_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
        base_url = base_url + "&symbol=" + ticker + "&apikey=" + self.api_key
        response = requests.get(base_url).json()
        daily_dataset = response["Time Series (Daily)"]
        metadata = response["Meta Data"]
        latest_date = metadata["3. Last Refreshed"]
        json_result = []
        latest_history = None
        for date, stock_data in daily_dataset.items():
            api_data = dict()
            # not returning name anymore
            api_data["ticker"] = ticker
            api_data["opening"] = stock_data["1. open"]
            api_data["high"] = stock_data["2. high"]
            api_data["low"] = stock_data["3. low"]
            api_data["closing"] = stock_data["4. close"]
            api_data["volume"] = stock_data["5. volume"]
            api_data["date"] = date
            json_result.append(api_data)
            if date == latest_date:
                latest_history = api_data
        if not meta:
            return json_result
        else:
            json_result_with_meta = {"latest_data": latest_history, "history": json_result}
            return json_result_with_meta


class StockHistoryUpdater:
    """
    Utility class to manage updates of history data on database. Update on stock history should occur daily,
    ideally after market closes.
    """
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
            Company.objects.get(ticker=ticker)
        except Company.DoesNotExist:  # company not in database
            return 2
        api_response = AlphaAPICaller().get_compact_date(ticker, meta=True)
        last_refresh = api_response['latest_data']['date']  # TODO: what happens if market not closed?????
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
            # Add to database using model or API
            json_data = api_response['latest_data']
            print(json_data)
            new_entry = Stock(ticker=json_data['ticker'], opening=json_data['opening'],
                              high=json_data['high'], low=json_data['low'], closing=json_data['closing'],
                              volume=json_data['volume'], date=json_data['date'])
            new_entry.save()
            # requests.post("http://127.0.0.1:8000/stocks/", data=json_data)
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
            status = StockHistoryUpdater.update_by_ticker(ticker)
            if status == 0:
                return_dict[ticker] = "OK"
            elif status == 1:
                return_dict[ticker] = "Error: record already exists"
            else:
                return_dict[ticker] = "Error: company not found in database"
        return return_dict


class ExperimentManager:
    """
    Utility class to hold functions related to experiments.
    """
    @staticmethod
    def run_experiment(ticker):
        """
        Run experiment for given ticker and returns list of experiment results. Fails if company doesn't exist in
        database.
        :param ticker: Ticker symbol to run experiment
        :return: List of experiment results. -1 if company is not found in database.
        """
        try:
            Company.objects.get(ticker=ticker)
        except Company.DoesNotExist:  # company not in database
            return -1
        expr_result = [100, 101, 102, 103, 104]  # numbers to be returned from experiment module
        results = []
        for index in range(1, 6):
            results.append({"id": index, "ticker": ticker, "value": expr_result[index - 1]})
        return results
