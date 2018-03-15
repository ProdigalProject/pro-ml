import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

data = pd.read_csv("apple_20.csv")

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