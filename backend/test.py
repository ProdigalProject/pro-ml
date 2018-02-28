import requests 

r = requests.get("http://18.217.102.60:8000/stocks") 
print(r.text)
print(r.json())
