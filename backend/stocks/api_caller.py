import requests


def get_compact_date(ticker):
    api_key = "NFBPXFB58FY9UAY0"
    base_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
    base_url = base_url + "&symbol=" + ticker + "&apikey=" + api_key
    response = requests.get(base_url).json()
    meta = response["Meta Data"]
    print(meta)
    last_refresh = meta["3. Last Refreshed"]