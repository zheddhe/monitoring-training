import requests

# address where to make the requests
address = 'http://localhost:5000/'

# GET requests
for i in range(20):
    response = requests.get(address)
    print(response.content)

# POST requests
for i in range(20):
    response = requests.post(address)
    print(response.content)
