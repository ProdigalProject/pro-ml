import requests

class MineStockPrices: 
    def __init__(self): 
        self._api_key = "NFBPXFB58FY9UAY0"
        self._base_url = "https://www.alphavantage.co/query"

    def get_intraday_stocks(self, search_term, interval="5min", outputsize="compact"): 
        payload = {} 
        payload["function"] = "TIME_SERIES_INTRADAY"
        payload["symbol"] = search_term 
        payload["interval"] = interval
        payload["outputsize"] = outputsize
        payload["apikey"] = self._api_key
        response = requests.get(self._base_url, params=payload)
        return response.text

    def get_daily_stocks(self): 
        pass 

    def get_weekly_stocks(self): 
        pass 

    def get_monthly_stocks(self):
        pass 

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
