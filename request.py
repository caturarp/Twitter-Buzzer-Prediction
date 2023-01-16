import requests

url = 'http://localhost:5000/results'
r = requests.post(url,json={'compound_mean':0.324, 'account_age':3, 'following':489, 'followers':500})

print(r.json())
