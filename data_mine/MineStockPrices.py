import requests

class MineStockPrices: 
    def __init__(self): 
        self._api_key = "NFBPXFB58FY9UAY0"
        self._base_url = "https://www.alphavantage.co/query"

    def get_response_from_api(self, function, search_term): 
        payload = {} 
        payload["function"] = function 
        payload["symbol"] = search_term 
        response = requests.get(self._base_url, params=payload)
        return response.text

    def get_intraday_stocks(self, search_term): 
        return get_response_from_api("TIME_SERIES_INTRADAY", search_term) 

    def get_daily_stocks(self, search_term): 
        return get_response_from_api("TIME_SERIES_DAILY", search_term)

    def get_weekly_stocks(self): 
        return get_response_from_api("TIME_SERIES_WEEKLY", search_term)

    def get_monthly_stocks(self):
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
