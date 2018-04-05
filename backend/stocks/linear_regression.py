# for converting json to csv
import csv
# for linear regression model
from stocks.models import Stock
from stocks.serializers import StockSerializer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


class Predictor:
    """
    Class to run linear regression experiment and predict closing value from
    given data of open, close, high, low and volume.
    """
    @staticmethod
    def get_json(ticker_symbol):
        """
        Gets history data of given ticker from API and returns them in
        JSON file object.
        :param ticker_symbol: Ticker to get data
        :return: JSON file object of history of given ticker
        """
        s_data = Stock.objects.filter(ticker=ticker_symbol).order_by('-date')
        json_file = []
        for data in s_data:
            json_obj = StockSerializer(data).data
            json_file.append(json_obj)
        return json_file

    @staticmethod
    def create_csv(json_file):
        """
        Creates csv file to feed in to prediction model from given JSON file
        object.
        :param json_file: JSON file object from get_json function.
        :return: No return value.
        """
        with open('json_data.csv', 'w', newline='') as json_data:
            filewriter = csv.writer(json_data, delimiter=',')
            filewriter.writerow(['timestamp', 'open',
                                 'high', 'low', 'close', 'volume'])
            for data in json_file:
                timestamp = data["date"]
                open_price = data["opening"]
                high_price = data["high"]
                low_price = data["low"]
                close_price = data["closing"]
                volume = data["volume"]
                filewriter.writerow([timestamp, open_price, high_price,
                                     low_price, close_price, volume])

    @staticmethod
    def predict_closing(open_price, high_price, low_price):
        """
        Predicts closing value from previous open, high, low data using linear
        regression model. 70% of history data is used for training,
        30% for testing.
        :param open_price: open value to be used on prediction
        :param high_price: high value to be used on prediction
        :param low_price: low value to be used on prediction
        :return: prediction result for closing value.
        """
        data = pd.read_csv("json_data.csv")

        x = data[["open", "high", "low"]]
        y = data["close"]

        x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                            test_size=0.3,
                                                            random_state=0)
        model = LinearRegression()
        model.fit(x_train, y_train)

        pred = model.predict([[open_price, high_price, low_price]])
        for i in pred:
            i = str(float(round(i, 2)))
            return i


def return_prediction(ticker_symbol):
    """
    Runs prediction model on given ticker 5 times recursively, and return
    prediction results for next 5 days.
    :param ticker_symbol: Ticker to run experiment on
    :return: List of prediction results.
    """
    p = Predictor()
    json_file = p.get_json(ticker_symbol)
    p.create_csv(json_file)
    csv_file = 'json_data.csv'
    predictions = []

    with open(csv_file, newline='') as f:
        reader_r = csv.reader(f, delimiter=',')
        next(reader_r)
        for index, line in enumerate(reader_r):
            print("Input (open, high, low):", line[1], line[2], line[3])
            expr_result = float(p.predict_closing(float(line[1]),
                                                  float(line[2]),
                                                  float(line[3])))
            predictions.insert(index, expr_result)
            if index >= 4:
                break

    return predictions


def main():
    """
    Kept to test predictor as stand-alone.
    Don't call this function from other module!
    :return: No return value.
    """
    predictions = return_prediction("AAPL")
    print(predictions)


if __name__ == "__main__":
    main()
