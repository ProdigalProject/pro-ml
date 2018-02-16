import pytest


@pytest.fixture
def dataTest():
    from .. import Data
    return Data.Data()


def test_get_data(dataTest):
    input_data = {
        "Inputs": {
            "Apple_Price_History":
            [
                {
                       'timestamp': "2018-04-14T00:00:00",
                       'open': "1",
                       'high': "1",
                       'low': "1",
                       'close': "1",
                       'volume': "1",
                }
            ],
        },

        "GlobalParameters":  {
        }
    }
    r = dataTest.get_data(input_data)
    assert(r is not None)
