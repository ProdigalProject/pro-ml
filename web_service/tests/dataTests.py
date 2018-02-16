import pytest

@pytest.fixture 
def mineStock():
    from .. import MineStockPrices
    return MineStockPrices.MineStockPrices() 

def test_get_data
    pass