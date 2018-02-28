from django.db import models

# Create your models here.
class Stock(object): 
    def __init__(self, name, ticker, high, low, opening, closing, volumes): 
        self.name = name 
        self.ticker = ticker 
        self.high = high 
        self.low = low 
        self.opening = opening
        self.closing = closing
        self.volumes = volumes 

