import requests


class MineStockPrices:
    '''
        MineStockPrices is the class used to pull stock prices data from API.
        Currently using alphavantage.co API to pull data.
        Supports intraday, daily, weekly and monthly prices of tickers.
        Can extend into cryptocurrencies in the future.
    '''
    def __init__(self):
        '''
            Constructor for MineStockPrices.
            Initializes two instance variables.
            _api_key: API token for alphavantage.co
            _base_url: Base URL to call alaphavantage API
        '''
        self._api_key = "NFBPXFB58FY9UAY0"
        self._base_url = "https://www.alphavantage.co/query"

    def get_response_from_api(self, function, search_term):
        '''
            Helper method to return json objects of ticker symbol from API
            function: table/database name defined by alphavantage.co
            search_term: ticker symbol to search for stock prices
        '''
        payload = {}
        payload["function"] = function
        payload["symbol"] = search_term
        response = requests.get(self._base_url, params=payload)
        return response.text

    def get_intraday_stocks(self, search_term):
        '''
            Get stock prices of a paricular company within one day.
            Default time interval between each API pull is 15 minutes.
            Default return format is JSON.
            search_term: ticker symbol to search for stock prices
        '''
        return get_response_from_api("TIME_SERIES_INTRADAY", search_term)

    def get_daily_stocks(self, search_term):
        '''
            Get stock prices of a company daily.
            Default number of entries returned is latest 100 data points.
            Default return format is JSON.
            search_term: ticker symbol to search for stock prices
        '''
        return get_response_from_api("TIME_SERIES_DAILY", search_term)

    def get_weekly_stocks(self, search_term):
        '''
            Get stock prices of a company weekly.
            Default number of entries returned is latest 100 data points.
            Default return format is JSON.
            search_term: ticker symbol to search for stock prices
        '''
        return get_response_from_api("TIME_SERIES_WEEKLY", search_term)

    def get_monthly_stocks(self):
        '''
            Get stock prices of a company monthly.
            Default number of entries returned is latest 100 data points.
            Default return format is JSON.
            search_term: ticker symbol to search for stock prices
        '''
        return get_response_from_api("TIME_SERIES_MONTHLY", search_term)

    def get_intraday_cryptos(self):
        pass

    def get_daily_cryptos(self):
        pass

    def get_weekly_cryptos(self):
        pass

    def get_monthly_cryptos(self):
        pass


def main():
    m = MineStockPrices()
    result = m.get_intraday_stocks("AAPL", "15min")
    print(result)

if __name__ == "__main__":
    main()
