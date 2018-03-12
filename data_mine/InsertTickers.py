from MineStockPrices import MineStockPrices
import json 
import pandas
import requests 

datelist = pandas.date_range(end=pandas.datetime.today(), periods=365).tolist()
date_av = [] 
for i in datelist: 
    s = str(i.year) + "-" + str(i.month).zfill(2) + "-" + str(i.day).zfill(2)
    date_av.append(s) 

mine = MineStockPrices()
full_data = mine.get_daily_stocks("AAPL")

json_data = json.loads(full_data) 
daily_data = json_data["Time Series (Daily)"]

for k, v in daily_data.items(): 
    if k in date_av: 
        api_data = {} 
        api_data["name"] = "Apple Inc." 
        api_data["ticker"] = "AAPL"
        api_data["high"] = v["2. high"] 
        api_data["low"] = v["3. low"] 
        api_data["opening"] = v["1. open"] 
        api_data["closing"] = v["4. close"] 
        api_data["volume"] = v["5. volume"] 
        api_data["date"] = k
        requests.post("http://prodigal-ml.us-east-2.elasticbeanstalk.com/stocks/", data=api_data)
