import requests
from stocks.models import Stock
import stocks.linear_regression as predictor


class AlphaAPICaller:
    """
    Utility class to make calls to AlphaVantage API.
    """
    api_key = "NFBPXFB58FY9UAY0"

    def get_compact_date(self, ticker, meta=False):
        """
        Calls AlphaVantage API on given ticker, gets compact (100) history data
        and returns formatted json. If meta=True, result will contain metadata
        of call to AlphaVantage API and list of result data.
        :param ticker: Ticker symbol to get history results
        :param meta: (Optional) Option to attach metadata on result.
        :return: Returns metadata with history or just history.
        """
        b_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
        b_url = b_url + "&symbol=" + ticker + "&apikey=" + self.api_key
        response = requests.get(b_url).json()
        try: 
            daily_dataset = response["Time Series (Daily)"]
            metadata = response["Meta Data"]
            latest_date = metadata["3. Last Refreshed"][:10]
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
            else:  # return data of latest date as separate attribute
                json_result_with_meta = {"latest_data": latest_history,
                                         "history": json_result}
                return json_result_with_meta
        except KeyError:
            empty_list = [] 
            return empty_list


class StockHistoryUpdater:
    """
    Utility class to manage updates of history data on database.
    Update on stock history should occur daily,
    ideally after market closes.
    """
    @staticmethod
    def update_by_ticker(ticker):
        """
        Get recent stock data of given ticker from AlphaVantage API and POSTs
        latest data to database, then DELETEs oldest data from database.
        Fails if company doesn't exist in database or record for current
        date exists.
        :param ticker: Ticker symbol to update data
        :return: 0: success
                 1: record already exists
                 2: company not found in database
        """
        if not Stock.objects.filter(ticker=ticker).exists():
            return 2
        api_response = AlphaAPICaller().get_compact_date(ticker, meta=True)
        # TODO: what happens if market not closed?????
        last_refresh = api_response['latest_data']['date'][:10]
        if Stock.objects.filter(ticker=ticker, date=last_refresh).exists():
            print('record exists')
            return 1
        # Delete oldest entry
        oldest_obj = Stock.objects.filter(ticker=ticker).earliest('date')
        print(oldest_obj.date)
        oldest_obj.delete()
        # Add to database using model or API
        json_data = api_response['latest_data']
        new_entry = Stock(ticker=json_data['ticker'],
                          opening=json_data['opening'],
                          high=json_data['high'], low=json_data['low'],
                          closing=json_data['closing'],
                          volume=json_data['volume'], date=json_data['date'])
        new_entry.save()
        return 0

    @staticmethod
    def update_all():
        """
        Updates stock data for all companies in database using
        Stock.update_by_ticker function.
        :return: Operation result of update on each ticker
        """
        ticker_list = []
        return_dict = {}
        company_obj_all = Stock.objects.values_list('ticker', flat=True)
        company_obj_all = company_obj_all.distinct()  # get all tickers
        for company in company_obj_all:
            ticker_list.append(company)
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
        Run experiment for given ticker and returns list of experiment results
        packed in JSON format.
        Fails if company doesn't exist in database.
        :param ticker: Ticker symbol to run experiment
        :return: JSON containing list of experiment results.
                 -1 if company is not found in database.
        """
        if not Stock.objects.filter(ticker=ticker).exists():
            return -1
        expr_result = predictor.return_prediction(ticker)
        results = []
        for index in range(1, 6):
            api_data = dict()
            api_data['value'] = expr_result[index - 1]
            api_data['ticker'] = ticker
            api_data['id'] = index
            results.append(api_data)
        return results
