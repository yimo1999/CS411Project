import requests


url = "http://127.0.0.1:5000/login"
d = {"username": "Tom","password": "111111"}
r = requests.post(url, data=d)
print(r.text)

url = "http://127.0.0.1:5000/index?username=Tom"
#
r = requests.get(url)