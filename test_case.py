import requests

connection_url = 'http://127.0.0.1:5000/api/connections'

headers = {
    'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOjEsImV4cCI6MTY1ODc2Mjk0M30.gaeJEa1_A2fX3XjJ7Y0JKKwPvzPItalSw-Jv3XXJAPI'
}
response = requests.post(connection_url, headers=headers)
# data = response.json()
print(response.json())