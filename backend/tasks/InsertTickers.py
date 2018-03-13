import json 
import pandas
import requests 
from MineStockPrices import MineStockPrices

class InsertTickers: 

    def __init__(self, date_range=0, custom=False, all_tickers=False): 
        self.mine = MineStockPrices() 
        self.custom = custom
        self.all = all_tickers 
        self.date_range = date_range

    def get_datelist(self): 
        date_av = [] 
        datelist = pandas.date_range(end=pandas.datetime.today(), 
                                     periods=self.date_range).tolist()
        for i in datelist: 
            s = str(i.year) + "-" +\
                str(i.month).zfill(2) + "-" +\
                str(i.day).zfill(2)
            date_av.append(s) 
        return date_av

    def get_custom_tickers(self, ticker): 
        custom_data = self.mine.get_daily_stocks(ticker)
        return custom_data 

    def get_all_tickers(self): 
        all_data = self.mine.get_daily_stocks(ticker) 
        return all_data 

    def run(self, tickers=None):  # ticker is a list 
        if self.all: 
            pass 
        elif self.custom: 
            custom_list = []
            for ticker in tickers: 
                custom_data = self.get_custom_tickers(ticker) 
                custom_list.append(custom_data)

            date_list = self.get_datelist()
            self.post_to_api(custom_list, date_list) 

    def post_to_api(self, ticker_list, date_list): 
        ''' Insert custom ticker to /stocks
            ticker_list: list of tickers 
            date_list: list of dates for a range
        ''' 
        for ticker in ticker_list: 
            json_data = json.loads(ticker) 
            daily_data = json_data["Time Series (Daily)"]
            symbol = json_data["Meta Data"]["2. Symbol"] 

            for k, v in daily_data.items(): 
                if k in date_list: 
                    api_data = {} 
                    api_data["name"] = "Apple Inc."  # should come from a table
                    api_data["ticker"] = symbol
                    api_data["opening"] = v["1. open"] 
                    api_data["high"] = v["2. high"] 
                    api_data["low"] = v["3. low"] 
                    api_data["closing"] = v["4. close"] 
                    api_data["volume"] = v["5. volume"] 
                    api_data["date"] = k
                    print(api_data) 
                    # requests.post("http://prodigal-ml.us-east-2.elasticbeanstalk.com/stocks/", data=api_data)

    def post_all_to_api(self): 
        pass 

def main(): 
    ins = InsertTickers(custom=True, date_range=10)
    ins.run(['AAPL']) 


if __name__ == "__main__": main()  
