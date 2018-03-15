from django.test import TestCase


class ApiTestCase(TestCase):
    def setup(self):
        import requests

    def test_api_get(self):
        r = requests.get("http://prodigal-ml.us-east-2.elasticbeanstalk.com\
                        /stocks/AAPL/")
        assert(r is not None)
