import numpy as np
import pandas as pd
import requests
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data = pd.read_csv("apple_20.csv")

X = data[["open", "high", "low"]]
y = data["close"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

pred = model.predict([[163.045, 165.81, 162.88]])
for i in pred:
    i = str(float(i))
    print("Predicted Closing Price: " + "$" + i)

data = {"name": "AAPL", "prediction": pred}

r = json.dumps(data)
load_r = json.loads(r)

requests.post('http://prodigal-ml.us-east-2.elasticbeanstalk.com/stocks/prediction/?format=json', data)

"""
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(df)
"""

"""
open_price = data["open"]
closing_price = data["close"]
x = np.array(open_price).reshape(-1,1)
y = np.array(closing_price)
model = LinearRegression()
model.fit(x,y)

test_val = 100
pred = model.predict(test_val)
for i in pred:
	i = str(float(i))
	print("Predicted Closing Price: " + "$" + i)
"""

