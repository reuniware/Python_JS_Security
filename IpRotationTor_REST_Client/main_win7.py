# coding: utf-8

# FOR NOW THERE IS NO IP ROTATION FOR THIS SCRIPT (ONLY THE FIRST TOR IP ADDRESS IS USED). I'M WORKING ON THAT.

# Add C:\...\Tor Browser\Browser\TorBrowser\Tor to the current user's environment variables (Windows 10/Windows 7)
import json
import requesocks

if __name__ == '__main__':
    print('Python + TOR')

session = requesocks.session()
session.proxies = {'http': 'socks5://127.0.0.1:9150', 'https': 'socks5://127.0.0.1:9150'}
r = session.get('http://www.ipecho.net/plain', auth=('user', 'pass'))
print(r.status_code)
print(r.headers['content-type'])
print(r.text)

data = {}
data['name'] = "toto"
data['username'] = "toto@toto.fr"
newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = session.post("https://apiserver/api/apifunction", data=json.dumps(data), headers=newHeaders)
print(r.status_code)
print(r.headers['content-type'])
print(r.text)
