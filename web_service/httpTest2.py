import urllib.request
import json

data = {
        "Inputs": {
                "input1":
                [
                    {
                            'symboling': "1",   
                            'normalized-losses': "1",   
                            'make': "",   

                            'fuel-type': "",   

                            'aspiration': "",   

                            'num-of-doors': "",   

                            'body-style': "",   

                            'drive-wheels': "",   

                            'engine-location': "",   

                            'wheel-base': "1",   

                            'length': "1",   

                            'width': "1",   

                            'height': "1",   

                            'curb-weight': "1",   

                            'engine-type': "",   

                            'num-of-cylinders': "",   

                            'engine-size': "1",   

                            'fuel-system': "",   

                            'bore': "1",   

                            'stroke': "1",   

                            'compression-ratio': "1",   

                            'horsepower': "1",   

                            'peak-rpm': "1",   

                            'city-mpg': "1",   

                            'highway-mpg': "1",   

                            'price': "1",   

                    }

                ],

        },

    "GlobalParameters":  {

    }

}

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/c1f1a7975825466b9c961dc274d8c6e1/services/4b5f7f8b4eca44bfa46eea239759aab3/execute?api-version=2.0&format=swagger'

api_key = 'wV5MTROaNr42P/Z9GNQgtOAf/PB66Zj6rNtti5NsT69kBwZnfm2n2LLwtMMl2MdAqTv1cPK4zuHD0HcjPshV4g=='

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