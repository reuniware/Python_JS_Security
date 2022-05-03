#For downloading huge number of files through proxychains/tor

import urllib.request

from requests import get
from torrequest import TorRequest
import xml.etree.ElementTree as ET
import os
from urllib.parse import urlparse
import urllib.request

ip = get('https://api.ipify.org').text
print(f'My public IP address is: {ip}')

i = 0
# while True:
# with TorRequest(proxy_port=9150, ctrl_port=9151, password=None) as tr:
#     tr.reset_identity()

ip = get('https://api.ipify.org').text
print(f'My public IP address is: {ip}')
txt = get('URL WITH ').text
# print(txt)
i = i + 1

# Get the current working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

root = ET.fromstring(txt)
# print(root)
j = 0
for child in root:
    # print(child.tag, child.attrib)
    for subchild in child:
        # print(subchild.tag, subchild.text)
        if subchild.tag.endswith('THE XML NODE TO GET ONE FILE NAME TO DOWNLOAD'):
            # print(subchild.text)
            file = subchild.text
            url = 'URL WITH XML RESPONSE' + file
            print(url)
            a = urlparse(url)
            filename = os.path.basename(a.path)

            if os.path.exists(filename):
                print(filename, "already exists", "skipping")
                j = j + 1
            else:
                try:
                    urllib.request.urlretrieve(url, filename)
                    print("download ok : ", filename)
                    j = j + 1
                    print(j)
                except:
                    print("error")
