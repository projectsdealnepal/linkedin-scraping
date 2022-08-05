import requests
import config

token_url = 'http://127.0.0.1:5000/api/token'
username = config.username
password = config.password

connection_url = '127.0.0.1/api/connections'
response = requests.post(token_url, auth=(username, password))
data = response.json()
token = data['token']
print(token)


