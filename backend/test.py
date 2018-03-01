import requests 

r = requests.get("http://prodigal-ml.us-east-2.elasticbeanstalk.com/stocks/1/?format=json") 
print(r.text)
print(r.json())
