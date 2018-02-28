import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# load 
file_path = "apple_20.csv" 
raw_data = pd.read_csv(file_path) 
y = raw_data.close 
X = raw_data.loc[:, raw_data.columns != "close"] 

# preprocess


# train test split data 
train_X, train_y, test_X, test_y = train_test_split(X, y, test_size=0.3)

# learn model
model = LinearRegression()
train_model = model.fit(train_X, train_y) 

