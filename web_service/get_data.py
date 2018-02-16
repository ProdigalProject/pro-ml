import urllib.request
import json

class Data:

    def __init__(self):
        self._api_key = 'e7MiObHOMV+CJ9/I1lahT8HighwH4jDbmhcc30SgePzhkVl4WEEQ/nCpSqNCCZ2K8YIefHKiCQbzpdVCBHlqhA=='
        self._url = 'https://ussouthcentral.services.azureml.net/workspaces/5c0fb2c3710c46348125a99f6dd0e1df/services/e20bef5fd25447658e67952606835a4c/execute?api-version=2.0&format=swagger'

    def get_data(input):
        body = str.encode(json.dumps(input))
        url = 'https://ussouthcentral.services.azureml.net/workspaces/5c0fb2c3710c46348125a99f6dd0e1df/services/e20bef5fd25447658e67952606835a4c/execute?api-version=2.0&format=swagger'
        api_key = 'e7MiObHOMV+CJ9/I1lahT8HighwH4jDbmhcc30SgePzhkVl4WEEQ/nCpSqNCCZ2K8YIefHKiCQbzpdVCBHlqhA=='
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            result = response.read()
            print(result)
        except urllib.error.HTTPError as error:
             print("The request failed with status code: " + str(error.code))
             # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
             print(error.info())
             print(json.loads(error.read().decode("utf8", 'ignore')))

    def main():
        data = {
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
        d = Data()
        result = d.get_data(data)
        print(result)

        if __name__ == "__main__":
            main()