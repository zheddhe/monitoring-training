import time
import requests

address = 'http://localhost:5000/'

for i in range(100):
    # sleeping
    time.sleep(0.1)
    # this help us not to wait for our response
    try:
        requests.get(address, timeout=10e-9)
    except requests.exceptions.ReadTimeout:
        pass
