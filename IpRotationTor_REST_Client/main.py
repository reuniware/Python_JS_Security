# Add C:\...\Tor Browser\Browser\TorBrowser\Tor to the current user's environment variables (Windows 10)
import threading
from random import randint, random

from torrequest import TorRequest
import time
import requests
import json

if __name__ == '__main__':
    print('Python + TOR')

with TorRequest(proxy_port=9150, ctrl_port=9151, password=None) as tr:

    resp = tr.get('http://www.ipecho.net/plain')
    print("Current IP : " + resp.text)

    index_reset = 0

    for i in range(10000):

        index_reset = index_reset+1
        if index_reset > 50:
            index_reset = 0
            tr.reset_identity()
            resp = tr.get('http://www.ipecho.net/plain')
            print("Current IP : " + resp.text)

        data = {}
        data['name'] = str(i) + 1000 * chr(randint(1, 8192))
        data['username'] = 1000 * (chr(randint(65, 90)) + chr(randint(65, 90)) + chr(randint(65, 90))) + str(i) + '@random_domain.com'

        resp = tr.post("https://your_rest_api_server_here/api/api_function", json=data)
        print(str(i) + ":" + str(resp.status_code) + " " + str(resp.elapsed.microseconds) + "µs")

