import pandas as pd


class ExtractTickers:

    CSV = "tickers.csv"

    def read_csv(self):
        data_frame = pd.read_csv(self.CSV)
        return data_frame

    def get_tickers(self):
        dframe = self.read_csv()
        return dframe["Symbol"]
