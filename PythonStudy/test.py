import requests

res = requests.get('https://api.github.com/users/chun4foryou')

print(res.text)
