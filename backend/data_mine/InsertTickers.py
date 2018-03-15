import json
# import pandas Temporary
import requests
import time
from data_mine.MineStockPrices import MineStockPrices


class InsertTickers:

    def __init__(self, custom='all', all_tickers=False):
        self.mine = MineStockPrices()
        self.custom = custom
        self.all = all_tickers

    def get_datelist(self, num_dates):
        date_av = []
        datelist = pandas.date_range(end=pandas.datetime.today(),
                                     periods=num_dates).tolist()
        for i in datelist:
            s = str(i.year) + "-" +\
                str(i.month).zfill(2) + "-" +\
                str(i.day).zfill(2)
            date_av.append(s)
        return date_av

    def get_custom_ticker(self, ticker):
        custom_data = self.mine.get_daily_stocks(ticker)
        return custom_data

    def get_all_tickers(self):
        all_data = self.mine.get_daily_stocks(ticker)
        return all_data

    def run(self, num_dates, tickers=None):  # ticker is a list
        if self.all:
            pass
        elif self.custom == 'all':
            custom_list = []
            for ticker in tickers:
                custom_data = self.get_custom_ticker(ticker)
                custom_list.append(custom_data)
                time.sleep(2)
                print(custom_data)

            date_list = self.get_datelist(num_dates)
            self.post_to_api(custom_list, date_list)

    def post_to_api(self, ticker_list, date_list):
        ''' Insert custom ticker to /stocks
            ticker_list: list of tickers
            date_list: list of dates for a range
        '''
        for ticker in ticker_list:
            json_data = json.loads(ticker)
            if 'Error Message' not in json_data.keys():
                daily_data = json_data["Time Series (Daily)"]
                symbol = json_data["Meta Data"]["2. Symbol"]
                base_url = 'http://127.0.0.1:8000/companies/' + symbol
                request_json = requests.get(base_url).json()
                if type(request_json) is not list:
                    company_name = 'Company name DNE'
                else:
                    company_name = request_json[0]['company_name']
                print(company_name)
                for k, v in daily_data.items():
                    if k in date_list:
                        api_data = {}
                        api_data["name"] = company_name
                        api_data["ticker"] = symbol
                        api_data["opening"] = v["1. open"]
                        api_data["high"] = v["2. high"]
                        api_data["low"] = v["3. low"]
                        api_data["closing"] = v["4. close"]
                        api_data["volume"] = v["5. volume"]
                        api_data["date"] = k
                        print(api_data)
                        requests.post(
                            "http://127.0.0.1:8000/stocks/",
                            data=api_data)


def main():
    tickers = []
    r = requests.get("http://127.0.0.1:8000/companies")
    for data in r.json():
        if data['exchange'] == 'Nasdaq Stock Exchange':
            tickers.append(data['ticker'])

    ins = InsertTickers()
    ins.run(365, tickers)


if __name__ == "__main__":
    main()
