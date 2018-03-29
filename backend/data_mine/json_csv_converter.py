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


# get json from website
data_url = "http://prodigal-ml.us-east-2.elasticbeanstalk.com/stocks/AAPL/?format=json"
file = requests.get(url=data_url)
json_file = file.json()

# create csv file from json data
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
data = pd.read_csv("json_data.csv")

X = data[["open", "high", "low"]]
y = data["close"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

pred = model.predict([[163.045, 165.81, 162.88]])
for i in pred:
    i = str(float(round(i,2)))
    print("Predicted Closing Price: " + "$" + i)

# evaluate prediction model
plt.plot(y_test, y_test, c='r', linewidth=0.5)
plt.scatter(y_test, y_pred, c='b', s=1)
plt.show()


