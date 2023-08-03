#import shlex
import subprocess
#import json

#Needed : An API Key from apilayer 
#Subscribe to Number Verification API :
#https://apilayer.com/?e=Sign+Up&l=Success
#https://apilayer.com/marketplace/number_verification-api#documentation-tab
# Sample of an API key (XXX at the end to mask the real one ;) ) : zUxrKHe83a3wLd7yIVECJEZ4XXXXXXXX
# 1000 requests/month in the free version

CurlUrl = "curl --request GET 'https://api.apilayer.com/number_verification/validate?number=14158586273' \
--header 'apikey: zUxrKHe83a3wLd7yIVECJEZ4XXXXXXXX'"

status, output = subprocess.getstatusoutput(CurlUrl)

print(status)
print(output)


