import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

"""
Predicting the closing price using one feature (the opening price)

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

"""
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(df)
"""
plt.plot(y_test, y_test, c='r', linewidth=0.5)
plt.scatter(y_test, y_pred, c='b', s=1)
plt.show()
