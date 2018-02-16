import pytest

@pytest.fixture 
def mineStock():
    from .. import MineStockPrices
    return MineStockPrices.MineStockPrices() 

def test_get_response_from_api(mineStock): 
    r = mineStock.get_response_from_api("TIME_SERIES_DAILY", "MSFT")
    assert(r != None)

def test_get_intraday_stocks(mineStock): 
    r = mineStock.get_response_from_api("TIME_SERIES_INTRADAY", "MSFT", "5min")
    assert(r != None)

def test_get_daily_stocks(mineStock): 
    r = mineStock.get_daily_stocks("MSFT")
    assert(r != None)

def test_get_weekly_stocks(mineStock): 
    r = mineStock.get_weekly_stocks("MSFT")
    assert(r != None)

def test_get_monthly_stocks(mineStock): 
    r = mineStock.get_monthly_stocks("MSFT")
    assert(r != None)

def test_get_daily_cryptos(): 
    pass 

def test_get_weekly_cryptos(): 
    pass 

def test_get_monthly_cryptos(): 
    pass 
