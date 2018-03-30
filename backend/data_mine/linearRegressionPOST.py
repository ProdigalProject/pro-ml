# for converting json to csv
import requests
import csv

# for linear regression model
import numpy as np
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class predictor:
    # get json from website
    @staticmethod
    def get_json(ticker_symbol):
        data_url = "http://prodigal-ml.us-east-2.elasticbeanstalk.com/stocks/"+ticker_symbol+"/?format=json"
        file = requests.get(url=data_url)
        json_file = file.json()
        return json_file

    # create csv file from json data
    @staticmethod
    def create_csv(json_file):
        with open('json_data.csv', 'w') as json_data:
            filewriter = csv.writer(json_data, delimiter=',')
            filewriter.writerow(['timestamp','open','high','low','close','volume'])
            for data in json_file:
                timestamp = data["date"]
                open_price = data["opening"]
                high_price = data["high"]
                low_price = data["low"]
                close_price = data["closing"]
                volume = data["volume"]
                filewriter.writerow([timestamp, open_price, high_price, low_price, close_price, volume])

    # predict closing price
    @staticmethod
    def predict_closing(open_price, high_price, low_price):
        data = pd.read_csv("json_data.csv")

        X = data[["open", "high", "low"]]
        y = data["close"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        pred = model.predict([[open_price, high_price, low_price]])
        for i in pred:
            i = str(float(round(i,2)))
            print("Predicted Closing Price: " + "$" + i)

        # post prediction
        # data = {"ticker": "AAPL", "prediction": pred[0], "date_ran_experiment": "2018-03-15"}
        # r = requests.post('http://prodigal-ml.us-east-2.elasticbeanstalk.com/prediction/', data=data)
        # print(r)

        # evaluate prediction model
        # plt.plot(y_test, y_test, c='r', linewidth=0.5)
        # plt.scatter(y_test, y_pred, c='b', s=1)
        # plt.show()
        
def main():
    p = predictor()
    json_file = p.get_json("AAPL")
    p.create_csv(json_file)
    csv_file = 'json_data.csv'
    
    with open(csv_file, newline='') as f:
        reader_r = csv.reader(f,delimiter=',')
        next(reader_r)
        for index, line in enumerate(reader_r):
            print("Input (open, high, low):", line[1], line[2], line[3])
            p.predict_closing(float(line[1]), float(line[2]), float(line[3]))
            print()
            if (index >= 4):
                break

if __name__ == "__main__":
    main()
