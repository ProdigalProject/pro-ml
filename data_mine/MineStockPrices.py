import requests
from ExtractTickers import ExtractTickers


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
        self._etc = ExtractTickers() 
        self._api_key = "NFBPXFB58FY9UAY0"
        self._base_url = "https://www.alphavantage.co/query"

    def get_response_from_api(self, function, search_term, datatype="json", interval=None):
        '''
            Helper method to return json objects of ticker symbol from API
            function: table/database name defined by alphavantage.co
            search_term: ticker symbol to search for stock prices
        '''
        payload = {}
        payload["function"] = function
        payload["symbol"] = search_term
        payload["apikey"] = self._api_key
        payload["interval"] = interval
        payload["datatype"] = datatype
        response = requests.get(self._base_url, params=payload)
        return response.text

    def get_intraday_stocks(self, search_term, interval="15min"):
        '''
            Get stock prices of a paricular company within one day.
            Default time interval between each API pull is 15 minutes.
            Default return format is JSON.
            search_term: ticker symbol to search for stock prices
        '''
        return self.get_response_from_api("TIME_SERIES_INTRADAY",
                                          search_term,
                                          interval)

    def get_daily_stocks(self, search_term):
        '''
            Get stock prices of a company daily.
            Default number of entries returned is latest 100 data points.
            Default return format is JSON.
            search_term: ticker symbol to search for stock prices
        '''
        return self.get_response_from_api("TIME_SERIES_DAILY", search_term)

    def get_weekly_stocks(self, search_term, datatype):
        '''
            Get stock prices of a company weekly.
            Default number of entries returned is latest 100 data points.
            Default return format is JSON.
            search_term: ticker symbol to search for stock prices
        '''
        return self.get_response_from_api("TIME_SERIES_WEEKLY", search_term, datatype)

    def get_monthly_stocks(self, search_term):
        '''
            Get stock prices of a company monthly.
            Default number of entries returned is latest 100 data points.
            Default return format is JSON.
            search_term: ticker symbol to search for stock prices
        '''
        return self.get_response_from_api("TIME_SERIES_MONTHLY", search_term)

    def get_intraday_cryptos(self):
        pass

    def get_daily_cryptos(self):
        pass

    def get_weekly_cryptos(self):
        pass

    def get_monthly_cryptos(self):
        pass

    def write_each_ticker_to_file(self): 
        tickers = self._etc.get_tickers()
        for tick in tickers: 
            csv_path = "data/csv/" + tick
            csv_file = open(csv_path, "w") 
            weekly_csv = self.get_weekly_stocks(tick, "csv")
            csv_file.write(weekly_csv) 
            csv_file.close()

            json_path = "data/json/" + tick
            json_file = open(json_path, "w") 
            weekly_json = self.get_weekly_stocks(tick, "json") 
            json_file.write(weekly_json)
            json_file.close()


def main():
    m = MineStockPrices()
    m.write_each_ticker_to_file() 
    

if __name__ == "__main__":
    main()
