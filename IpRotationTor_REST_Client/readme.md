This python script demonstrates how to use the TOR network for accessing a remote REST service (POST).

This script gets a new TOR IP address every 50 requests.

This works on Windows 10.

Clues for adapting for Windows 7 (with Python 2.7) :

- Import requesocks

GET SAMPLE :

import requesocks

session = requesocks.session()

session.proxies = {'http': 'socks5://127.0.0.1:9150', 'https': 'socks5://127.0.0.1:9150'}

r = session.get('http://www.ipecho.net/plain', auth=('user', 'pass'))

print(r.status_code)

print(r.headers['content-type'])

print(r.text)

POST SAMPLE :

data = {}

data['name'] = "toto"

data['username'] = "toto@toto.fr"

newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}

r = session.post("https://restapiurl/api/apifunction", data=json.dumps(data), headers=newHeaders)

print(r.status_code)

print(r.headers['content-type'])

print(r.text)
