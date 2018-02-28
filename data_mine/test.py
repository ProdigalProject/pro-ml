from ExtractTickers import ExtractTickers 
from MineStockPrices import MineStockPrices
import pandas as pd 

# etc = ExtractTickers() 
mine = MineStockPrices() 


w = mine.get_weekly_stocks("AAPL") 
f = open("test.txt", 'w')
f.write(w) 
f.close()
