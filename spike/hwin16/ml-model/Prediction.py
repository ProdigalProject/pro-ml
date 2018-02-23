import numpy as np 
from datetime import datetime

# load 
raw_data = np.loadtxt("apple_20.csv", 
                       usecols=(1:)
                       delimiter=",", 
                       skiprows=1) 

# train test split data 
raw_data

